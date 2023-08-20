import RPi.GPIO as GPIO
from time import sleep, time

PIN_TRIGGER = 7
PIN_ECHO = 11
PIN_SERVO = 12



class Lid:
    def __init__(self):
        self._run = False
        self._flag = False

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(PIN_TRIGGER, GPIO.OUT)
        GPIO.setup(PIN_ECHO, GPIO.IN)
        GPIO.setup(PIN_SERVO, GPIO.OUT)

        self._pwm = GPIO.PWM(PIN_SERVO, 50)
        self._pwm.start(4)
    
    def turn_on(self):
        self._run = True
    
    def turn_off(self):
        self._run = False
    
    def current_status(self):
        return self._run

    def change_duty_cycle(self, amount):
        self._pwm.ChangeDutyCycle(amount)
    
    def shutdown(self):
        self._pwm.stop()
        GPIO.cleanup()

    async def sense(self):
        while self.current_status():
            #Trigger
            GPIO.output(PIN_TRIGGER, GPIO.HIGH)
            sleep(0.00001)
            GPIO.output(PIN_TRIGGER, GPIO.LOW)

            while GPIO.input(PIN_ECHO) == 0:
                pulse_start_time = time()

            while GPIO.input(PIN_ECHO) == 1:
                pulse_end_time = time()

            pulse_duration = pulse_end_time - pulse_start_time
            
            distance = round(pulse_duration * 17150, 2)
            
            print("Distance:",distance,"cm")

            if distance < 10:
                if not self._flag :
                    self._pwm.ChangeDutyCycle(7.5)
                    sleep(5)
                    self._pwm.ChangeDutyCycle(4)
                    sleep(1)
                self._flag = True
            else:
                self._flag = False

            sleep(1)
    
try:
    lid = Lid()
    lid.sense()
    sleep(5)
    lid.turn_on()
    lid.sense()
finally:
    lid.shutdown()