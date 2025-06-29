[app]

# App Info
title = FastTube
package.name = com.fasttube.app
package.domain = org.fasttube.dev
version = 0.1

# Python Requirements
requirements = 
    python3,
    kivy==2.1.0,
    requests,
    certifi,
    pyjnius,
    ffmpeg-python,  # ffmpeg ki jagah ffmpeg-python istemal karein
    yt-dlp,
    android  # zaroori hai

# Kivy Version
kivy.version = 2.1.0

# Source Directory
source.dir = .

# Android Settings
android.arch = arm64-v8a  # ARM64 best hai
android.api = 33          # Android 13 (latest stable)
android.minapi = 21       # Minimum Android 5.0 support
android.ndk = 25b         # NDK version
android.sdk = 34          # SDK version
android.build_tools_version = 34.0.0  # Build tools version
android.accept_sdk_license = True     # Auto-accept licenses
android.allow_backup = False          # Security setting

# Permissions
android.permissions = 
    INTERNET,
    WRITE_EXTERNAL_STORAGE,
    READ_EXTERNAL_STORAGE

# YouTube Links Handle Karne Ke Liye
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
            - host: www.youtube.com \

# Main Script
android.entrypoint = main.py

# Build Settings
fullscreen = 1
debug = 1
log_level = 2  # Detailed logs
orientation = portrait  # Screen orientation

[buildozer]
log_level = 2  # Debugging ke liye
warn_on_root = 1  # Warnings show karega
