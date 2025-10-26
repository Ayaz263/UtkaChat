[app]
title = UtkaChat
package.name = utkachat
package.domain = org.test
requirements = python3,kivy,requests,threading,socket
android.permissions = INTERNET
android.accept_sdk_license = True
android.permissions = INTERNET,ACCESS_NETWORK_STATE

- name: Build APK with Buildozer
  uses: digreatbrian/buildozer-action@v2
  with:
    python-version: 3.9
    buildozer-cmd: buildozer android debug --verbose
    work-dir: .

[buildozer]
log_level = 2
