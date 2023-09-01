import asyncio
from gpiozero import Robot
import getch
import time

from .header import *

class Directions:
    def __init__(self):
        self._robot = Robot(left=(MOTOR_LEFT_PIN1, MOTOR_LEFT_PIN2), right=(MOTOR_RIGHT_PIN1, MOTOR_RIGHT_PIN2))

    def stop(self):
        self._robot.stop()

    def move(self, speed_left, speed_right):
        self._robot.value = (speed_left, speed_right)
        # time.sleep(0.7)
        # robot.stop()

    async def F_L(self):
        self.move(0.45, 0.45)
        await asyncio.sleep(0.1)
        self._robot.stop()
        await asyncio.sleep(0.1)

    async def F_30(self):
        self.move(0.45, 0.45)
        await asyncio.sleep(0.85)
        self._robot.stop()
        await asyncio.sleep(0.1)

    def B(self):
        self.move(speed_left = -MOTOR_BASE_SPEED, speed_right = -MOTOR_BASE_SPEED + 0.1)

    async def B_15(self):
        self.move( -0.4, speed_right=-0.3)
        await asyncio.sleep(0.01)
        self._robot.stop()

    async def L_180(self):
        self._robot.value = (-0.6, 0.7)
        await asyncio.sleep(0.5)
        self._robot.value = (-0.3,0.4)
        await asyncio.sleep(0.4)
        self._robot.stop()

    async def L_90(self):
        self._robot.value = (-0.6, 0.6)
        await asyncio.sleep(0.28)
        self._robot.value = (-0.4,0.4)
        await asyncio.sleep(0.2)
        self._robot.stop()

    async def L_30(self):
        self._robot.value = (-0.5, 0.5)
        await asyncio.sleep(0.18)
        self._robot.stop()
        await asyncio.sleep(0.1)

    async def R_180(self):
        self._robot.value = (0.7,-0.6)
        await asyncio.sleep(0.5)
        self._robot.value = (0.4,-0.3)
        await asyncio.sleep(0.45)
        self._robot.stop()
        await asyncio.sleep(1)

    async def R_90(self):
        self._robot.value = (0.6,-0.6)
        await asyncio.sleep(0.28)
        self._robot.value = (0.4,-0.4)
        await asyncio.sleep(0.2)
        self._robot.stop()

    async def R_30(self):
        self._robot.value = (0.5,-0.5)
        await asyncio.sleep(0.2) 
        self._robot.stop()
        await asyncio.sleep(0.1)

    async def R_30_round(self, num):
        for i in range(num):
            await self.R_30()

    async def L_30_round(self, num):
        for i in range(num):
            await self.L_30()

    async def F_30_round(self, num):
        for i in range(num):
            await self.F_30()
    
    def shutdown(self):
        self._robot.stop()

async def main():
    try: 
        print("Enter commands: 'w' for Backward, 's' for decelerate backward, 'a' for left, 'd' for right, 'x' to exit")
        move = Directions()
        while True:
            command = getch.getch()
            
            if command == 'x':
                move._robot.stop()
                break
            else:
                move._robot.stop()  # 先停止当前动作
                if command == 'w':
                    await move.F_L()
                elif command == 's':
                    await move.B()  
                elif command == 'a':
                    await move.L_90()  # 调整速度
                elif command == 'd':
                    await move.R_30()  # 调整速度
    except KeyboardInterrupt:
        move.shutdown()
    finally:
        move.shutdown()

if __name__ == '__main__':  
    asyncio.run (main())