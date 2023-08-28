from enum import Enum, auto

# CONSTANTS
LID_TRIG = 7
LID_ECHO = 11
LID_SERVO = 12

MOTOR_FRONT_TRIG = 20
MOTOR_FRONT_ECHO = 21
MOTOR_LEFT_TRIG = 22
MOTOR_LEFT_ECHO = 23
MOTOR_RIGHT_TRIG = 24
MOTOR_RIGHT_ECHO = 25

MOTOR_FORWARD = 30 # Unit: cm
MOTOR_TURN_DEG = 30 # Unit: deg
MOTOR_STOP_RADIUS = 50 # Unit: cm
MOTOR_ROTATE_RADIUS = 10 # Unit: cm
MOTOR_MAX_TRAVEL_DIST = 150 # Unit: cm

SONAR_MAX_DISTANCE = 100 # Unit: cm
BBB = 12
Turn = 0.1
MAX_D_RF = 20
MAX_F=23
MM_turn = 40

FULL = 9
SENSOR1_TRIGGER = 20
SENSOR1_ECHO = 21
SENSOR2_TRIGGER = 22
SENSOR2_ECHO = 23
ITERATIONS = 10

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