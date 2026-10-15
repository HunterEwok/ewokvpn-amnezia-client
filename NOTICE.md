# NOTICE

ewokVPN is a modified version of AmneziaVPN.

- Original work: AmneziaVPN, https://github.com/amnezia-vpn/amnezia-client
  Copyright (C) AmneziaVPN contributors. Licensed under the GNU General Public License v3.0.
- Modified work: ewokVPN, https://github.com/HunterEwok/ewokvpn-amnezia-client
  Modifications copyright (C) ewokVPN contributors. Licensed under the GNU General Public License v3.0.

This notice is provided to satisfy section 5(a) of the GPL-3.0 ("The work must carry prominent notices
stating that you modified it, and giving a relevant date"). The authoritative, file-by-file record of
changes is the git history of this repository.

ewokVPN is not affiliated with or endorsed by the AmneziaVPN team. "Amnezia" and "AmneziaVPN" are
used only to identify the original project and its protocols and services (for example AmneziaWG,
AmneziaDNS and Amnezia Premium).

## Changes

### 2026-10-14: fork and rebranding

Forked from upstream branch `dev` at commit `705a373d510102fbce3c75149d005ca533717b10`.
No VPN functionality was changed.

- Product name changed from AmneziaVPN to ewokVPN: executables (`ewokVPN`, `ewokVPN-service`),
  installers and package names, Linux/macOS/Windows service and desktop files, CI artifact names.
- Application identifiers changed so the fork does not reuse upstream identities:
  Android `applicationId` `com.ewokvpn.app`, Apple bundle id `com.ewokvpn.ewokVPN`,
  app group `group.com.ewokvpn.ewokVPN`. The upstream Apple Development Team ID was removed.
- User-facing strings that name the application now say ewokVPN (UI, translations, Android
  strings and notifications). Strings that refer to upstream protocols and services keep the
  Amnezia name.
- The About page states that ewokVPN is a fork of AmneziaVPN under GPL-3.0, links to the
  ewokVPN source code and to the original AmneziaVPN project.
- Built-in app update checks are disabled by default (`CLIENT_ENABLE_APP_UPDATES=0`), because they
  query the AmneziaVPN gateway and would offer upstream AmneziaVPN installers.
- Windows file version resources keep the upstream copyright and add the fork's.
- README files rewritten for the fork; THIRD_PARTY_LICENSES.md extended with dependencies that were
  missing from it.

### 2026-10-14: ewokVPN icons

- All AmneziaVPN logos and app icons replaced with the ewokVPN day and night icons
  (`branding/icons`, generated for every platform by `tools/generate_icons.py`).
- iOS uses the night icon as the dark-appearance app icon. The tray, notification and
  quick-settings icons use a new ewok head silhouette.
- Unused AmneziaVPN logo files (wordmarks and `AmneziaVPN_Full_logo.svg`) removed.
