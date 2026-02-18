from talon import Context
import subprocess
import sys

from .keymap_dotool import KEY_NAME_MAP, MODIFIER_ALIASES, SYMBOL_KEY_MAP

# Translate Talon key specs into dotool actions for Sublime.


ctx = Context()
ctx.matches = r"""
app: Sublime Text
app: Sublime Text 4
app: Sublime Text 3
app: sublime_text
"""


def _normalize_key_name(key: str) -> str:
    if not key:
        return key
    if key in SYMBOL_KEY_MAP:
        return SYMBOL_KEY_MAP[key]
    if key.startswith("keypad_"):
        return "kp" + key[len("keypad_") :]
    key_lower = key.lower()
    if not key.startswith("x:") and not key.startswith("k:"):
        key = key_lower
    return KEY_NAME_MAP.get(key, key)


def _split_modifiers(chord: str) -> tuple[list[str], str]:
    parts = chord.split("-")
    mods = []
    key_parts = []
    for part in parts:
        if not key_parts and part in MODIFIER_ALIASES:
            mods.append(MODIFIER_ALIASES[part])
        else:
            key_parts.append(part)
    return mods, "-".join(key_parts)


def _build_chord(mods: list[str], key: str) -> str:
    parts = mods[:]
    if key:
        parts.append(key)
    return "+".join(parts)


def _mods_only_actions(mods: list[str]) -> list[str]:
    if not mods:
        return []
    actions = [f"keydown {mod}" for mod in mods]
    actions.extend(f"keyup {mod}" for mod in reversed(mods))
    return actions


def _parse_suffix(chord: str) -> tuple[str, str, int]:
    # Handle :down/:up and :N suffixes.
    if ":" not in chord:
        return chord, "key", 1
    base, suffix = chord.rsplit(":", 1)
    if suffix.isdigit():
        return base, "key", max(1, int(suffix))
    if suffix == "down":
        return base, "keydown", 1
    if suffix == "up":
        return base, "keyup", 1
    return chord, "key", 1


def _normalize_alpha_key(key: str, mods: list[str]) -> str:
    if key and len(key) == 1 and key.isalpha() and key.isupper():
        if "shift" not in mods:
            mods.append("shift")
        return key.lower()
    return key


def _dotool_actions_for_chord(chord: str) -> list[str]:
    chord = chord.strip()
    if not chord:
        return []

    base, action, repeat = _parse_suffix(chord)
    mods, key = _split_modifiers(base)
    key = _normalize_alpha_key(key, mods)
    key = _normalize_key_name(key)

    if not key:
        return _mods_only_actions(mods)

    chord_str = _build_chord(mods, key)
    if action != "key":
        return [f"{action} {chord_str}"]
    if repeat <= 1:
        return [f"key {chord_str}"]
    return [f"key {chord_str}" for _ in range(repeat)]


def _talon_key_to_dotool_actions(key_spec: str) -> list[str]:
    # Split sequences like "ctrl-, ctrl-f" into dotool actions.
    return [
        action
        for chord in key_spec.split()
        for action in _dotool_actions_for_chord(chord)
    ]


@ctx.action_class("main")
class MainActions:
    @staticmethod
    def key(key: str):
        print(f"sublime key: {key!r}", file=sys.stderr, flush=True)
        try:
            actions = _talon_key_to_dotool_actions(key)
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
