import smbus
import time
# Define some constants from the datasheet
lightLevel = 0
DEVICE     = 0x23 # Default device I2C address
ONE_TIME_HIGH_RES_MODE_1 = 0x20
#bus = smbus.SMBus(0) # Rev 1 Pi uses 0
bus = smbus.SMBus(1)  # Rev 2 Pi uses 1

def convertToNumber(data):
  result=(data[1] + (256 * data[0])) / 1.2
  return (result)

def readLight(addr=DEVICE):
  data = bus.read_i2c_block_data(addr,ONE_TIME_HIGH_RES_MODE_1)
  return convertToNumber(data)

def main():
  while True:
    global lightLevel
    lightLevel=readLight()
    print(lightLevel)
    time.sleep(2)

   
    
