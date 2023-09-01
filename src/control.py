import asyncio

import RPi.GPIO as GPIO

from .is_full import Is_Full, detect_full
from .header import *

class Lid:
    def __init__(self):
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
    
    def turn_on(self):
        self._sense_event.set()
    
    def turn_off(self):
        self._sense_event.clear()
    
    def shutdown(self):
        self._sense_event.clear()
        self._pwm.stop()
        GPIO.cleanup()

    async def sense(self):
        sensor1 = Is_Full(DEPTH_SENSOR1_TRIG, DEPTH_SENSOR1_ECHO)
        sensor2 = Is_Full(DEPTH_SENSOR2_TRIG, DEPTH_SENSOR2_ECHO)
        while True:
            await self._sense_event.wait()
            #Trigger
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