""" This module switches between moving to target and avoiding obstacles

This module contains the code for controlling a robot's movement and obstacle
avoidance using ultrasonic sensors and UWB positioning.

Typical usage: 
move = Move()
move.move()
"""

import asyncio
import time
import math

from gpiozero import Robot
from gpiozero.pins.rpigpio import RPiGPIOFactory
import RPi.GPIO as GPIO

from .directions import *
from .header import *
from .serial_capture import UWB3000Serial

class Move():
    """ The Move class manages the robot's movement behavior.

    By calculating the distance with UWB on multiple occasions, the program 
    can figure out the distance and direction it should be going. Moving in 
    segments allows for it to avoid obstacles in its path.

    Attributes:
        ser: serial UWB module
        direction: movement function class object
        front_distance: distance from the front to an obstacle
        left_distance: distance from the left to an obstacle
        right_distance: distance from the right to an obstacle
    """

    def __init__(self) -> None: 
        """ Initialized required setup for Move

        The required setup work include GPIOFactory, GPIO, UBW serial input,
        and a direction instance. 

        Args: None
        """

        pin_factory = RPiGPIOFactory()

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(AVOID_FRONT_TRIG, GPIO.OUT)
        GPIO.setup(AVOID_FRONT_ECHO, GPIO.IN)
        GPIO.setup(AVOID_LEFT_TRIG, GPIO.OUT)
        GPIO.setup(AVOID_LEFT_ECHO, GPIO.IN)
        GPIO.setup(AVOID_RIGHT_TRIG, GPIO.OUT)
        GPIO.setup(AVOID_RIGHT_ECHO, GPIO.IN)

        self._ser = UWB3000Serial('/dev/ttyUSB0', 115200)
        self._ser.reset_input_buffer()

        self._direction = Directions()
        
        self._front_distance = 100000
        self._left_distance = 100000
        self._right_distance = 100000

    def measure_distance(self, trigger_pin: int, echo_pin: int) -> None:
        """ Measures the distance to the nearest object

        By using an ultrasonic module, the distance could be calculated. The 
        data is also limited to a max distance for ease of processing.

        Args: 
            trigger_pin: pin for triggering a pulse
            echo_pin: pin for receiving the echo

        Returns:
            distance: minimum between the detected distance and the max allowed

        Raises: None
        """

        GPIO.output(trigger_pin, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(trigger_pin, GPIO.LOW)

        while GPIO.input(echo_pin) == GPIO.LOW:
            pass
        pulse_start = asyncio.get_event_loop().time()

        while GPIO.input(echo_pin) == GPIO.HIGH:
            pass
        pulse_end = asyncio.get_event_loop().time()

        pulse_duration = pulse_end - pulse_start
        distance = (pulse_duration * 34300) / 2
        return min(distance, AVOID_MAX_DISTANCE)

    def update_distances(self) -> None:
        """ Updates the internal distance of three sides: front, left, right

        By calling individual measure distance and there corresponding pins, we
        can calculate the distances.

        Args: None

        Returns: None

        Raises: None
        """

        self._front_distance = self.measure_distance(
            AVOID_FRONT_TRIG, AVOID_FRONT_ECHO)
        self._left_distance = self.measure_distance(
            AVOID_LEFT_TRIG, AVOID_LEFT_ECHO)
        self._right_distance = self.measure_distance(
            AVOID_RIGHT_TRIG, AVOID_RIGHT_ECHO)
        
    def check_light(self) -> bool:
        """ Check if the distance to obstables are passable

        This is done by updating distance and checking with constants.

        Args: None

        Returns: 
            True/False: whether the distance is far enough

        Raises: None
        """
        
        self.update_distances()
        if (
            self._left_distance > AVOID_MAX_RL 
            and self._right_distance > AVOID_MAX_RL 
            and self._front_distance > AVOID_MAX_F
        ):
            return True
        else:
            return False

    async def Obstacle_avoidance(self) -> bool:
        """ Function-level comment: Performs obstacle avoidance.

        This method checks distances and adjusts the robot's direction to 
        avoid obstacles. This is done by a semi-greedy approach of testing 
        the angle of the least obstacles.

        Args: None

        Returns:
            True/False: whether the device moved to a location.

        Raises: None
        """

        Flag = False
        (i, j) = (0, 0)
        self.update_distances()
        
        if not self._check_light():
            if self._right_distance < self._left_distance:
                Flag = False
            else:
                Flag = True

            if Flag == False:
                for i in range(5):
                    self.update_distances()
                    if self.check_light():
                        await self._direction.F_30()
                        return True
                    else:
                        await self._direction.L_30()
                        await asyncio.sleep(0.5)

                if i == 4:
                    self.update_distances()
                    if self.check_light():
                        await self._direction.F_30()
                        return True
                    return False
            else:
                for j in range(5):
                    self.update_distances()
                    if self.check_light():
                        await self._direction.F_30()
                        return True
                    else:
                        await self._direction.R_30()
                        await asyncio.sleep(0.5)

                if j == 4:
                    self.update_distances()
                    if self.check_light():
                        await self._direction.F_30()
                        return True
                    return False

    def get_intersection(self, s1, s2, s3) -> (float, float):
        """Retrieve a relative distance and direction of the destination

        Math.

        Args: 
            s1/s2/s3: sensor data number

        Returns:
            (x, y): relative coordinate of the destination
        
        Raises: None
        """

        x = (s3 ** 2 - s1 ** 2) / (4 * MOTOR_ROTATE_RADIUS)
        y = (s3 ** 2 + s1 ** 2) / 2 - MOTOR_ROTATE_RADIUS ** 2 - x ** 2
        y = 0 if y < 0 else math.sqrt(y)

        error1 = abs(math.sqrt(x ** 2 + (MOTOR_ROTATE_RADIUS - y) ** 2) - s2)
        error2 = abs(math.sqrt(x ** 2 + (MOTOR_ROTATE_RADIUS + y) ** 2) - s2)

        return (x,y) if error1 < error2 else (x,-y)

    def angle_count(self, angle) -> int:
        """ Amount of spins to get to an angle.

        Since a spin is 30 degrees, the amount of spins is angle / 30.

        Args:
            angle: target angle
        
        Returns:
            angle / 30: number of spins
        
        Raises: None
        """

        return int(angle / 30)

    def distance_count(self, dis) -> int:
        """ Amount of moves to get to an distance.

        Since a moves is 30 centimeters, the amount of moves is dis / 30.

        Args:
            dis: target distance
        
        Returns:
            dis / 30: number of moves
        
        Raises: None
        """

        return int(dis / 30)

    async def find_direction(self) -> None:
        """ Retrieve data  and calculate the direction to move towards.

        From the UBW module, retrieve the data three times at different angles.
        Then, with the data, calculate the coordinate of the destination. From
        the coordinate, we can retrieve the angle and direction towards the 
        destination.

        Args: None

        Returns: 
            distance: the target distance
            angle: the target angle
        
        Raises: None
        """

        await asyncio.sleep(2)
        s1 = self._ser.read_distance()
        await self._direction.L_90()
        
        await asyncio.sleep(2)
        s2 = self._ser.read_distance()
        # rotate 90 逆時針
        await self._direction.L_90()
        
        await asyncio.sleep(2)
        s3 = self._ser.read_distance()
        
        
        
        target_coordinate = self.get_intersection(s1, s2, s3)

        distance = math.sqrt(
            target_coordinate[0] ** 2 + target_coordinate[1] ** 2)
        angle = math.degrees(
            math.atan2(target_coordinate[1], target_coordinate[0]))

        return distance, angle

    async def A_B(self) -> bool:
        """ Moves from start to end only if no obstacles in area

        Incorperates the other class functions to find the distance and
        direction. After than, move steadily until target reached or 
        insufficient space due to obstacles.

        Args: None

        Returns:
            True/False: Destination met

        Raises: None
        """
        
        await asyncio.sleep(1)

        while True:
            distance = float(self._ser.read_distance())
            
            if distance <= MOTOR_STOP_RADIUS:
                break
            else:
                distance, angle = await self.find_direction()

                if angle < 0: 
                    angle = 180 + angle
                    await self._direction.L_30_round(self.angle_count(angle))
                else:
                    angle = 180 - angle
                    await self._direction.R_30_round(self.angle_count(angle))
                
                distance_to_go = min(
                    MOTOR_MAX_TRAVEL_DIST, 
                    MOTOR_FORWARD * math.ceil(0.5 * distance / MOTOR_FORWARD))
                self.update_distances()
                for i in range(self.distance_count(distance_to_go)):
                    self.update_distances()
                    if (
                        self._left_distance > 30 
                        and self._right_distance > 30 
                        and self._front_distance > 30
                    ):
                        await self._direction.F_30()
                    elif distance <= MOTOR_STOP_RADIUS:
                        return True
                    elif (
                        self._left_distance > 20 
                        or self._right_distance > 20 
                        or self._front_distance > 20
                    ):
                        await self._direction.F_L()
                        return False
                    else:
                        return False
        return True

    async def move(self):
        """ Executes the instruction move, including avoiding obstacles.

        Args: None

        Returns: None

        Raises: None
        """
    
        while True:
            Flag = await self.A_B()
            if not Flag:
                Flag=await self.Obstacle_avoidance()
            else:
                break

    def shutdown(self):
        """Clean up.

        Only direction requires internalc clean up.
        
        Args: None

        Returns: None

        Raises: None
        """
        
        self._direction.shutdown()
