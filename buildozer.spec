[app]

# (str) Aapki application ka naam jo phone par show hoga
title = FastTube

# (str) Android package ka unique ID (com.yourcompany.yourappname format mein)
package.name = com.fasttube.app

# (str) Package domain (Android/iOS packaging ke liye zaroori)
package.domain = org.fasttube.dev

# (str) Application ka version
version = 0.1

# (list) Python libraries required
requirements = python3,kivy==2.1.0,requests,certifi,pyjnius,ffmpeg,yt-dlp

# (str) Kivy version
kivy.version = 2.1.0

# (list) Python modules folder
source.dir = . # <<< Yeh line [app] section mein redundant hai, lekin troubleshooting ke liye rakhi hai

# (str) Android category
android.category = video

# (int) Android target and minimum API
android.api = 33
android.minapi = 21

# (str) Android NDK settings
android.ndk = 25b
android.ndk_api = 21
# NDK path ko manually android_build.yml mein set kiya gaya hai,
# lekin yahan specify karna Buildozer ki internal logic ke liye madadgar ho sakta hai.
android.ndk_path = /home/runner/.buildozer/android/platform/android-ndk-r25b

# (str) Python-for-Android version (master = latest stable from GitHub)
# "master" latest version uthayega. Agar stability issue aaye to specific version (e.g., 0.6.0) use karein.
p4a.version = master

# (str) Build tools version (fixes AIDL error)
# Yeh version android_build.yml mein install hone wale version se match hona chahiye.
android.build_tools_version = 34.0.0 # <<< Yahan 36.0.0 se 34.0.0 kiya gaya hai

# (list) ABI to target
android.arch = arm64-v8a

# (list) Required permissions
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# (list) Share Intent Filters (YouTube Links)
android.activities = \
    org.kivy.android.PythonActivity: \
        - intent_filters: \
            - action: android.intent.action.SEND \
            - category: android.intent.category.DEFAULT \
            - data: \
                - scheme: content \
                - host: * \
                - mime_type: text/plain \
            - data: \
                - scheme: http \
                - host: youtu.be \
            - data: \
                - scheme: http \
                - host: www.youtu.be \
            - data: \
                - scheme: https \
                - host: youtu.be \
            - data: \
                - scheme: https \
                - host: www.youtu.be \
            - data: \
                - scheme: http \
                - host: youtube.com \
            - data: \
                - scheme: http \
                - host: www.youtube.com \
            - data: \
                - scheme: https \
                - host: youtube.com \
            - data: \
                - scheme: https \
                - host: www.youtube.com \
            - data: \
                - scheme: http \
                - host: m.youtube.com \
            - data: \
                - scheme: https \
                - host: m.youtube.com \

# (str) Main script to run
android.entrypoint = main.py

# (bools)
fullscreen = 1
debug = 1
optimize = 0

# (str) Log verbosity level
log_level = 2

# (str) Redundant source fix (yeh line [app] section mein hai)
# source_dir = . # <<< Yeh line ab upar 'source.dir = .' ke naam se mojood hai, isay duplicate na karein.

[buildozer]

# (str) Dist name
dist_name = fasttube

# (str) Source directory again (redundant but safe)
source_dir = .

# ✅ Auto accept Android SDK licenses
android.accept_sdk_license = True
