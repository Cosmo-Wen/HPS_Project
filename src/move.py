import time
import asyncio
from gpiozero import Robot
from gpiozero.pins.rpigpio import RPiGPIOFactory
import RPi.GPIO as GPIO
from .directions import *
import math
from .SerialCapture import UWB3000Serial

# 設置超聲波感測器的引腳
FRONT_TRIGGER_PIN = 5  # 前方超聲波感測器的 Trigger 引腳
FRONT_ECHO_PIN = 6     # 前方超聲波感測器的 Echo 引腳
LEFT_TRIGGER_PIN = 13   # 左方超聲波感測器的 Trigger 引腳
LEFT_ECHO_PIN = 19      # 左方超聲波感測器的 Echo 引腳
RIGHT_TRIGGER_PIN = 24  # 右方超聲波感測器的 Trigger 引腳
RIGHT_ECHO_PIN = 25     # 右方超聲波感測器的 Echo 引腳

FORWARD_STEP = 30 #30cm 
TURN_STEP = 30 #30deg
STOP_RADIUS = 50  #50cm
ROTATE_RADIUS = 10  #12cm
MAX_TRAVEL_DIST = 150 #150cm
# 超聲波感測的最大距離 (單位: 公分)
MAX_DISTANCE = 100
BBB = 12
MAX_D_RF = 20#左右偵測最大避障距離
MAX_F=23#前

# 初始化 RPigpioFactory
pin_factory = RPiGPIOFactory()


# 初始化 GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(FRONT_TRIGGER_PIN, GPIO.OUT)
GPIO.setup(FRONT_ECHO_PIN, GPIO.IN)
GPIO.setup(LEFT_TRIGGER_PIN, GPIO.OUT)
GPIO.setup(LEFT_ECHO_PIN, GPIO.IN)
GPIO.setup(RIGHT_TRIGGER_PIN, GPIO.OUT)
GPIO.setup(RIGHT_ECHO_PIN, GPIO.IN)
front_distance = 1000
left_distance = 1000
right_distance = 1000
A_B_thread_enabled=True

ser = UWB3000Serial('/dev/ttyUSB0',115200)
ser.reset_input_buffer()

def measure_distance(trigger_pin, echo_pin):
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
    # print(distance)
    return min(distance, MAX_DISTANCE)

# try:
#     print("按下 Ctrl+C 可停止程式")
#     while True:
#         front_distance = measure_distance(FRONT_TRIGGER_PIN, FRONT_ECHO_PIN)
#         left_distance = measure_distance(LEFT_TRIGGER_PIN, LEFT_ECHO_PIN)
#         right_distance = measure_distance(RIGHT_TRIGGER_PIN, RIGHT_ECHO_PIN)
        
#         if left_distance<MAX_D_RF or right_distance<MAX_D_RF or front_distance < MAX_F:
#             print("已停止")
#             test_1.stop()
#         else:
#             print("前進")
#             test_1.F()


# except KeyboardInterrupt:
#     pass
# finally:
#     test_1.stop


# 全局事件，用於控制執行緒停止
# stop_event = threading.Event()
# stop_a_b_event = threading.Event()
# # 執行緒1：檢測超聲波距離並停止馬達
# def distance_check_and_stop():
#     global distance_measurement_enabled
#     while True:
#         if left_distance < MAX_D_RF or right_distance < MAX_D_RF or front_distance < MAX_F:
#             print("*＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊...")  # 印出分隔線
#             distance_measurement_enabled = False  # 停用距離測量
#             test_1.stop()
#             time.sleep(0.5)
#             Obstacle_avoidance()
#             time.sleep(0.1)
#             distance_measurement_enabled = True  # 在避障結束後重新啟用距離測量
#         else:
#             distance_measurement_enabled = True  # 啟用距離測量
#         time.sleep(0.001)


# 執行緒2：持續監控距離並更新
# def update_distances():
#     global front_distance, left_distance, right_distance
#     while True:
#         if distance_measurement_enabled:
#             front_distance = measure_distance(FRONT_TRIGGER_PIN, FRONT_ECHO_PIN)
#             left_distance = measure_distance(LEFT_TRIGGER_PIN, LEFT_ECHO_PIN)
#             right_distance = measure_distance(RIGHT_TRIGGER_PIN, RIGHT_ECHO_PIN)
#             # print("前方距離：{} 厘米，左側距離：{} 厘米，右側距離：{} 厘米".format(front_distance, left_distance, right_distance))
#         time.sleep(0.003)

def update_distances_1():
    global front_distance, left_distance, right_distance
    front_distance = measure_distance(FRONT_TRIGGER_PIN, FRONT_ECHO_PIN)
    left_distance = measure_distance(LEFT_TRIGGER_PIN, LEFT_ECHO_PIN)
    right_distance = measure_distance(RIGHT_TRIGGER_PIN, RIGHT_ECHO_PIN)
    print("前方距離：{} 厘米，左側距離：{} 厘米，右側距離：{} 厘米".format(front_distance, left_distance, right_distance))

