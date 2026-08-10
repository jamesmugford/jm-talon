# Override community wake/sleep phrases (non-Dragon only)

mode: command
mode: dictation
mode: sleep
not speech.engine: dragon
not tag: user.deep_sleep
-
^(wake up)+$: skip()
^talon wake [<phrase>]$: skip()
