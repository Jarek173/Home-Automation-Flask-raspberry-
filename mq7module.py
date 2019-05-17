import spidev
from numpy import interp
import RPi.GPIO as GPIO
output = 0;

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(5, GPIO.OUT)
GPIO.setup(6, GPIO.OUT)
GPIO.output(5, GPIO.HIGH)
GPIO.output(6, GPIO.HIGH)

spi = spidev.SpiDev() 
spi.open(0,0)
GPIO.setup(2, GPIO.IN)

def mq7DigitalInput(pin):
    if GPIO.input(pin):
        return 0
    if GPIO.input(pin)!= 1:
        return 1
    
def mq7AnalogInput(channel):
    spi.max_speed_hz = 1350000
    adc = spi.xfer2([1,(8+channel)<<4,0])
    data = ((adc[1]&3) <<8) + adc[2]
    return data

def main():
    global output 
    output = mq7AnalogInput(0) 
    output = interp(output, [0, 1023], [0, 1000])
    Doutput = mq7DigitalInput(2)
