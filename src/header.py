from enum import Enum, auto

# CONSTANTS
# Lid Control
LID_TRIG = 4
LID_ECHO = 17
LID_SERVO = 18

# Avoid Obstacles
AVOID_FRONT_TRIG = 5
AVOID_FRONT_ECHO = 6
AVOID_LEFT_TRIG = 13
AVOID_LEFT_ECHO = 19
AVOID_RIGHT_TRIG = 24
AVOID_RIGHT_ECHO = 25

AVOID_MAX_DISTANCE = 100 # Unit: cm
AVOID_MAX_RL = 20 # Unit: cm
AVOID_MAX_F = 23 # Unit: cm 
AVOID_FULL = 9 # Unit: cm
BBB = 12 # Beep Beep Beep 

# Movement Control
MOTOR_LEFT_PIN1 = 9
MOTOR_LEFT_PIN2 = 10
MOTOR_RIGHT_PIN1 = 7
MOTOR_RIGHT_PIN2 = 8

MOTOR_BASE_SPEED = 0.6
MOTOR_FORWARD = 30 # Unit: cm
MOTOR_TURN_DEG = 30 # Unit: deg
MOTOR_STOP_RADIUS = 50 # Unit: cm
MOTOR_ROTATE_RADIUS = 10 # Unit: cm
MOTOR_MAX_TRAVEL_DIST = 150 # Unit: cm

# Depth detection
DEPTH_SENSOR1_TRIG = 20 
DEPTH_SENSOR1_ECHO = 21
DEPTH_SENSOR2_TRIG = 22
DEPTH_SENSOR2_ECHO = 23
DEPTH_LED = 2

DEPTH_SAMPLE = 10 # Unit: #

# Enumerator classes
class Instructions(Enum):
    START = auto()
    END = auto()
    MOVE = auto()
    RETURN = auto()
    INVALID = auto()
    LOG = auto()

class States(Enum):
    IDLE = auto()
    ONLINE = auto()
    INVALID = auto()

class Actions(Enum):
    NOTHING = auto()
    HALT = auto()
    INVALID = auto()