import asyncio
import numpy as np
import RPi.GPIO as GPIO
import time

from .header import *

class Is_Full:
    def __init__(self, trig_pin, echo_pin):
        self._trigger = trig_pin
        self._echo = echo_pin
        GPIO.setmode(GPIO.BCM)

    async def check_distance(self):        
        
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

        # 限制測量距離在3cm到21cm之間，超出21cm時輸出垃圾桶已滿的值
        if distance < 3:
            distance = 3
        elif distance > 21:
            distance = AVOID_FULL - 0.5
        await asyncio.sleep(0.1)
        return distance

    # 獲取多次測量距離值列表
    async def get_distance(self):
        distances = [await self.check_distance() for i in range(DEPTH_SAMPLE)]
        return np.mean(distances)
    
    async def is_trash_can_full(self):
        distance = await self.get_distance()
        if distance is not None:
            if distance < AVOID_FULL:
                return True
            else:
                return False
        else:
            return None
    
    def shutdown(self):
        GPIO.cleanup()     
        
async def detect_full(sensor1: Is_Full, sensor2: Is_Full):
    if await sensor1.is_trash_can_full() and await sensor2.is_trash_can_full():
        return True
    else:
        return False