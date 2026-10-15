# ewokVPN

ewokVPN is a VPN client that can deploy a VPN server on your own server. It is a fork of
[AmneziaVPN](https://github.com/amnezia-vpn/amnezia-client) and is distributed under the same
[GNU General Public License v3.0](LICENSE).

> [!NOTE]
> ewokVPN is an independent project. It is not affiliated with, endorsed by, or supported by the
> AmneziaVPN team. "Amnezia", "AmneziaVPN" and the Amnezia logo belong to their respective owners.
> Please report ewokVPN problems in this repository, not to the AmneziaVPN support channels.

## Origin and changes

- Upstream project: https://github.com/amnezia-vpn/amnezia-client
- Forked from upstream branch `dev` at commit `705a373` (October 2026).
- The full list of changes made in this fork is in [NOTICE.md](NOTICE.md) and in the git history of this repository.

## Source code

The complete corresponding source code for every ewokVPN release is published in this repository:
https://github.com/HunterEwok/ewokvpn-amnezia-client. Each release is built from the git tag of the same name.

## Features

- Very easy to use - enter your IP address, SSH login, password and ewokVPN will automatically install VPN docker containers to your server and connect to the VPN.
- Classic VPN-protocols: OpenVPN, WireGuard and IKEv2 protocols.
- Protocols with traffic Masking (Obfuscation): OpenVPN over [Cloak](https://github.com/cbeuw/Cloak) plugin, Shadowsocks (OpenVPN over Shadowsocks), [AmneziaWG](https://docs.amnezia.org/documentation/amnezia-wg/) and XRay.
- Split tunneling support - add any sites to the client to enable VPN only for them or add Apps (only for Android and Desktop).
- Windows, MacOS, Linux, Android, iOS builds.

## Tech

ewokVPN, like AmneziaVPN, uses several open-source projects to work:

- [OpenSSL](https://www.openssl.org/)
- [OpenVPN](https://openvpn.net/)
- [Qt](https://www.qt.io/)
- [LibSsh](https://libssh.org)
- [WireGuard](https://www.wireguard.com/)
- [Xray-core](https://xtls.github.io/en/)
- [Conan](https://conan.io/)
- and more, see [THIRD_PARTY_LICENSES.md](THIRD_PARTY_LICENSES.md)

## Translations

Translation files are in the `client/translations` folder. Each `*.ts` file contains strings for one language.

## Checking out the source code

Make sure to pull all submodules after checking out the repo.

```bash
git submodule update --init --recursive
```

## Hacking guide

Want to contribute? Welcome!

### Build requirements

* [`CMake`](https://cmake.org/download/)
* Compiler and underlying build system, depending on the target:
  - [Linux] Any of `make` and `gcc`
  - [Apple] [`Xcode`](https://developer.apple.com/xcode/) or [`Xcode command line tools`](https://developer.apple.com/xcode/)
  - [Windows] [`Visual Studio 2022`](https://aka.ms/vs/17/release/vs_community.exe) or [`VS 2022 Build Tools`](https://aka.ms/vs/17/release/vs_buildtools.exe)
  - [Android] [`Android SDK`](#installing-android-sdk) and [`Ninja`](https://ninja-build.org/)
* [`Qt 6.10+`](https://www.qt.io/download-open-source) with the following modules:
  - Core module for targeting platform (Desktop/Android/iOS)
  - Qt 5 Compatibility module
  - Qt Remote Objects
* [`Conan`](https://conan.io/downloads) package manager
  - On MacOS is enough just to use `homebrew` or install it in `.venv` in project root
  - Other systems must have it in `PATH`
* (Optional) Installer dependencies:
  - [Windows/Linux] [`Qt Installer Framework`](https://www.qt.io/download-open-source)
  - [Windows] [`WIX toolset`](https://github.com/wixtoolset/wix/releases)

### Building the project using scripts

* Run scripts located in `deploy` directory
* Basically, if dependencies are located in default installation paths, the scripts will find them automatically.
* If they differ, specify them using the following variables:
  - `QT_INSTALL_DIR` - Qt root installation folder
  - `QT_ROOT_PATH`   - Qt framework root directory
  - `QIF_ROOT_PATH`  - Qt Installer Framework root path
  - `ANDROID_HOME`   - Path to Android SDK root folder
  - and others. Check scripts for more

Unix-like:
```bash
# Build executables for the host platform
deploy/build.sh

# Or just
deploy/build.sh

# Build executables and installers for the host platform
deploy/build.sh --installer all

# Build Android APK and AAB
deploy/build.sh -t android --aab

# Call for help
deploy/build.sh -h
```

Windows:
```batch
:: Build executables for Windows
deploy/build.bat

:: Build executables with IFW installer for Windows
deploy/build.bat --installer ifw

:: Build executables with IFW and WIX installer for Windows
deploy/build.bat --installer ifw --installer wix

:: Or just
deploy/build.bat --installer all
```

### Developing the project in IDEs

* Basically, you can use any IDE that handles CMake and Qt kits properly to run configure and build steps, and to navigate through the code nicely. For example:
  - `Qt Creator`
  - `Visual Studio Code` with `Qt Extension Pack`
  - and so on

* To use `Xcode`, you have to configure project first by using `cmake`. The easiest way to do it is to use `Qt Creator` for configuration. Then open `ewokVPN.xcodeproj` file from the build folder by using `Xcode`. Note that none of the files changed are saved - the files actually getting changed in build directory. Copy them manually if necessary

* `Android studio` could be used in the same way - just configure the project by using `cmake` manually or by using `Qt Creator`. Open `<build-dir>/client/android-build` in `Android studio` then. Do not forget to copy the changes - everything you do is saved under the build directory actually.

### Installing Android SDK

* Android SDK could be installed using the following methods:
  - Using `Qt Creator`. Use `Preferences`->`SDKs`
  - Using `Android studio`. By default it installs necessary `SDKs` automatically during the installation
  - Manually by using `sdk-manager`. Check [this](https://developer.android.com/tools) page for details

## License

ewokVPN is free software: you can redistribute it and/or modify it under the terms of the
GNU General Public License as published by the Free Software Foundation, version 3 (see [LICENSE](LICENSE)).

Copyright (C) AmneziaVPN contributors. Modifications copyright (C) ewokVPN contributors.

This project also includes third-party components distributed under their own terms
(see [THIRD_PARTY_LICENSES.md](THIRD_PARTY_LICENSES.md)). The ewokVPN icons
are generated from `branding/icons` by `tools/generate_icons.py`.

## Support the original developers

ewokVPN is built on the work of the AmneziaVPN team. If you want to support them, see the
[upstream project](https://github.com/amnezia-vpn/amnezia-client#donate).
