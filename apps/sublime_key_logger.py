"""Sublime-only Talon key translation via dotool.

Format:
- Input key spec: space-separated chords like "ctrl-, ctrl-f".
- Chord: modifiers joined by "-" plus a key name (e.g., "super-1").
- Suffixes: ":down", ":up", or ":N" for repeats.
- Output: dotool action lines like "key ctrl+f".
"""

from talon import Context
import subprocess
import sys

from .keymap_dotool import KEY_NAME_MAP, MODIFIER_ALIASES, SYMBOL_KEY_MAP

KeySpec = str
DotoolAction = str
DotoolActions = list[DotoolAction]


ctx = Context()
ctx.matches = r"""
app: Sublime Text
app: Sublime Text 4
app: Sublime Text 3
app: sublime_text
"""


def _normalize_key_name(key: str) -> str:
    """Normalize a Talon key name to a dotool-compatible name.

    Args:
        key: Talon key name or symbol.

    Returns:
        Dotool-compatible key name, possibly with x:/k: prefix.
    """
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


def _split_modifiers(chord: str) -> tuple[tuple[str, ...], str]:
    """Split a chord into modifiers and the base key.

    Args:
        chord: Talon chord string like "ctrl-shift-a".

    Returns:
        Tuple of (modifiers, key) where modifiers is a tuple.
    """
    parts = chord.split("-")
    mods: list[str] = []
    key_parts: list[str] = []
    for part in parts:
        if not key_parts and part in MODIFIER_ALIASES:
            mods.append(MODIFIER_ALIASES[part])
        else:
            key_parts.append(part)
    return tuple(mods), "-".join(key_parts)


def _build_chord(mods: tuple[str, ...], key: str) -> str:
    """Build a dotool chord string from modifiers and a key.

    Args:
        mods: Modifier tuple.
        key: Normalized key name.

    Returns:
        Dotool chord string like "ctrl+shift+a".
    """
    parts = list(mods)
    if key:
        parts.append(key)
    return "+".join(parts)


def _mods_only_actions(mods: tuple[str, ...]) -> DotoolActions:
    """Emit down/up actions for modifier-only chords.

    Args:
        mods: Modifier tuple.

    Returns:
        Dotool actions to press and release the modifiers.
    """
    if not mods:
        return []
    actions = [f"keydown {mod}" for mod in mods]
    actions.extend(f"keyup {mod}" for mod in reversed(mods))
    return actions


def _parse_suffix(chord: str) -> tuple[str, str, int]:
    """Parse :down/:up or :N suffixes for a chord.

    Args:
        chord: Talon chord string, possibly with a suffix.

    Returns:
        Tuple of (base_chord, action, repeat).
    """
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


def _normalize_alpha_key(key: str, mods: tuple[str, ...]) -> tuple[tuple[str, ...], str]:
    """Normalize single-letter uppercase keys without mutating inputs.

    Args:
        key: Single key string.
        mods: Modifier tuple.

    Returns:
        Tuple of (mods, key) with shift added if needed.
    """
    if key and len(key) == 1 and key.isalpha() and key.isupper():
        if "shift" in mods:
            return mods, key.lower()
        return mods + ("shift",), key.lower()
    return mods, key


def _dotool_actions_for_chord(chord: str) -> DotoolActions:
    """Convert a single Talon chord to dotool actions.

    Args:
        chord: Talon chord string, e.g. "ctrl-a" or "esc:2".

    Returns:
        List of dotool action lines.
    """
    chord = chord.strip()
    if not chord:
        return []

    base, action, repeat = _parse_suffix(chord)
    mods, key = _split_modifiers(base)
    mods, key = _normalize_alpha_key(key, mods)
    key = _normalize_key_name(key)

    if not key:
        return _mods_only_actions(mods)

    chord_str = _build_chord(mods, key)
    if action != "key":
        return [f"{action} {chord_str}"]
    if repeat <= 1:
        return [f"key {chord_str}"]
    return [f"key {chord_str}" for _ in range(repeat)]


def _talon_key_to_dotool_actions(key_spec: KeySpec) -> DotoolActions:
    """Convert a Talon key spec into dotool actions.

    Args:
        key_spec: Talon key spec with space-separated chords.

    Returns:
        List of dotool action lines.
    """
    return [
        action
        for chord in key_spec.split()
        for action in _dotool_actions_for_chord(chord)
    ]


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
