# Pixels per unit of distance in the plan view with the default view
# TODO: refactor visuals so this isn't needed (currently it prevents distortion, as the
#       default visual size would be really small for the typical unit sizes we're
#       working with)
PIXELS_PER_DISTANCE_UNIT = 200

# Editor width as a proportion of the screen
EDITOR_WIDTH = 0.33
# How light the grey background of the editor should be
EDITOR_BACKGROUND_BRIGHTNESS = 0.85

# Pixels of padding between elements displayed in the editor
EDITOR_PADDING = 2
EDITOR_TEXT_PADDING = 1
EDITOR_TEXT_SIZE = 15
EDITOR_BED_INDENT = 25

# Colours
EDITOR_BLOCK_COLOUR = (0.7,) * 3
EDITOR_BACKGROUND_COLOUR = (0.9,) * 3

# Navigation
EDITOR_SCROLL_SPEED = 75.0

# Seems the mouse's click position can sometimes get out of sync with its integrated
# position - when enabled, this will check whether that is the case at each click event
VALIDATE_MOUSE_POSITION = False
