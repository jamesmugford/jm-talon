# Override community sleep phrases (non-Dragon only)

mode: command
mode: dictation
mode: sleep
not speech.engine: dragon
-
^go to sleep [<phrase>]$: skip()
^talon sleep [<phrase>]$: skip()
^sleep all [<phrase>]$: skip()
