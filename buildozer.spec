[app]

# (str) Aapki application ka naam jo phone par show hoga
title = FastTube

# (str) Android package ka unique ID (com.yourcompany.yourappname format mein)
package.name = com.fasttube.app

# (str) Package domain (Android/iOS packaging ke liye zaroori)
package.domain = org.fasttube.dev

# (str) Application ka version (aam taur par buildozer khud increase karta hai)
version = 0.1

# (list) Aapki application ki Python dependencies.
requirements = python3,kivy==2.1.0,requests,certifi,pyjnius,ffmpeg,yt-dlp

# (str) Kivy version jo aap use kar rahen hain.
kivy.version = 2.1.0

# (list) Custom source folders for python modules (directories relative to the main.py)
source.include_dirs =

# (str) Android app ki category (Google Play Store ke liye).
android.category = video

# (list) Android target SDK version. Latest stable API level istemal karein.
android.api = 33

# (list) Android minimum SDK version. Purane phones ke liye compatibility.
android.minapi = 21

# (str) Android NDK version (Buildozer ke liye recommended).
android.ndk = 25b

# (list) Android NDK API version. Target API level ke mutabiq ho.
android.ndk_api = 21

# (str) Python-for-Android (p4a) version.
p4a.version = 0.6.0

# (list) Android ABI list jin ke liye build karna hai.
android.arch = arm64-v8a

# (list) Android permissions jo aapki app ko chahiye hongi.
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# (list) Android activities. Share Intent handling ke liye yeh section ahem hai.
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

# (str) Android entry point for the app (usually main.py)
android.entrypoint = main.py

# (str) Android app icon. Agar aapke project folder mein icon.png hai to path den.
# android.icon = %(source.dir)s/icon.png

# (str) Android splash screen.
# android.splash = %(source.dir)s/splash.png

# (bool) Full screen app
fullscreen = 1

# (bool) Allow a debug build (0 = release build)
debug = 1

# (bool) Optimize for size
optimize = 0

# (list) Presplash background color (for Android)
# android.presplash_bg = #000000

# (str) User interface to use for logs
log_level = 2

# (str) The directory containing the app's source code (Redundant but for fix)
source_dir = . # <<< Nayi line yahan add ki gayi hai, [app] section mein

[buildozer]

# (str) Default distribution to use
dist_name = fasttube

# (str) The directory containing the app's source code
source_dir = . # <<< Yeh line pehle se mojood hai, isay rehne den
