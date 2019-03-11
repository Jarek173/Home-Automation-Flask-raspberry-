import RPi.GPIO as GPIO

def setPin(pin, pinStatus):
    if pinStatus == "out":
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)
    if pinStatus == "in":
        GPIO.setup(pin, GPIO.IN)
        

