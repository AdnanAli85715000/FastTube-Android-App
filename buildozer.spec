[app]

# (str) Aapki application ka naam jo phone par show hoga
title = FastTube

# (str) Android package ka unique ID (com.yourcompany.yourappname format mein)
package.name = com.fasttube.app # FastTube ke liye unique naam

# (str) Package domain (Android/iOS packaging ke liye zaroori)
package.domain = org.fasttube.dev # FastTube domain

# (str) Application ka version (aam taur par buildozer khud increase karta hai)
version = 0.1

# (list) Aapki application ki Python dependencies.
# requirements.txt se liya gaya, aur kuch common dependencies bhi shamil ki hain.
# pyjnius Android-specific functionality (Share Intent) ke liye zaroori hai.
# ffmpeg yt-dlp ke liye lazmi hai.
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

# (list) Android ABI list jin ke liye build karna hai.
# arm64-v8a modern Android phones ke liye common hai.
android.arch = arm64-v8a

# (list) Android permissions jo aapki app ko chahiye hongi.
# INTERNET: Videos download karne ke liye.
# WRITE_EXTERNAL_STORAGE: Videos ko phone storage mein save karne ke liye.
# READ_EXTERNAL_STORAGE: Storage se files read karne ke liye.
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# (list) Android activities. Share Intent handling ke liye yeh section ahem hai.
# Yeh AndroidManifest.xml mein intent-filters add karega.
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

[buildozer]

# (str) Default distribution to use
dist_name = fasttube

# (str) The directory containing the app's source code
source_dir = .
