import math
import string




# # random network: specified number of sub-networks with a specified number of nodes constantly throughout all time steps for the entire simulation
# SUB_NETWORKS = [
#     20
# ] # NETWORKS = list of number of nodes in each sub network (fully connected), len(NETWORKS) = number of networks
# N = sum(NETWORKS) # number of nodes in the network
# R = 5 # max signal radius of each node
# # coordinate range of 2D rectangular map
# X_MIN, X_MAX = 0.00, 25.00
# Y_MIN, Y_MAX = 0.00, 25.00
# NODE_POSITIONS =
#     nodes = [Node(0, 0)]
#     n0 = nodes[0]
#     while num_nodes in NETWORKS:
#         # create starting node n0 at a position (0, 0)
#         # pick a random distance from .05*R to R
#         # pick a random direction from 0 to 2*math.pi
#         # create a node that direction and distance away from the previous node created
#         #     (verify its inbounds w/ no coordinate wrap around)
#         # n0 = n



# SCREEN_SCALE = 15.0 # make SCREENSIZE SCREEN_SCALE times as big as coordinate range of 2D rectangular map

# grid network: N nodes at each point in a W by H grid, N=W*H, R = dist so neighbors in grid are neighbors in network
W = 20 # width of grid
H = 20 # height of grid
N = W * H # number of nodes in the network
R = 1 * math.sqrt(2) # max signal radius of each node
# coordinate range of 2D rectangular map
X_MIN, X_MAX = 0.00, float(W)
Y_MIN, Y_MAX = 0.00, float(H)
SCREEN_SCALE = 20.0 # make SCREENSIZE SCREEN_SCALE times as big as coordinate range of 2D rectangular map

SCREEN_SIZE = (
    int(SCREEN_SCALE * (X_MAX - X_MIN)),
    int(SCREEN_SCALE * (Y_MAX - Y_MIN))
)


SIGNAL_SPEED = 3.5 # how far the signal travels per second
PING_FREQUENCY = 0.5 # number of pings per second


# coordinate range of 3D globe
# pass

ALL_CHARS = ''.join(set(string.printable) - set(string.whitespace)) # all printable characters except white space
# source: https://docs.python.org/3/library/string.html





OUTPUT_FRAME_RATE = False

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

