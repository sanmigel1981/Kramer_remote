[app]

title = Kramer Remote
package.name = kramerremote
package.domain = org.kramer
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
requirements = python3,kivy==2.1.0,pyjnius,android
orientation = portrait

android.permissions = BLUETOOTH_SCAN,BLUETOOTH_CONNECT,ACCESS_FINE_LOCATION,INTERNET

android.api = 31
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a,armeabi-v7a
android.accept_sdk_license = True

p4a.bootstrap = sdl2
p4a.branch = master

# Исключаем проблемные Python 2 файлы из NDK
android.exclude_android_src = toolchains/llvm/prebuilt/linux-x86_64/share/clang, sources/third_party/googletest/scripts, build/tools, prebuilt/linux-x86_64/bin/*.py

[buildozer]
log_level = 2
warn_on_root = 1