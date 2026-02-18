-
enter: key(enter)

switch:
	user.mouse_toggle_control_mouse()
	user.mouse_toggle_zoom_mouse()

snore:
	speech.disable()
	app.notify("Talon Sleep")

parrot(tut):
	print("tut again")
	user.play_beep()
	core.repeat_command(1)

dredge: key(alt-tab)

#	KinesicMouse
pause | ram: key(alt-1)
center: key(alt-2)

#basic: key(shift-alt-1)
#mouse: key(shift-alt-2)
#scroll: key(shift-alt-3)
#test: key(shift-alt-4)


# Function key hotkeyb mappings

# key(f15): bcore.repeat_phrase(1)

#	Stream Deck
key(f2): speech.toggle() 
# alt gr options: altgr | alt-gr | ralt | ctrl-alt
# right super options: rwin | rsuper | super-r
# menu key (right of super): menu
# right ctrl options: rctrl | ctrl-r
