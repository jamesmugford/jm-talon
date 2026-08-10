# jamesmugford-talon

## OBS recording

The `record mode` command enters `user.record`. While that mode is active,
`record toggle` toggles OBS recording and then plays a confirmation sound.
`command mode` and `mixed mode` leave record mode without changing OBS.

This integration requires:

- OBS Studio's authenticated WebSocket server on port 4455.
- `gobs-cli` configured to connect to `127.0.0.1`.
- Connection settings in `~/.config/gobs-cli/config.env`, outside this
  repository.
