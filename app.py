import asyncio
import numpy as np
import RPi.GPIO as GPIO

FULL = 9
SENSOR1_TRIGGER = 20
SENSOR1_ECHO = 21
SENSOR2_TRIGGER = 22
SENSOR2_ECHO = 23
ITERATIONS = 10

class Is_Full:
    def __init__(self, trig_pin, echo_pin):
        self._trigger = trig_pin
        self._echo = echo_pin
        GPIO.setup(self._trigger, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self._echo, GPIO.IN)


    async def check_distance(self):
        GPIO.output(self._trigger, GPIO.HIGH)
        asyncio.sleep(0.00015)
        GPIO.output(self._trigger, GPIO.LOW)
    
        while not GPIO.input(self._echo):
            pass
        t1 = asyncio.get_event_loop().time()
        
        while GPIO.input(self._echo):
            pass
        t2 = asyncio.get_event_loop().time()
        
        distance = (t2 - t1) * 340 * 100 / 2
        
        # 限制測量距離在3cm到21cm之間，超出21cm時輸出垃圾桶已滿的值
        if distance < 3:
            distance = 3
        elif distance > 21:
            distance = FULL - 0.5
        
        asyncio.sleep(0.1)
        
        return distance

    # 獲取多次測量距離值列表
    async def get_distance(self):
        distances = [self.check_distance(self._trigger, self._echo) for i in range(ITERATIONS)]
        return np.mean(distances)

    def is_trash_can_full(self):
        distance = self.get_distance()
        if distance is not None:
            print('平均距離：%0.2f 公分' % distance)
            if distance < FULL:
                return True
            else:
                return False
        else:
            print('無法確定參考距離')
            return None
    
    def shutdown():
        GPIO.cleanup()     
        
def detect_full(sensor1: Is_Full, sensor2: Is_Full):
    if sensor1.is_trash_can_full() and sensor2.is_trash_can_full():
        print('Trash can is full')
    else:
        print('Trash can is not full')   

async def main():
    try:
        sensor1 = Is_Full(SENSOR1_TRIGGER, SENSOR1_ECHO)
        sensor2 = Is_Full(SENSOR2_TRIGGER, SENSOR2_ECHO)
        detect_full(sensor1, sensor2)
    finally:
        sensor1.shutdown()

if __name__ == "__main__":
    main()