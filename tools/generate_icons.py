#!/usr/bin/env python3
"""Generate every ewokVPN app icon from the two masters in branding/icons.

branding/icons/day.png and night.png are square app icons with rounded corners
on a flat page background (the corners are rebuilt here). Replace them with
higher-resolution renders of the same design and re-run:

    python3 tools/generate_icons.py

Requires Pillow.
"""

import json
import os

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "branding", "icons")
CLIENT = os.path.join(ROOT, "client")

# Corner radius of the rounded-square masters, as a fraction of their side.
CORNER = 100 / 440
# Square around the ewok's head, as fractions of the master side (left, top, right, bottom).
FACE_BOX = (70 / 440, 20 / 440, 370 / 440, 320 / 440)
# Status/notification silhouette colours used by the desktop tray.
TRAY_COLORS = {"default": (128, 128, 128, 255), "active": (255, 255, 255, 255), "error": (255, 0, 0, 255)}
BROWN = (59, 36, 20, 255)


def p(*parts):
    return os.path.join(ROOT, *parts)


def rounded_mask(size, radius_frac, inset=0, supersample=4):
    s = size * supersample
    m = Image.new("L", (s, s), 0)
    i = inset * supersample
    ImageDraw.Draw(m).rounded_rectangle((i, i, s - 1 - i, s - 1 - i), radius=radius_frac * s, fill=255)
    return m.resize((size, size), Image.LANCZOS)


def circle_mask(size, supersample=4):
    s = size * supersample
    m = Image.new("L", (s, s), 0)
    ImageDraw.Draw(m).ellipse((0, 0, s - 1, s - 1), fill=255)
    return m.resize((size, size), Image.LANCZOS)


def full_bleed(master):
    """Fill the page-coloured corners with the icon's own background.

    Each corner pixel takes the colour of the point just inside the rounded
    edge on the line towards that corner's arc centre, then the filled area is
    smoothed so it blends into the original background.
    """
    img = master.convert("RGB")
    n = img.width
    r = CORNER * n
    inset = 5
    src = img.load()
    filled = img.copy()
    dst = filled.load()
    outside = Image.new("L", (n, n), 0)
    out_px = outside.load()
    for y in range(n):
        for x in range(n):
            cx = r if x < r else (n - 1 - r if x > n - 1 - r else None)
            cy = r if y < r else (n - 1 - r if y > n - 1 - r else None)
            if cx is None or cy is None:
                continue
            dx, dy = x - cx, y - cy
            dist = (dx * dx + dy * dy) ** 0.5
            limit = r - inset
            if dist <= limit:
                continue
            k = limit / dist
            sx, sy = cx + dx * k, cy + dy * k
            dst[x, y] = src[int(round(sx)), int(round(sy))]
            out_px[x, y] = 255
    smooth = filled.filter(ImageFilter.GaussianBlur(3))
    feather = outside.filter(ImageFilter.GaussianBlur(1.5))
    filled = Image.composite(smooth, filled, outside)
    return Image.composite(filled, img, feather)


def save(img, *parts):
    path = p(*parts)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    img.save(path)
    print("wrote", os.path.relpath(path, ROOT))


