# MOBILEAPK

> **🚨 SETUP REQUIRED:** If you're seeing a 404 error on GitHub Pages, you need to **[merge Pull Request #2](https://github.com/cfaamir789/MOBILEAPK/pull/2)** to deploy to the `main` branch. See [SETUP_INSTRUCTIONS.md](SETUP_INSTRUCTIONS.md) for details.

[![Live Preview](https://img.shields.io/badge/Live%20Preview-GitHub%20Pages-blue?style=for-the-badge&logo=github)](https://cfaamir789.github.io/MOBILEAPK/)
[![Build APK](https://github.com/cfaamir789/MOBILEAPK/workflows/Build%20Android%20APK/badge.svg)](https://github.com/cfaamir789/MOBILEAPK/actions)
[![Latest Release](https://img.shields.io/github/v/release/cfaamir789/MOBILEAPK?style=for-the-badge)](https://github.com/cfaamir789/MOBILEAPK/releases/latest)

A mobile application with both web preview and native Android APK.

## 📱 Live Web Preview

View the interactive live preview of this mobile app directly in your browser:

**👉 [https://cfaamir789.github.io/MOBILEAPK/](https://cfaamir789.github.io/MOBILEAPK/)**

The preview shows a realistic Android phone frame with:
- Interactive app bar and navigation
- Live clock in the status bar
- Scrollable content cards
- Tap interactions on each card

## 📥 Download Android APK

> **📦 APK Status:** The APK will be automatically built and published after merging [PR #2](https://github.com/cfaamir789/MOBILEAPK/pull/2) to the `main` branch. Check the [Releases page](https://github.com/cfaamir789/MOBILEAPK/releases/latest) after merging.

**[⬇️ Download Latest APK](https://github.com/cfaamir789/MOBILEAPK/releases/latest)** (Available after first merge to `main`)

### Installation Instructions:

1. **Download** the APK file from the [latest release](https://github.com/cfaamir789/MOBILEAPK/releases/latest)
2. **Enable Unknown Sources**:
   - Go to your Android device's **Settings**
   - Navigate to **Security** or **Privacy**
   - Enable **"Install from Unknown Sources"** or **"Install Unknown Apps"**
3. **Install** the APK:
   - Open your device's file manager or downloads folder
   - Tap on the downloaded APK file
   - Follow the installation prompts
4. **Launch** the MobileAPK app from your app drawer

### Minimum Requirements:
- Android 5.0 (API level 21) or higher
- ~10 MB storage space

## 🔨 Building from Source

To build the APK yourself:

```bash
cd android
./gradlew assembleRelease
```

The APK will be generated at: `android/app/build/outputs/apk/release/app-release-unsigned.apk`

## 🚀 Deployment

### Web Preview (GitHub Pages)
The live preview is automatically deployed to **GitHub Pages** on every push to `main` via the workflow `.github/workflows/deploy-pages.yml`.

### Android APK Build
The Android APK is automatically built on every push to `main` via the workflow `.github/workflows/build-apk.yml` and published to GitHub Releases.

## 🛠️ Development

### Project Structure
```
├── index.html                    # Web preview
├── android/                      # Android app source
│   ├── app/
│   │   ├── src/main/
│   │   │   ├── java/com/mobileapk/
│   │   │   │   └── MainActivity.java
│   │   │   ├── res/              # Resources
│   │   │   └── AndroidManifest.xml
│   │   └── build.gradle          # App-level Gradle config
│   ├── build.gradle              # Project-level Gradle config
│   └── settings.gradle
└── .github/workflows/            # CI/CD workflows
```

## 📄 License

This project is open source and available for educational purposes.
