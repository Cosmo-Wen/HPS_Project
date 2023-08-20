import RPi.GPIO as GPIO
from time import sleep, time

PIN_TRIGGER = 7
PIN_ECHO = 11
PIN_SERVO = 12

GPIO.setmode(GPIO.BOARD)
GPIO.setup(PIN_TRIGGER, GPIO.OUT)
GPIO.setup(PIN_ECHO, GPIO.IN)
GPIO.setup(PIN_SERVO, GPIO.OUT)

pwm = GPIO.PWM(PIN_SERVO, 50)
pwm.start(4)

class Lid:
    def __init__(self):
        self.run = False

    def sense(self):
        flag = False

        while self.run:
            #Trigger
            GPIO.output(PIN_TRIGGER, GPIO.HIGH)
            sleep(0.00001)
            GPIO.output(PIN_TRIGGER, GPIO.LOW)

            while GPIO.input(PIN_ECHO)==0:
                pulse_start_time = time()
            while GPIO.input(PIN_ECHO)==1:
                pulse_end_time = time()

            pulse_duration = pulse_end_time - pulse_start_time
            distance = round(pulse_duration * 17150, 2)
            print("Distance:",distance,"cm")

            if(distance < 10):
                if(flag==False):
                    pwm.ChangeDutyCycle(7.5)
                    sleep(5)
                    pwm.ChangeDutyCycle(4)
                    sleep(1)
                flag = True
            else:
                flag = False

            sleep(1)

lid = Lid()
try:
    lid.sense()
    sleep(5)
    lid.run = True
    lid.sense()
finally:
    pwm.stop()
    GPIO.cleanup()
