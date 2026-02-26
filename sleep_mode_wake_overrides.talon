# Override community wake phrases (non-Dragon only)

mode: command
mode: dictation
mode: sleep
not speech.engine: dragon
not tag: user.deep_sleep
-
^(wake up)+$: skip()
^talon wake [<phrase>]$: skip()

mode: sleep
not tag: user.deep_sleep
-
^(welcome back)+$: skip()

mode: sleep
tag: user.deep_sleep
-
^wake up and listen$: skip()
