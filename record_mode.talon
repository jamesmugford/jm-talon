os: linux
mode: user.record
-
^command mode$:
    mode.disable("user.record")
    mode.disable("dictation")
    mode.enable("command")
^mixed mode$:
    mode.disable("user.record")
    mode.enable("dictation")
    mode.enable("command")
^record toggle$:
    user.system_command("/usr/bin/gobs-cli record toggle && /usr/bin/pw-play /usr/share/sounds/freedesktop/stereo/device-added.oga")
