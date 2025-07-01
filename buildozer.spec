    [app]

    # (str) The directory containing the app's source code (TOP PRIORITY)
    source.dir = . # <<< Yahan rakha gaya hai, [app] section mein sabse upar

    # (str) Aapki application ka naam jo phone par show hoga
    title = FastTube

    # (str) Android package ka unique ID (com.yourcompany.yourappname format mein)
    package.name = com.fasttube.app

    # (str) Package domain (Android/iOS packaging ke liye zaroori)
    package.domain = org.fasttube.dev

    # (str) Application ka version
    version = 0.1

    # (list) Python libraries required (requirements.txt se sync honi chahiye)
    # ffmpeg ko yahan se hata diya gaya hai, kyunke Buildozer khud handle karta hai.
    requirements = python3,kivy==2.1.0,requests,certifi,pyjnius,yt-dlp,Pillow

    # (str) Kivy version
    kivy.version = 2.1.0

    # (str) Android app ki category (Google Play Store ke liye).
    android.category = video

    # (int) Android target and minimum API
    android.api = 33
    android.minapi = 21

    # (str) Android NDK settings
    android.ndk = 25b
    android.ndk_api = 21
    android.ndk_path = /home/runner/.buildozer/android/platform/android-ndk-r25b

    # (str) Python-for-Android version
    p4a.version = master

    # (str) Build tools version (AIDL error ko fix karta hai)
    android.build_tools_version = 34.0.0

    # (list) ABI to target (modern Android phones ke liye)
    android.arch = arm64-v8a

    # (list) Required permissions
    android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

    # (list) Android activities for Share Intent (YouTube Links)
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

    # (str) Android app icon (agar aapke project folder mein icon.png hai to path den)
    # android.icon = %(source.dir)s/icon.png

    # (str) Android splash screen
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

    [buildozer]

    # (str) Default distribution to use
    dist_name = fasttube

    # (str) The directory containing the app's source code
    source_dir = . # <<< Yeh line [buildozer] section mein hai

    # (bool) Auto accept Android SDK licenses (Buildozer ko licenses automatically accept karne den)
    android.accept_sdk_license = True
    