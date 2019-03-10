import RPi.GPIO as GPIO

def setPin(pin, pinStatus):
    if pinStatus == "out":
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)
    if pinStatus == "in":
        GPIO.setup(pin, GPIO.IN)
        
def mq7(pin):
    GPIO.setup(pin, GPIO.IN)
    if GPIO.input(pin):
        return 0
    if GPIO.input(pin)!=1:
        return 1
