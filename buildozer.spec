[app]
title = RuView SMART
package.name = ruviewsmart
package.domain = org.ruview.smart
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json,txt
version = 1.0.0
requirements = python3,kivy,plyer,pyjnius
orientation = portrait
fullscreen = 0
android.permissions = ACCESS_WIFI_STATE,ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION,POST_NOTIFICATIONS,VIBRATE,FOREGROUND_SERVICE
android.api = 33
android.minapi = 24
android.ndk = 25b
android.archs = arm64-v8a
android.build_tools_version = 33.0.2
android.accept_sdk_license = True
[buildozer]
log_level = 2