def check_light():
    update_distances_1()
    if left_distance > MAX_D_RF and right_distance > MAX_D_RF and front_distance > MAX_F  :
        return True
    else:
        return False
async def Obstacle_avoidance():
    Flag=False
    print("*****************************************************************")
    update_distances_1()
    if not check_light():
        if right_distance<left_distance:
            Flag=False
        else:
            Flag=True
        i=0
        j=0
        if Flag ==False:#往左邊走
            for i in range(5):
                update_distances_1()
                if check_light():
                    await F_30()
                    return True
                else:
                    await L_30()
                    await asyncio.sleep(0.5)


            if i==4:
                update_distances_1()
                if check_light():
                    await F_30()
                    return True
                return False

        if Flag == True:
            for j in range(5):
                update_distances_1()
                if check_light():
                    print("**")
                    await F_30()
                    return True
                else:
                    await R_30()
                    await asyncio.sleep(0.5)
            if j==4:#往右邊
                update_distances_1()
                if check_light():
                    print("**")
                    await F_30()
                    return True
                return False

def get_intersection(s1, s2, s3):
    x = (s3**2 - s1**2)/(4*ROTATE_RADIUS)
    y = (s3**2 + s1**2)/2 - ROTATE_RADIUS**2 - x**2
    y = 0 if y < 0 else math.sqrt(y)

    error1 = abs(math.sqrt(x**2 + (ROTATE_RADIUS-y)**2) - s2)
    error2 = abs(math.sqrt(x**2 + (ROTATE_RADIUS+y)**2) - s2)

    return (x,y) if error1<error2 else (x,-y)

def angle_count(angle):
    return int(angle/30)
def distance_count(Dis):
    return int(Dis/30)
async def find_direction():
    await asyncio.sleep(1)
    s1 = ser.read_distance()
    print('s1 = ', s1, 'cm')
    # rotate 90 逆時針
    await L_90()
    # input('Press enter after rotate 90deg counterclkwise')
    
    await asyncio.sleep(1)
    s2 = ser.read_distance()
    print('s2 = ', s2, 'cm')
    # rotate 90 逆時針
    await L_90()
    # input('Press enter after rotate 90deg counterclkwise')
    
    await asyncio.sleep(1)
    s3 = ser.read_distance()
    print('s3 = ', s3, 'cm')
    await R_180()
    # input('Press enter after rotate 180deg')
    
    
    
    target_coordinate = get_intersection(s1, s2, s3)
    '''
    distance(cm) between car and target
    angle(deg) that car needs to rotate counterclockwise
    '''
    distance = math.sqrt(target_coordinate[0]**2 + target_coordinate[1]**2)
    angle = math.degrees(math.atan2(target_coordinate[1], target_coordinate[0]))


    return distance, angle

async def A_B():
    # input("Press enter to start process")
    await asyncio.sleep(1)

    while True:
        distance = float(ser.read_distance())
        
        if distance <= STOP_RADIUS:
            break

        else:
            print('distance isn\'t close enough, keep going')
            # input('Press enter to start measure process')
            distance, angle = await find_direction()
            print('distance = ', distance, 'cm')
            print('angle = ', angle, 'deg')

            angle_to_rotate = TURN_STEP*round(angle/TURN_STEP)
            # car rotate
            # 此處angl介於-180到180
            if angle < 0: 
                angle = -angle
                # 右轉angle
                await R_30_round(angle_count(angle))
            else:
                # 左轉angle
                await L_30_round(angle_count(angle))
            # input('Press enter after car rotate ' + str(angle_to_rotate) + 'deg')
            distance_to_go = min(MAX_TRAVEL_DIST, FORWARD_STEP*math.ceil(0.5*distance/FORWARD_STEP))
            # car go
            update_distances_1()
            print("前方距離：{} 厘米，左側距離：{} 厘米，右側距離：{} 厘米".format(front_distance, left_distance, right_distance))
            for i in range(distance_count(distance_to_go)):
                update_distances_1()
                if left_distance > 30 and right_distance > 30 and front_distance > 30 :
                    await F_30()
                elif distance <= STOP_RADIUS:
                    return True
                elif left_distance > 20 or right_distance > 20 or front_distance > 20:
                    await F_L()
                    return False
                else:
                    return False
    print('good! distance satisfied')
    ser.close()
    return True
        # input('Press enter after car go ' + str(distance_to_go) + 'cm')

async def move():
    print("按下 Ctrl+C 可停止程式")
    while True :
        Flag = await A_B()
        if not Flag:
            Flag=await Obstacle_avoidance()
        else:
            break

if __name__ == "__main__":
    try:
        asyncio.run(move())
    except KeyboardInterrupt:
        pass
    finally:
        stop()