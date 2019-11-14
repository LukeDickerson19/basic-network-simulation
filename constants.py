import math
import string




# # TODO: static network
# GRID = True # flag to put the nodes in a grid or not
# SUB_NETWORKS = [
#     2,
#     5,
#     1,
#     9
# ] # list of number of nodes in each sub network (fully connected), len(NETWORKS) = number of networks
# N = sum(SUB_NETWORKS)
# SCREEN_SCALE = 10.0 # make SCREENSIZE SCREEN_SCALE times as big as coordinate range of 2D rectangular map
# SCREEN_SIZE = (
#     int(SCREEN_SCALE * W),
#     int(SCREEN_SCALE * H)
# )


# VARIABLE NETWORK
W = 20 # width of model's 2D map
H = 20 # height of model's 2D map
N_MIN, N_MAX = 10, 20 # min/max number of devices on the map at any point in time
AVG_VEL = 0.01 # average velocity of a device
STD_DEV_VEL = 0.001 # standard deviation of device velocity
MAX_VEL = AVG_VEL + 3*STD_DEV_VEL # max device velocity
MIN_VEL = AVG_VEL - 3*STD_DEV_VEL # min device velocity
MIN_VEL = max(MIN_VEL, 0.00001) # ensure MIN_VEL is always positive
MAX_DST_DIST = 0.01 # max distance from device to destination that qualifies as reaching the destination
R = 5.0 # signal radius range of a device to connect to other devices (to send/receive messages)
SCREEN_SCALE = 25.0 # pixels per unit, aka make the SCREENSIZE SCREEN_SCALE times as big as coordinate range of the 2D map
SCREEN_SIZE = (
    int(SCREEN_SCALE * W),
    int(SCREEN_SCALE * H)
) # pixel dimentions of display screen



SIGNAL_SPEED = 2.5#6.5 # how far the signal travels per second (make sure this is faster than MAX_VEL)
PING_FREQUENCY = 0.20#0.33 # number of pings per second

# Python Color Constants Module
# https://www.webucator.com/blog/2015/03/python-color-constants-module/
_ping = 'red'
_echo = 'green'
_message = 'blue'
BACKGROUND_COLOR = 'black'
NODE_DEFAULT_COLOR = 'white'
NODE_PING_COLOR = _ping
NODE_ECHO_COLOR = _echo
NODE_MESSAGE_COLOR = _message
SIGNAL_PING_COLOR = 'dark' + _ping
SIGNAL_ECHO_COLOR = 'dark' + _echo
SIGNAL_MESSAGE_COLOR = _message
DOT_PING_COLOR = _ping
DOT_ECHO_COLOR = _echo
DOT_MESSAGE_COLOR = _message
CONNECTION_COLOR = 'white'
SELECTED_DEVICE_COLOR = 'gray8' #(20, 20, 20)


SIGNAL_RING_THICKNESS = 3

ALL_CHARS = ''.join(set(string.printable) - set(string.whitespace)) # all printable characters except white space, used for key creation
# source: https://docs.python.org/3/library/string.html





OUTPUT_FRAME_RATE = False # flag if we want to print the frame rate to the console

CONTROL_KEY = [
	"Keyboard Controls:",
	"	<space> = Pause/Play",
	"	v = Toggle view drawing",
	"	k = Toggle Control Key",
]



# CELLULAR AUTOMATA
AUTOMATA_PERIOD = 0.15 # period of time (in seconds) that a turn lasts

# 1D cellular automata
# https://github.com/ogham/mindless-automata

# BOIDS
# https://medium.com/@lady_shapes/cellular-automata-76dd6ff25173
# https://github.com/alanmacleod/autocell

# Conway's Game of Life:
# https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life
def place_at(x, y, pattern):

    return [(pos[0] + x, pos[1] + y) for pos in pattern]

# automata_still_lifes
BLOCK = [
    (0, 1), (1, 1),
    (0, 0), (1, 0)
]

# automata_oscillators
BLINKER = [(0, 0), (1, 0), (2, 0)]
TOAD = BLINKER + place_at(1, 1, BLINKER)
BEACON = BLOCK + place_at(2, 2, BLOCK)

# automata_spaceships
GLIDER = BLINKER + [(2, 1), (1, 2)]



# Forest Fire:
# https://en.wikipedia.org/wiki/Forest-fire_model
F = 0.05 # A tree ignites with probability F even if no neighbor is burning
P = 0.75 # An empty space fills with a tree with probability p

# All:
AUTOMATA_START_POSITIONS = {
    'blank'      : [],
    'one_center' : [(int(W / 2), int(H / 2))],
    'blinker'    : place_at(int(W / 2), int(H / 2), BLINKER),
    'toad'       : place_at(int(W / 2), int(H / 2), TOAD),
    'beacon'     : place_at(int(W / 2), int(H / 2), BEACON),
    'glider'     : place_at(int(W / 2), int(H / 2), GLIDER)
}

