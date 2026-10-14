# ewokVPN

### [English](README.md) | Русский

ewokVPN — VPN-клиент, который умеет разворачивать VPN на вашем собственном сервере. Это форк
[AmneziaVPN](https://github.com/amnezia-vpn/amnezia-client), распространяемый под той же лицензией
[GNU General Public License v3.0](LICENSE).

> [!NOTE]
> ewokVPN — независимый проект. Он не связан с командой AmneziaVPN, не одобрен и не поддерживается ею.
> «Amnezia», «AmneziaVPN» и логотип Amnezia принадлежат их владельцам.
> О проблемах ewokVPN сообщайте в этом репозитории, а не в каналы поддержки AmneziaVPN.

## Происхождение и изменения

- Исходный проект: https://github.com/amnezia-vpn/amnezia-client
- Форк сделан от ветки `dev` исходного проекта, коммит `705a373` (октябрь 2026).
- Полный список изменений форка — в [NOTICE.md](NOTICE.md) и в истории git этого репозитория.

## Исходный код

Полный исходный код каждого релиза ewokVPN опубликован в этом репозитории:
https://github.com/HunterEwok/ewokvpn-amnezia-client. Каждый релиз собирается из git-тега с тем же названием.

## Особенности

- Простой в использовании — введите IP-адрес, SSH-логин и пароль, и ewokVPN автоматически установит VPN-контейнеры Docker на ваш сервер и подключится к VPN.
- Классические VPN-протоколы: OpenVPN, WireGuard и IKEv2.
- Протоколы с маскировкой трафика (обфускацией): OpenVPN с плагином [Cloak](https://github.com/cbeuw/Cloak), Shadowsocks (OpenVPN over Shadowsocks), [AmneziaWG](https://docs.amnezia.org/documentation/amnezia-wg/) и XRay.
- Поддержка Split Tunneling — добавляйте любые сайты или приложения в список, чтобы включить VPN только для них.
- Платформы: Windows, macOS, Linux, Android, iOS.

## Технологии

ewokVPN, как и AmneziaVPN, использует проекты с открытым исходным кодом:

- [OpenSSL](https://www.openssl.org/)
- [OpenVPN](https://openvpn.net/)
- [Qt](https://www.qt.io/)
- [LibSsh](https://libssh.org)
- [WireGuard](https://www.wireguard.com/)
- [Xray-core](https://xtls.github.io/en/)
- [Conan](https://conan.io/)
- и другие, см. [THIRD_PARTY_LICENSES.md](THIRD_PARTY_LICENSES.md)

## Переводы

Файлы переводов лежат в папке `client/translations`. Каждый файл `*.ts` содержит строки для одного языка.

## Проверка исходного кода

После клонирования репозитория обязательно загрузите все подмодули.

```bash
git submodule update --init --recursive
```

## Руководство по разработке

Хотите внести свой вклад? Добро пожаловать!

### Требования для сборки

* [`CMake`](https://cmake.org/download/)
* Компилятор и система сборки, в зависимости от таргета:
  - [Linux] Любые `make` и `gcc`
  - [Apple] [`Xcode`](https://developer.apple.com/xcode/) или [`Xcode command line tools`](https://developer.apple.com/xcode/)
  - [Windows] [`Visual Studio 2022`](https://aka.ms/vs/17/release/vs_community.exe) или [`VS 2022 Build Tools`](https://aka.ms/vs/17/release/vs_buildtools.exe)
  - [Android] [`Android SDK`](#установка-android-sdk) и [`Ninja`](https://ninja-build.org/)
* [`Qt 6.10+`](https://www.qt.io/download-open-source) со следующими модулями:
  - Основные модули для таргета (Desktop/Android/iOS)
  - Qt 5 Compatibility module
  - Qt Remote Objects
* Пакетный менеджер [`Conan`](https://conan.io/downloads)
  - На MacOS достаточно использовать `homebrew` или установить в `.venv` в корень проекта 
  - Для остальных систем необходимо прописать пути в `PATH`
* (Необязательно) Заивисимости для установщиков:
  - [Windows/Linux] [`Qt Installer Framework`](https://www.qt.io/download-open-source)
  - [Windows] [`WIX toolset`](https://github.com/wixtoolset/wix/releases)

### Сборка проекта через скрипты

* Запустите скрипты, находящиеся в папке `deploy`
* Если все зависимости установлены в стандартных локациях, скрипт найдёт их самостоятельно
* Если пути отличаются, их нужно явно указать используя:
  - `QT_INSTALL_DIR` - корневая папка установки Qt
  - `QT_ROOT_PATH`   - корневая папка Qt Framework
  - `QIF_ROOT_PATH`  - корневая папка Qt Installer Framework
  - `ANDROID_HOME`   - путь к Android SDK
  - и другие. Их можно получить из вышеуказанных скриптов

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

### Разработка в IDE

* Можно использовать любые IDE которые умеют работать с CMake и находить Qt Kits. Например:
  - `Qt Creator`
  - `Visual Studio Code` with `Qt Extension Pack`
  - и так далее

* Для использования `Xcode` нужно сконфигурировать проект с помощью `cmake`. Самый простой способ это сделать - использовать `Qt Creator` для конфигурации. Затем, нужно открыть файл `ewokVPN.xcodeproj` из папки сборки с помощью `Xcode`. Учтите, что никакие файлы фактически не сохраняются - они сохраняются в директории сборки. Если требуется, скопируйте файлы вручную

* `Android studio` может быть использована подобным вышеуказанному способу - нужно использовать `cmake` вручную или через `Qt Creator` для конфигурации. Далее, откройте `<build-dir>/client/android-build` в `Android studio`. Не забудьте скопировать изменённые файлы в папку с исходным кодом - все файлы, изменённые в IDE, сохраняются фактически в папке сборки.

### Установка Android SDK

* Android SDK может быть установлен следующими способами:
  - Используя `Qt Creator`, через настройки в пунктах `Preferences`->`SDKs`
  - Используя `Android studio`. По умолчанию необходимые `SDK` устанавливаются автоматически.
  - Вручную, используя `sdk-manager`. Подробности можно найти [здесь](https://developer.android.com/tools)

## Лицензия

ewokVPN — свободное программное обеспечение: вы можете распространять и изменять его на условиях
GNU General Public License версии 3, опубликованной Free Software Foundation (см. [LICENSE](LICENSE)).

Copyright (C) AmneziaVPN contributors. Изменения: Copyright (C) ewokVPN contributors.

Проект также включает сторонние компоненты под их собственными лицензиями
(см. [THIRD_PARTY_LICENSES.md](THIRD_PARTY_LICENSES.md)). Иконки ewokVPN
собираются из `branding/icons` скриптом `tools/generate_icons.py`.

## Поддержать авторов оригинала

ewokVPN построен на работе команды AmneziaVPN. Поддержать их можно через
[исходный проект](https://github.com/amnezia-vpn/amnezia-client#donate).
