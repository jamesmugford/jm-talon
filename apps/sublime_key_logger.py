"""Sublime-only Talon key translation via dotool."""

from talon import Context
import subprocess
import sys

from .key_translate_dotool import KeySpec, talon_key_to_dotool_actions

ctx = Context()
ctx.matches = r"""
app: Sublime Text
app: Sublime Text 4
app: Sublime Text 3
app: sublime_text
"""


@ctx.action_class("main")
class MainActions:
    @staticmethod
    def key(key: KeySpec):
        """Log and forward Talon key specs through dotoolc.

        Args:
            key: Talon key spec string.
        """
        print(f"sublime key: {key!r}", file=sys.stderr, flush=True)
        try:
            actions = talon_key_to_dotool_actions(key)
            if not actions:
                return
            # Send a small batch to dotoolc (dotoold should be running).
            subprocess.run(
                ["dotoolc"],
                input="\n".join(actions) + "\n",
                text=True,
                check=False,
                timeout=0.5,
            )
        except Exception as exc:
            print(f"sublime dotool error: {exc}", file=sys.stderr, flush=True)
