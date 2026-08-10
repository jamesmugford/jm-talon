from talon import Context, Module, actions, cron

try:
    import winsound
except ImportError:
    winsound = None

ctx = Context()
mod = Module()

@mod.action_class
class Actions:

    def play_beep():
        """Switches the parrot mode around"""
        if winsound:
            winsound.Beep(1000, 500)
