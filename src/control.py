import asyncio

import RPi.GPIO as GPIO


PIN_TRIGGER = 7
PIN_ECHO = 11
PIN_SERVO = 12



class Lid:
    def __init__(self):
        self._flag = False
        self._sense_event = asyncio.Event()
        self._sense_event.clear()

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(PIN_TRIGGER, GPIO.OUT)
        GPIO.setup(PIN_ECHO, GPIO.IN)
        GPIO.setup(PIN_SERVO, GPIO.OUT)

        self._pwm = GPIO.PWM(PIN_SERVO, 50)
        self._pwm.start(4)
    
    def turn_on(self):
        self._sense_event.set()
    
    def turn_off(self):
        self._sense_event.clear()
    
    def shutdown(self):
        self._sense_event.clear()
        self._pwm.stop()
        GPIO.cleanup()
        print("DETECT SHUTDOWN")

    async def sense(self):
        while True:
            await self._sense_event.wait()
            #Trigger
            GPIO.output(PIN_TRIGGER, GPIO.HIGH)
            await asyncio.sleep(0.00001)
            GPIO.output(PIN_TRIGGER, GPIO.LOW)

            while GPIO.input(PIN_ECHO) == 0:
                pulse_start_time = loop.get_event_loop().time()

            while GPIO.input(PIN_ECHO) == 1:
                pulse_end_time = loop.get_event_loop().time()

            pulse_duration = pulse_end_time - pulse_start_time
            
            distance = round(pulse_duration * 17150, 2)
            
            print("Distance:",distance,"cm")

            if distance < 10:
                if not self._flag :
                    self._pwm.ChangeDutyCycle(7.5)
                    await asyncio.sleep(5)
                    self._pwm.ChangeDutyCycle(4)
                    await asyncio.sleep(1)
                self._flag = True
            else:
                self._flag = False
            print("Detecting...")
            await asyncio.sleep(1)
    
# try:
#     lid = Lid()
#     lid.sense()
#     sleep(5)
#     lid.turn_on()
#     lid.sense()
# finally:
#     lid.shutdown()