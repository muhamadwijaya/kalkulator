[app]
title = Kalkulator Saham
package.name = kalkulatorsaham
package.domain = io.github.muhamadwijaya
source.dir = .
source.include_exts = py,png,json
source.exclude_patterns = smoke_test.py,presplash.png,bin/*,build.log
version = 0.1.0
requirements = python3,kivy
orientation = portrait
fullscreen = 0
icon.filename = %(source.dir)s/icon.png
presplash.filename = %(source.dir)s/presplash.png
android.presplash_color = #0E1319

android.api = 34
android.minapi = 24
android.archs = arm64-v8a, armeabi-v7a
android.accept_sdk_license = True
android.allow_backup = True
android.debug_artifact = apk

[buildozer]
log_level = 2
warn_on_root = 1
