[app]
title = UtkaChat
package.name = utkachat
package.domain = org.test
# Объедините все разрешения в одну строку
requirements = python3,kivy,requests,threading,socket
android.permissions = INTERNET,ACCESS_NETWORK_STATE
android.accept_sdk_license = True

[buildozer]
log_level = 2
