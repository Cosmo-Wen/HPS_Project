""" Provides a module that controls the mechanisms of the lid.

This module is controls the lid opening and closing of the lid and the LED 
light embedded on said lid. This includes turning on and off, shutting down,
and separately detecting the trash overflow situation.

Typical usage:
lid = Lid()
lid.turn_on()/turn_off()
lid.sense()
"""

import asyncio

import RPi.GPIO as GPIO

from .header import *
from .is_full import IsFull, detect_full

class Lid:
    """ Controls opening the lid and showing the fullness when the can is full.

    The lid control involves setting up a detection object regarding fullness. 
    Other than that, the module uses asyncio events to gate the detection and 
    opening mechanism. When the detection mechanism receives data less than 10
    centimeters, the lid will open by sending a signal to the servo. 

    Attributes:
        flag: To signify continuous presence
        sense_event: Whether to turn on and off the feature
        pwm: Servo pin for pulse width modulation
    """

    def __init__(self) -> None:
        """ Set up all the pins and events

        Args: None
        """

        self._flag = False
        self._sense_event = asyncio.Event()
        self._sense_event.clear()

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(LID_TRIG, GPIO.OUT)
        GPIO.setup(LID_ECHO, GPIO.IN)
        GPIO.setup(LID_SERVO, GPIO.OUT)
        GPIO.setup(DEPTH_LED, GPIO.OUT)

        self._pwm = GPIO.PWM(LID_SERVO, 50)
        self._pwm.start(4)
    
    def turn_on(self) -> None:
        """ Turns on the detection.

        Using asyncio Events, this is possible asynchronously.

        Args: None

        Returns: None

        Raises: None
        """

        self._sense_event.set()
    
    def turn_off(self) -> None:
        """ Turns off the detection.

        Using asyncio Events, this is possible asynchronously.

        Args: None

        Returns: None

        Raises: None
        """

        self._sense_event.clear()
    
    def shutdown(self) -> None:
        """ Cleans GPIO, events, and PWM.

        Args: None

        Returns: None

        Raises: None
        """

        self._sense_event.clear()
        self._pwm.stop()
        GPIO.cleanup()

    async def sense(self) -> None:
        """ Controls the lid and the light regarding fullness.

        There are three sensors at work, one for the lid opening and two for
        depth detection. When the lid sensor returns a distance less than 10
        centimeter, the lid opes with servo control. Similarly, when the IsFull
        module returns true for whether the can is full, the LED turns on.

        Args: None

        Returns: None

        Raises: None
        """
        sensor1 = IsFull(DEPTH_SENSOR1_TRIG, DEPTH_SENSOR1_ECHO)
        sensor2 = IsFull(DEPTH_SENSOR2_TRIG, DEPTH_SENSOR2_ECHO)

        while True:
            await self._sense_event.wait()

            GPIO.output(LID_TRIG, GPIO.HIGH)
            await asyncio.sleep(0.00001)
            GPIO.output(LID_TRIG, GPIO.LOW)

            while GPIO.input(LID_ECHO) == 0:
                pulse_start_time = asyncio.get_event_loop().time()

            while GPIO.input(LID_ECHO) == 1:
                pulse_end_time = asyncio.get_event_loop().time()

            pulse_duration = pulse_end_time - pulse_start_time
            
            distance = round(pulse_duration * 17150, 2)

            if distance < 10:
                if not self._flag :
                    self._pwm.ChangeDutyCycle(7.5)
                    await asyncio.sleep(1)

                    full = await detect_full(sensor1, sensor2)

                    if full:
                        GPIO.output(DEPTH_LED, GPIO.HIGH)
                    else: 
                        GPIO.output(DEPTH_LED, GPIO.LOW)
                    await asyncio.sleep(5)

                    self._pwm.ChangeDutyCycle(4)
                    await asyncio.sleep(1)
                
                self._flag = True
            else:
                self._flag = False

            await asyncio.sleep(1)
