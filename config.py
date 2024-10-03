from collections import namedtuple

import colors

Position = namedtuple('Position', ['x', 'y'])
Size = namedtuple('Size', ['width', 'height'])

# CANVAS
SCREEN_RESOLUTION = Size(1280, 720)
FULLSCREEN = False
BACKGROUND_COLOR = colors.BLACK
TITLE = 'Conway\'s Game of Life'

# TILE
TILE_SIZE = Size(10, 10)

DEAD_TILE_COLOR = colors.PEONY
LIVING_TILE_COLOR = colors.GARDENIA
DYING_TILE_COLOR = colors.CROCUS
LIVE_TILE_COLOR = colors.HEATHER

# GRID LINES
GRID_LINE_THICKNESS = 0
GRID_LINE_COLOR = colors.TWILIGHT

# FPS
FPS_COUNTER_ENABLED = False
FPS = 60
FPS_COUNTER_FONT = 'consolas'
FPS_COUNTER_SIZE = 20
FPS_COUNTER_COLOR = colors.PASTEL_LIGHT_BLUE
FPS_COUNTER_POSITION = Position(10, 10)