# Override community welcome-back phrase

mode: sleep
not tag: user.deep_sleep
-
^(welcome back)+$: skip()
