os: linux
mode: command
not mode: user.record
-
^record mode$:
    mode.disable("dictation")
    mode.disable("command")
    mode.enable("user.record")
