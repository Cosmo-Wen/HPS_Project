import asyncio
from gpiozero import Robot
import getch
import time

BASE_SPEED = 0.6
# 設置左右輪引腳
LEFT_PIN1 = 9
LEFT_PIN2 = 10
RIGHT_PIN1 = 7
RIGHT_PIN2 = 8
# 創建 Robot 實例
robot = Robot(left=(LEFT_PIN1, LEFT_PIN2), right=(RIGHT_PIN1, RIGHT_PIN2))
def stop():
    robot.stop()
def move(speed_left, speed_right):
    robot.value = (speed_left, speed_right)
    # time.sleep(0.7)
    # robot.stop()
async def F_L():
    move(0.45, 0.45)
    await asyncio.sleep(0.1)
    robot.stop()
    await asyncio.sleep(0.1)
async def F_30():
    move(0.45, 0.45)
    await asyncio.sleep(0.85)
    robot.stop()
    await asyncio.sleep(0.1)
def B():
    move(speed_left=-BASE_SPEED, speed_right=-BASE_SPEED + 0.1)
async def B_15():
    move( -0.4, speed_right=-0.3)
    await asyncio.sleep(0.01)
    robot.stop()
async def L_180():
    print("向左轉180")
    robot.value = (-0.6, 0.7)
    await asyncio.sleep(0.5)
    robot.value = (-0.3,0.4)
    await asyncio.sleep(0.4)
    robot.stop()
async def L_90():
    print("向左轉90")
    robot.value = (-0.6, 0.6)
    await asyncio.sleep(0.28)
    robot.value = (-0.4,0.4)
    await asyncio.sleep(0.2)
    robot.stop()
async def L_30():
    print("向左轉30")
    robot.value = (-0.5, 0.5)
    await asyncio.sleep(0.18)
    robot.stop()
    await asyncio.sleep(0.1)
async def R_180():
    print("向右轉180")
    robot.value = (0.7,-0.6)
    await asyncio.sleep(0.5)
    robot.value = (0.4,-0.3)
    await asyncio.sleep(0.45)
    robot.stop()
    await asyncio.sleep(1)
async def R_90():
    print("向右轉90")
    robot.value = (0.6,-0.6)
    await asyncio.sleep(0.28)
    robot.value = (0.4,-0.4)
    await asyncio.sleep(0.2)
    robot.stop()
async def R_30():
    print("向右轉30")
    robot.value = (0.5,-0.5)
    await asyncio.sleep(0.2) 
    robot.stop()
    await asyncio.sleep(0.1)
async def R_30_round(num):
    for i in range(num):
        await R_30()
async def L_30_round(num):
    for i in range(num):
        await L_30()
async def F_30_round(num):
    for i in range(num):
        await F_30()

async def main():
    while True:
        command = getch.getch()
        
        if command == 'x':
            robot.stop()
            break
        else:
                robot.stop()  # 先停止当前动作
                if command == 'w':
                    await F_L()
                elif command == 's':
                    await B()  
                elif command == 'a':
                    await L_90()  # 调整速度
                elif command == 'd':
                    await R_30()  # 调整速度

if __name__ == '__main__':
    try:
        print("Enter commands: 'w' for Backward, 's' for decelerate backward, 'a' for left, 'd' for right, 'x' to exit")
        asyncio.run (main())

    except KeyboardInterrupt:
        robot.stop()

    finally:
        robot.stop()
