[app]

# (str) Title of your application
title = Kramer Remote

# (str) Package name
package.name = kramerremote

# (str) Package domain (needed for android/ios packaging)
package.domain = org.kramer

# (str) Source code directory
source.dir = .

# (list) Source files to include/ignore
source.include_exts = py,png,jpg,kv,atlas,ttf,txt
source.exclude_exts = spec
source.exclude_dirs = tests, bin, docs, __pycache__

# (str) Version of your application
version = 1.0

# (str) Entry point for your application
entrypoint = main.py

# (list) Python requirements
requirements = python3,kivy,pyjnius,android

# (str) Orientation of your application (portrait, landscape, or both)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
android.permissions = BLUETOOTH_SCAN,BLUETOOTH_CONNECT,ACCESS_FINE_LOCATION,INTERNET

# (int) Android API level (Android version)
android.api = 31

# (int) Minimum API level
android.minapi = 21

# (int) Android NDK version
android.ndk = 23b

# (list) Android architectures to build for
android.archs = arm64-v8a,armeabi-v7a

# (bool) Accept Android SDK license
android.accept_sdk_license = True

# (str) Android entry point (leave as is)
android.entrypoint = org.kivy.android.PythonActivity

# (str) Bootstrap to use for Android (sdl2, pygame, webview)
p4a.bootstrap = sdl2

# (str) python-for-android branch/tag to use
p4a.branch = v2023.09.16

# (bool) Use the SDL2 window provider
window_provider = sdl2

# (str) Android private storage (leave as is)
# android.private_storage = applibs

# (str) Android permission mapping (leave as is)
android.permission_mapping = android.permission_mapping.json

# (bool) Enable AndroidX support
android.enable_androidx = True

# (str) Log level for buildozer (0=error, 1=warning, 2=info, 3=debug)
log_level = 2

# (bool) Warn if running as root
warn_on_root = 1

[buildozer]
# Отключаем автоматическое обновление/клонирование python-for-android
p4a.update = False
p4a.local = 1