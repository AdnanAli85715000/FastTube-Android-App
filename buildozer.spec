[app]
title = FastTube
package.name = com.fasttube.app
package.domain = org.fasttube.dev
version = 0.1

requirements = 
    python3,
    kivy==2.1.0,
    requests,
    certifi,
    pyjnius,
    ffmpeg-python,
    yt-dlp,
    android

kivy.version = 2.1.0
source.dir = .
android.entrypoint = main.py

# Android Settings
android.arch = arm64-v8a
android.api = 33
android.minapi = 21
android.ndk = 25b
android.sdk = 34
android.build_tools_version = 34.0.0
android.accept_sdk_license = True
android.allow_backup = False

# Permissions
android.permissions = 
    INTERNET,
    WRITE_EXTERNAL_STORAGE,
    READ_EXTERNAL_STORAGE

# YouTube Intent Filters
android.activities = org.kivy.android.PythonActivity: \
    - intent_filters: \
        - action: android.intent.action.SEND \
        - category: android.intent.category.DEFAULT \
        - data: \
            - scheme: http \
            - host: youtu.be \
        - data: \
            - scheme: https \
            - host: youtu.be \
        - data: \
            - scheme: http \
            - host: www.youtube.com \
        - data: \
            - scheme: https \
            - host: www.youtube.com

# Build Settings
fullscreen = 1
debug = 1
log_level = 2

[buildozer]
log_level = 2
warn_on_root = 1
