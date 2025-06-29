name: Android Build with Buildozer

on:
  push:
    branches:
      - master
      - main
  pull_request:
    branches:
      - master
      - main

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'

    - name: Install Buildozer and dependencies
      run: |
        sudo apt-get update
        sudo apt-get install -y zip unzip git wget openjdk-17-jdk autoconf libtool pkg-config zlib1g-dev libncurses-dev libssl-dev build-essential python3-pip
        sudo apt-get install -y libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev
        pip install --upgrade pip setuptools
        pip install cython
        pip install buildozer==1.2.0

    - name: Manually download Android NDK and SDK
      run: |
        mkdir -p /home/runner/.buildozer/android/platform
        cd /home/runner/.buildozer/android/platform

        # Install Android SDK command-line tools
        mkdir android-sdk
        cd android-sdk
        wget https://dl.google.com/android/repository/commandlinetools-linux-8512546_latest.zip -O cmdtools.zip
        unzip cmdtools.zip -d cmdline-tools
        rm cmdtools.zip
        mv cmdline-tools cmdline-tools/latest

        export ANDROID_HOME=$PWD
        export PATH=$ANDROID_HOME/cmdline-tools/latest/bin:$PATH

        # Accept licenses
        yes | ./cmdline-tools/latest/bin/sdkmanager --sdk_root=$ANDROID_HOME --licenses

        # Install required SDK tools
        ./cmdline-tools/latest/bin/sdkmanager --sdk_root=$ANDROID_HOME \
          "platform-tools" \
          "platforms;android-33" \
          "build-tools;33.0.2"

        # Install NDK
        cd ..
        wget https://dl.google.com/android/repository/android-ndk-r25b-linux.zip
        unzip android-ndk-r25b-linux.zip
        rm android-ndk-r25b-linux.zip

    - name: Build Android APK
      run: |
        export ANDROIDSDK="/home/runner/.buildozer/android/platform/android-sdk"
        export ANDROIDNDK="/home/runner/.buildozer/android/platform/android-ndk-r25b"
        export PATH="$ANDROIDSDK/cmdline-tools/latest/bin:$PATH"
        export PATH="$ANDROIDSDK/platform-tools:$PATH"

        buildozer android debug

    - name: Upload APK artifact
      uses: actions/upload-artifact@v4
      with:
        name: FastTube-APK
        path: bin/*.apk
