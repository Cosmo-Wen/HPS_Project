""" This module senses whether the can is full.

By checking distances and analyzing the data, we can determine whether the 
trash can is full by eliminating distances too large and too small. 

Typical usage:
sensor = Is_Full(DEPTH_SENSOR1_TRIG, DEPTH_SENSOR1_ECHO)
"""

import asyncio
import numpy as np
import time

import RPi.GPIO as GPIO

from .header import *

class IsFull:
    """ Creates an instance of detecting whether the can is full.

    This is done by checking for distance from a sensor and making logic
    operations. If the distance is too small or too abnormally large, the
    can is full.

    Attributes:
        trigger: ultrasonic trigger pin
        echo: utrasonic echo pin
    """

    def __init__(self, trig_pin: int, echo_pin: int) -> None:
        """ Set up required GPIO.

        Args: 
            trig_pin: Pin for pulse trigger
            echo_pin: Pin for detecting returning echo

        Returns: None

        Raises: None
        """

        self._trigger = trig_pin
        self._echo = echo_pin
        GPIO.setmode(GPIO.BCM)

    async def check_distance(self) -> None:        
        """ Triggering the ultrasonic modules and calculating the distance.

        This function detects the distance and parse the data into a number 
        between 3 and 21.

        Args: None

        Returns:
            distance: distance detected by the module

        Raises: None
        """

        GPIO.setup(self._trigger, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self._echo, GPIO.IN)
        GPIO.output(self._trigger, GPIO.HIGH)
        time.sleep(0.00015)
        GPIO.output(self._trigger, GPIO.LOW)

        while not GPIO.input(self._echo):
            pass
        t1 = asyncio.get_event_loop().time()

        while GPIO.input(self._echo):
            pass
        t2 = asyncio.get_event_loop().time()

        distance = (t2 - t1) * 340 * 100 / 2

        if distance < 3:
            distance = 3
        elif distance > 21:
            distance = AVOID_FULL - 0.5

        await asyncio.sleep(0.1)

        return distance

    async def get_distance(self) -> None:
        """ Retrieve multiple distances and returns the mean.

        Args: None

        Returns:
            distance: mean of the multiple distances

        Raises: None
        """

        distances = [await self.check_distance() for i in range(DEPTH_SAMPLE)]
        
        return np.mean(distances)
    
    async def is_trash_can_full(self) -> bool:
        """ If the distance is below the threshold, return true.

        Args: None

        Returns:
            True/False: whether the trash can is full

        Raises: None
        """

        distance = await self.get_distance()

        if distance is not None:
            if distance < AVOID_FULL:
                return True
            else:
                return False
        else:
            return False
    
    def shutdown(self):
        GPIO.cleanup()     
        
async def detect_full(sensor1: IsFull, sensor2: IsFull) -> None:
    """ This function combines the result of the two sensors and returns

    By testing whether the sensor is full for two sensors, we get a more  
    accurate result.

    Args: 
        sensor1: first sensor of type IsFull
        sensor2: second sensor of type IsFull

    Returns:
        True/False: AND of both sensor testing for fullness

    Raises: None
    """

    if (
        await sensor1.is_trash_can_full() 
        and await sensor2.is_trash_can_full()
    ):
        return True
    else:
        return False