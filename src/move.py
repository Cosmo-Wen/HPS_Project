import time
import asyncio
from gpiozero import Robot
from gpiozero.pins.rpigpio import RPiGPIOFactory
import RPi.GPIO as GPIO

from .directions import *
import math
from .serial_capture import UWB3000Serial
from .header import *

class Move():
    def __init__(self): 
        pin_factory = RPiGPIOFactory()

        # 初始化 GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(AVOID_FRONT_TRIG, GPIO.OUT)
        GPIO.setup(AVOID_FRONT_ECHO, GPIO.IN)
        GPIO.setup(AVOID_LEFT_TRIG, GPIO.OUT)
        GPIO.setup(AVOID_LEFT_ECHO, GPIO.IN)
        GPIO.setup(AVOID_RIGHT_TRIG, GPIO.OUT)
        GPIO.setup(AVOID_RIGHT_ECHO, GPIO.IN)

        self._ser = UWB3000Serial('/dev/ttyUSB0',115200)
        self._ser.reset_input_buffer()

        self._direction = Directions()

    def measure_distance(self, trigger_pin, echo_pin):
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

    def update_distances_1(self):
        global front_distance, left_distance, right_distance
        front_distance = self.measure_distance(AVOID_FRONT_TRIG, AVOID_FRONT_ECHO)
        left_distance = self.measure_distance(AVOID_LEFT_TRIG, AVOID_LEFT_ECHO)
        right_distance = self.measure_distance(AVOID_RIGHT_TRIG, AVOID_RIGHT_ECHO)
        
    def check_light(self):
        self.update_distances_1()
        if left_distance > AVOID_MAX_RL and right_distance > AVOID_MAX_RL and front_distance > AVOID_MAX_F  :
            return True
        else:
            return False

    async def Obstacle_avoidance(self):
        Flag = False
        self.update_distances_1()
        if not self._check_light():
            if right_distance<left_distance:
                Flag=False
            else:
                Flag=True
            i=0
            j=0
            if Flag ==False:#往左邊走
                for i in range(5):
                    self.update_distances_1()
                    if self.check_light():
                        await self._direction.F_30()
                        return True
                    else:
                        await self._direction.L_30()
                        await asyncio.sleep(0.5)


                if i==4:
                    self.update_distances_1()
                    if self.check_light():
                        await self._direction.F_30()
                        return True
                    return False

            if Flag == True:
                for j in range(5):
                    self.update_distances_1()
                    if self.check_light():
                        await self._direction.F_30()
                        return True
                    else:
                        await self._direction.R_30()
                        await asyncio.sleep(0.5)
                if j==4:#往右邊
                    self.update_distances_1()
                    if self.check_light():
                        await self._direction.F_30()
                        return True
                    return False

    def get_intersection(self, s1, s2, s3):
        x = (s3 ** 2 - s1 ** 2) / (4 * MOTOR_ROTATE_RADIUS)
        y = (s3 ** 2 + s1 ** 2) / 2 - MOTOR_ROTATE_RADIUS ** 2 - x ** 2
        y = 0 if y < 0 else math.sqrt(y)

        error1 = abs(math.sqrt(x ** 2 + (MOTOR_ROTATE_RADIUS - y) ** 2) - s2)
        error2 = abs(math.sqrt(x ** 2 + (MOTOR_ROTATE_RADIUS + y) ** 2) - s2)

        return (x,y) if error1 < error2 else (x,-y)

    def angle_count(self, angle):
        return int(angle/30)

    def distance_count(self, Dis):
        return int(Dis/30)

    async def find_direction(self):
        await asyncio.sleep(2)
        s1 = self._ser.read_distance()
        # rotate 90 逆時針
        await self._direction.L_90()
        # input('Press enter after rotate 90deg counterclkwise')
        
        await asyncio.sleep(2)
        s2 = self._ser.read_distance()
        # rotate 90 逆時針
        await self._direction.L_90()
        # input('Press enter after rotate 90deg counterclkwise')
        
        await asyncio.sleep(2)
        s3 = self._ser.read_distance()
        # input('Press enter after rotate 180deg')
        
        
        
        target_coordinate = self.get_intersection(s1, s2, s3)
        '''
        distance(cm) between car and target
        angle(deg) that car needs to rotate counterclockwise
        '''
        distance = math.sqrt(target_coordinate[0] ** 2 + target_coordinate[1] ** 2)
        angle = math.degrees(math.atan2(target_coordinate[1], target_coordinate[0]))


        return distance, angle

    async def A_B(self):
        # input("Press enter to start process")
        await asyncio.sleep(1)

        while True:
            print('test1')
            distance = float(self._ser.read_distance())
            print('test2')
            
            if distance <= MOTOR_STOP_RADIUS:
                print('test3')
                break

            else:
                print('test4')
                distance, angle = await self.find_direction()
                print('test5')
                
                angle_to_rotate = MOTOR_TURN_DEG * round(angle / MOTOR_TURN_DEG)
                # car rotate
                # 此處angl介於-180到180
                if angle < 0: 
                    angle = 180+angle
                    # 右轉angle
                    print('test1')
                    await self._direction.L_30_round(self.angle_count(angle))
                    print('test1')
                else:
                    # 左轉angle
                    angle = 180-angle
                    await self._direction.R_30_round(self.angle_count(angle))
                # input('Press enter after car rotate ' + str(angle_to_rotate) + 'deg')
                distance_to_go = min(MOTOR_MAX_TRAVEL_DIST, MOTOR_FORWARD*math.ceil(0.5*distance/MOTOR_FORWARD))
                # car go
                self.update_distances_1()
                for i in range(self.distance_count(distance_to_go)):
                    self.update_distances_1()
                    if left_distance > 30 and right_distance > 30 and front_distance > 30 :
                        await self._direction.F_30()
                    elif distance <= MOTOR_STOP_RADIUS:
                        return True
                    elif left_distance > 20 or right_distance > 20 or front_distance > 20:
                        await self._direction.F_L()
                        return False
                    else:
                        return False
        return True
            # input('Press enter after car go ' + str(distance_to_go) + 'cm')

    async def move(self):
        while True :
            Flag = await self.A_B()
            if not Flag:
                Flag=await self.Obstacle_avoidance()
            else:
                break

    def shutdown(self):
        self._direction.shutdown()
