""" This module governs the basic movements of the motor.

By configuring the speed of left and right wheel speed, multiple maneuvers
are possible and listed as class methods.

Typical usage:
move = Directions()
move.F_30()
...
"""

import asyncio
import getch
import time

from gpiozero import Robot

from .header import *

class Directions:
    """ Controls the motor function of the wheels.

    By invoking the Robot module provided by gpiozero, we can control the 
    movement of the two pins separately. 

    Attributes:
        robot: the object for controlling 4 set of pins representing two wheels
    """

    def __init__(self) -> None:
        """ Setting up the robot object.

        Args: None

        Returns: None

        Raises: None
        """
    
        self._robot = Robot(
            left=(MOTOR_LEFT_PIN1, MOTOR_LEFT_PIN2), 
            right=(MOTOR_RIGHT_PIN1, MOTOR_RIGHT_PIN2)
        )

    def stop(self) -> None:
        """ Stops the wheels completely.

        Args: None

        Returns: None

        Raises: None
        """

        self._robot.stop()

    def move(self, speed_left: float, speed_right: float) -> None:
        """ Move the wheels depending on the arguements.

        Args: 
            speed_left: the speed for the left wheels
            speed_right: the speed for the right wheels

        Returns: None

        Raises: None
        """

        self._robot.value = (speed_left, speed_right)

    async def F_L(self) -> None:
        """Move forward a little.

        Args: None

        Returns: None

        Raises: None
        """

        self.move(0.45, 0.45)
        await asyncio.sleep(0.1)
        self._robot.stop()
        await asyncio.sleep(0.1)

    async def F_30(self) -> None:
        """Move forward 30cm.

        Args: None

        Returns: None

        Raises: None
        """

        self.move(0.45, 0.45)
        await asyncio.sleep(0.85)
        self._robot.stop()
        await asyncio.sleep(0.1)

    def B(self) -> None:
        """Move backwards.

        Args: None

        Returns: None

        Raises: None
        """

        self.move(speed_left = - MOTOR_BASE_SPEED, speed_right = - MOTOR_BASE_SPEED + 0.1)

    async def B_15(self) -> None:
        """Move backwards 15cm.

        Args: None

        Returns: None

        Raises: None
        """

        self.move( -0.4, speed_right=-0.3)
        await asyncio.sleep(0.01)
        self._robot.stop()

    async def L_180(self) -> None:
        """Turn towards the left by 180 degrees.

        Args: None

        Returns: None

        Raises: None
        """

        self._robot.value = (-0.6, 0.7)
        await asyncio.sleep(0.5)
        self._robot.value = (-0.3,0.4)
        await asyncio.sleep(0.4)
        self._robot.stop()

    async def L_90(self) -> None:
        """Turn towards the left by 90 degrees.

        Args: None

        Returns: None

        Raises: None
        """

        self._robot.value = (-0.6, 0.6)
        await asyncio.sleep(0.28)
        self._robot.value = (-0.4,0.4)
        await asyncio.sleep(0.2)
        self._robot.stop()

    async def L_30(self) -> None:
        """Turn towards the left by 30 degrees.

        Args: None

        Returns: None

        Raises: None
        """

        self._robot.value = (-0.5, 0.5)
        await asyncio.sleep(0.18)
        self._robot.stop()
        await asyncio.sleep(0.1)

    async def R_180(self) -> None:
        """Turn towards the right by 180 degrees.

        Args: None

        Returns: None

        Raises: None
        """

        self._robot.value = (0.7,-0.6)
        await asyncio.sleep(0.5)
        self._robot.value = (0.4,-0.3)
        await asyncio.sleep(0.45)
        self._robot.stop()
        await asyncio.sleep(1)

    async def R_90(self) -> None:
        """Turn towards the right by 90 degrees.

        Args: None

        Returns: None

        Raises: None
        """

        self._robot.value = (0.6,-0.6)
        await asyncio.sleep(0.28)
        self._robot.value = (0.4,-0.4)
        await asyncio.sleep(0.2)
        self._robot.stop()

    async def R_30(self) -> None:
        """Turn towards the right by 30 degrees.

        Args: None

        Returns: None

        Raises: None
        """

        self._robot.value = (0.5,-0.5)
        await asyncio.sleep(0.2) 
        self._robot.stop()
        await asyncio.sleep(0.1)

    async def R_30_round(self, num: int) -> None:
        """Turn towards the right by 30 degrees multiple times.

        Args: None

        Returns: None

        Raises: None
        """

        for i in range(num):
            await self.R_30()

    async def L_30_round(self, num: int) -> None:
        """Turn towards the left by 30 degrees multiple times.

        Args: None

        Returns: None

        Raises: None
        """

        for i in range(num):
            await self.L_30()

    async def F_30_round(self, num: int) -> None:
        """Move forward by 30cm multiple times.

        Args: None

        Returns: None

        Raises: None
        """

        for i in range(num):
            await self.F_30()
    
    def shutdown(self) -> None:
        """ Cleans robot.

        Args: None

        Returns: None

        Raises: None
        """

        self._robot.stop()