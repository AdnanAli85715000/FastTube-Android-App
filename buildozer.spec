[app]

# (str) App name shown on the device
title = FastTube

# (str) Unique package name
package.name = com.fasttube.app

# (str) Domain name
package.domain = org.fasttube.dev

# (str) App version
version = 0.1

# (list) Required Python modules
requirements = python3,kivy==2.1.0,requests,certifi,pyjnius,ffmpeg,yt-dlp

# (str) Kivy version
kivy.version = 2.1.0

# (str) Your main.py directory
source.dir = .

# (str) Entry point
android.entrypoint = main.py

# (str) App icon
# android.icon = %(source.dir)s/icon.png

# (str) Splash image
# android.splash = %(source.dir)s/splash.png

# (str) Android category
android.category = video

# (int) Fullscreen mode
fullscreen = 1

# (bool) Debug build (1 = yes)
debug = 1

# (bool) Optimize APK (0 = no)
optimize = 0

# (int) Logging level
log_level = 2

# ✅ Android SDK / NDK Settings
android.api = 33
android.minapi = 21
android.ndk = 25b
android.ndk_api = 21

# ✅ Use manually downloaded NDK from GitHub Actions
android.ndk_path = /home/runner/.buildozer/android/platform/android-ndk-r25b

# ✅ Use a stable version of p4a
p4a.version = 0.6.0

# ✅ Architecture (GitHub runners support arm64)
android.arch = arm64-v8a

# ✅ Permissions
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# ✅ Share Intent / YouTube handling
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

# ✅ Presplash background (optional)
# android.presplash_bg = #000000

# ✅ Force specific build tools version if needed
# android.build_tools_version = 33.0.2

# ✅ Additional Java classes path (optional)
# android.add_jars = path/to/extra.jar

# ✅ Avoid problems with threading in ffmpeg/yt-dlp
android.allow_backup = 1

# ✅ Fix: Make sure project directory is visible
source_dir = .

[buildozer]

# (str) Distribution name
dist_name = fasttube

# (str) Again define your app directory
source_dir = .
