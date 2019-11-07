import string



# network 0: N nodes constantly throughout all time steps for the entire simulation
N = 2#100 # number of nodes in the network


# network 1: N nodes come in and out randomly over the time steps of the simulation
# N = 100

R = 33 # max signal radius of each node
SIGNAL_SPEED = 3.5 # how far the signal travels per second
PING_FREQUENCY = 0.5 # number of pings per second

# coordinate range of 2D rectangular map
X_MIN, X_MAX = 0.00, 30.00
Y_MIN, Y_MAX = 0.00, 30.00

# coordinate range of 3D globe
# pass

ALL_CHARS = ''.join(set(string.printable) - set(string.whitespace)) # all printable characters except white space
# source: https://docs.python.org/3/library/string.html




SCREEN_SCALE = 15.0 # 5x as big as coordinate range of 2D rectangular map
# SCREEN_SIZE = (750, 500)
SCREEN_SIZE = (
	int(SCREEN_SCALE * (X_MAX - X_MIN)),
	int(SCREEN_SCALE * (Y_MAX - Y_MIN))
)

OUTPUT_FRAME_RATE = False

CONTROL_KEY = [
	"Keyboard Controls:",
	"	<space> = Pause/Play",
	"	v = Toggle view drawing",
	"	k = Toggle Control Key",
]

