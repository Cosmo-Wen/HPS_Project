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
def F():
    print("向前進")
    move(speed_left=BASE_SPEED, speed_right=BASE_SPEED - 0.1)
def F_L():
    move(0.45, 0.45)
    time.sleep(0.1)
    robot.stop()
    time.sleep(0.1)
def F_30():
    move(0.45, 0.45)
    time.sleep(0.85)
    robot.stop()
    time.sleep(0.1)
def B():
    move(speed_left=-BASE_SPEED, speed_right=-BASE_SPEED + 0.1)
def B_15():
    move( -0.4, speed_right=-0.3)
    time.sleep(0.01)
    robot.stop()
def L_180():
    print("向左轉180")
    robot.value = (-0.6, 0.7)
    time.sleep(0.5)
    robot.value = (-0.3,0.4)
    time.sleep(0.4)
    robot.stop()
def L_90():
    print("向左轉90")
    robot.value = (-0.6, 0.6)
    time.sleep(0.28)
    robot.value = (-0.4,0.4)
    time.sleep(0.2)
    robot.stop()
def L_30():
    print("向左轉30")
    robot.value = (-0.5, 0.5)
    time.sleep(0.18)
    robot.stop()
    time.sleep(0.1)
def R_180():
    print("向右轉180")
    robot.value = (0.7,-0.6)
    time.sleep(0.5)
    robot.value = (0.4,-0.3)
    time.sleep(0.45)
    robot.stop()
    time.sleep(1)
def R_90():
    print("向右轉90")
    robot.value = (0.6,-0.6)
    time.sleep(0.28)
    robot.value = (0.4,-0.4)
    time.sleep(0.2)
    robot.stop()
def R_30():
    print("向右轉30")
    robot.value = (0.5,-0.5)
    time.sleep(0.2) 
    robot.stop()
    time.sleep(0.1)
def R_30_round(num):
    for i in range(num):
        R_30()
def L_30_round(num):
    for i in range(num):
        L_30()
def F_30_round(num):
    for i in range(num):
        F_30()

if __name__ == '__main__':
    try:
        print("Enter commands: 'w' for Backward, 's' for decelerate backward, 'a' for left, 'd' for right, 'x' to exit")
        while True:
            command = getch.getch()
            
            if command == 'x':
                robot.stop()
                break
            else:
                robot.stop()  # 先停止当前动作
                if command == 'w':
                    F_L()
                elif command == 's':
                    B()  
                elif command == 'a':
                    L_90()  # 调整速度
                elif command == 'd':
                    R_30()  # 调整速度

    except KeyboardInterrupt:
        robot.stop()

    finally:
        robot.stop()


