# constants that go in the making of the grid used for the snake's movment
GRADUATION = 30
PIXEL = 10
STEP = 2 * PIXEL
WD = PIXEL * GRADUATION
HT = PIXEL * GRADUATION
CELLS = int(WD / STEP)
# constants that go into specifying the shapes' sizes
OB_SIZE_FACTOR = 0.8
SN_SIZE_FACTOR = 0.9
OB_SIZE = PIXEL * OB_SIZE_FACTOR
SN_SIZE = PIXEL * SN_SIZE_FACTOR
VO_SIZE = PIXEL * SN_SIZE_FACTOR
# color constants
BG_COLOR = 'black'
OB_COLOR = 'green'
SN_COLOR = 'white'
VO_COLOR = 'blue'
# a dictionary to ease access to a shape's type in the Shape class
SN = 'snake'
OB = 'obstacle'
OV = "visited"
SIZE = {SN: SN_SIZE, OB: OB_SIZE, OV: VO_SIZE}
# constants for keyboard input
UP = 'Up'
DOWN = 'Down'
RIGHT = 'Right'
LEFT = 'Left'
# a dictionary to ease access to 'directions'
DIRECTIONS = {UP: [0, -1], DOWN: [0, 1], RIGHT: [1, 0], LEFT: [-1, 0]}
AXES = {UP: 'Vertical', DOWN: 'Vertical',
        RIGHT: 'Horizontal', LEFT: 'Horizontal'}
# refresh time for the perpetual motion
REFRESH_TIME = 350
# number of food objects
FOOD = 3