class Icon:
    def __init__(self, master_path):
        self.full = full_bleed(Image.open(master_path)).resize((1024, 1024), Image.LANCZOS)
        self.full = self.full.filter(ImageFilter.UnsharpMask(radius=2, percent=60, threshold=2))

    def square(self, size):
        return self.full.resize((size, size), Image.LANCZOS)

    def rounded(self, size, padding=0.0):
        inner = round(size * (1 - 2 * padding))
        icon = self.square(inner).convert("RGBA")
        icon.putalpha(rounded_mask(inner, CORNER))
        canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        off = (size - inner) // 2
        canvas.paste(icon, (off, off), icon)
        return canvas

    def face(self, size):
        n = self.full.width
        box = tuple(round(v * n) for v in FACE_BOX)
        return self.full.crop(box).resize((size, size), Image.LANCZOS)

    def face_round(self, size, scale=1.0):
        inner = round(size * scale)
        face = self.face(inner).convert("RGBA")
        face.putalpha(circle_mask(inner))
        canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        off = (size - inner) // 2
        canvas.paste(face, (off, off), face)
        return canvas

    def edge_color(self):
        face = self.face(256).convert("RGB")
        ring = [face.getpixel((x, y)) for x in range(256) for y in range(256)
                if 120 ** 2 <= (x - 128) ** 2 + (y - 128) ** 2 <= 127 ** 2]
        return tuple(sum(c[i] for c in ring) // len(ring) for i in range(3))


def silhouette(size, color, supersample=4):
    """Monochrome ewok head (hood with ears) for tray and status icons."""
    s = size * supersample
    k = s / 256
    m = Image.new("L", (s, s), 0)
    d = ImageDraw.Draw(m)
    for cx in (62, 194):
        d.ellipse(((cx - 38) * k, 30 * k, (cx + 38) * k, 106 * k), fill=255)
    d.ellipse((40 * k, 46 * k, 216 * k, 222 * k), fill=255)
    for cx in (100, 156):
        d.ellipse(((cx - 14) * k, 112 * k, (cx + 14) * k, 140 * k), fill=0)
    d.ellipse((112 * k, 150 * k, 144 * k, 174 * k), fill=0)
    m = m.resize((size, size), Image.LANCZOS)
    img = Image.new("RGBA", (size, size), color)
    img.putalpha(m)
    return img


SILHOUETTE_VECTOR = """<?xml version="1.0" encoding="utf-8"?>
<!-- ewokVPN head silhouette, generated by tools/generate_icons.py -->
<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="256dp"
    android:height="256dp"
    android:viewportWidth="256"
    android:viewportHeight="256">
  <path
      android:fillColor="#FFFFFFFF"
      android:fillType="evenOdd"
      android:pathData="M62,30a38,38 0,1 0,0.1 0zM194,30a38,38 0,1 0,0.1 0zM128,46a88,88 0,1 0,0.1 0zM100,112a14,14 0,1 0,0.1 0zM156,112a14,14 0,1 0,0.1 0zM128,150a16,12 0,1 0,0.1 0z"/>
</vector>
"""


def banner(day, w, h):
    top, bottom = (241, 232, 210), (228, 212, 178)
    img = Image.new("RGBA", (w, h))
    d = ImageDraw.Draw(img)
    for y in range(h):
        t = y / max(1, h - 1)
        d.line([(0, y), (w, y)], fill=tuple(round(a + (b - a) * t) for a, b in zip(top, bottom)) + (255,))
    face = day.face_round(round(h * 0.8))
    img.paste(face, (round(h * 0.1), round(h * 0.1)), face)
    x = round(h * 1.0)
    size = round(h * 0.3)
    while True:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", size)
        if d.textlength("ewokVPN", font=font) <= w - x - h * 0.1 or size <= 6:
            break
        size -= 1
    d.text((x, h / 2), "ewokVPN", font=font, fill=BROWN, anchor="lm")
    return img


def main():
    day = Icon(os.path.join(SRC, "day.png"))
    night = Icon(os.path.join(SRC, "night.png"))

    # --- shared desktop images
    save(day.rounded(256), "client", "images", "icon.png")
    save(day.rounded(512), "deploy", "data", "linux", "ewokVPN.png")
    save(day.rounded(480), "metadata", "en-US", "images", "icon.png")
    logo = Image.new("RGBA", (1440, 1200), (0, 0, 0, 0))
    big = day.rounded(1100)
    logo.paste(big, ((1440 - 1100) // 2, 50), big)
    save(logo, "client", "images", "ewokBigLogo.png")
    for name, color in TRAY_COLORS.items():
        save(silhouette(200, color), "client", "images", "tray", name + ".png")

    # --- Windows / macOS standalone icon files
    ico = day.rounded(256)
    ico.save(p("client", "images", "app.ico"), sizes=[(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
    print("wrote client/images/app.ico")
    mac = day.rounded(1024, padding=100 / 1024)
    mac.save(p("client", "images", "app.icns"))
    print("wrote client/images/app.icns")
    for catalog in ("Images.xcassets", "Images-beta.xcassets"):
        folder = p("client", "macos", "app", catalog, "AppIcon.appiconset")
        for fname in sorted(os.listdir(folder)):
            if not fname.endswith(".png"):
                continue
            base = fname[:-4]
            size = int(base.split("@")[0]) * (2 if base.endswith("@2x") else 1)
            save(day.rounded(1024, padding=100 / 1024).resize((size, size), Image.LANCZOS),
                 "client", "macos", "app", catalog, "AppIcon.appiconset", fname)

    # --- iOS: single-size app icon with a dark (night) variant
    ios = p("client", "ios", "app", "Media.xcassets", "AppIcon.appiconset")
    for fname in os.listdir(ios):
        if fname.endswith(".png"):
            os.remove(os.path.join(ios, fname))
    save(day.square(1024), "client", "ios", "app", "Media.xcassets", "AppIcon.appiconset", "AppIcon.png")
    save(night.square(1024), "client", "ios", "app", "Media.xcassets", "AppIcon.appiconset", "AppIcon-dark.png")
    contents = {
        "images": [
            {"filename": "AppIcon.png", "idiom": "universal", "platform": "ios", "size": "1024x1024"},
            {"appearances": [{"appearance": "luminosity", "value": "dark"}],
             "filename": "AppIcon-dark.png", "idiom": "universal", "platform": "ios", "size": "1024x1024"},
        ],
        "info": {"author": "xcode", "version": 1},
    }
    with open(os.path.join(ios, "Contents.json"), "w") as f:
        json.dump(contents, f, indent=2)
        f.write("\n")
    launch = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0))
    li = day.rounded(512)
    launch.paste(li, (256, 256), li)
    save(launch, "client", "ios", "app", "launch.png")

    # --- Android
    res = ("client", "android", "res")
    dens = {"ldpi": 0.75, "mdpi": 1, "hdpi": 1.5, "xhdpi": 2, "xxhdpi": 3, "xxxhdpi": 4}
    for d, k in dens.items():
        folder = p(*res, "mipmap-" + d)
        if os.path.exists(os.path.join(folder, "icon.png")):
            save(day.rounded(round(48 * k)), *res, "mipmap-" + d, "icon.png")
        if os.path.exists(os.path.join(folder, "icon_round.png")):
            save(day.face_round(round(48 * k)), *res, "mipmap-" + d, "icon_round.png")
        if os.path.exists(os.path.join(folder, "ic_launcher_foreground.png")):
            save(day.face_round(round(108 * k), scale=72 / 108), *res, "mipmap-" + d, "ic_launcher_foreground.png")
        if os.path.exists(os.path.join(folder, "ic_banner.png")):
            save(banner(day, round(160 * k), round(90 * k)), *res, "mipmap-" + d, "ic_banner.png")
    r, g, b = day.edge_color()
    with open(p(*res, "drawable", "ic_launcher_background.xml"), "w") as f:
        f.write('<?xml version="1.0" encoding="utf-8"?>\n'
                '<shape xmlns:android="http://schemas.android.com/apk/res/android"\n'
                '    android:shape="rectangle">\n'
                f'    <solid android:color="#{r:02X}{g:02X}{b:02X}" />\n'
                '</shape>\n')
    with open(p(*res, "drawable", "ic_amnezia_round.xml"), "w") as f:
        f.write(SILHOUETTE_VECTOR)
    print("wrote android drawables")


if __name__ == "__main__":
    main()
