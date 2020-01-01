import smbus
import time
import Adafruit_DHT
import BlynkLib
DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 17
BLYNK_AUTH = 'aLgfbszploYw448BLJcKqVGppRW-s5Cf'
blynk = BlynkLib.Blynk(BLYNK_AUTH)
DEVICE     = 0x23
POWER_DOWN = 0x00 # No active state
POWER_ON   = 0x01 # Power on
RESET      = 0x07 # Reset data register value
ONE_TIME_HIGH_RES_MODE_1 = 0x20
bus = smbus.SMBus(1)
@blynk.on("readV1")
@blynk.on("readV2")
@blynk.on("readV3")
def readLight(addr=DEVICE):
  data = bus.read_i2c_block_data(addr,ONE_TIME_HIGH_RES_MODE_1)
  return convertToNumber(data)

def convertToNumber(data):
  result=(data[1] + (256 * data[0])) / 1.2
  return (result)

def main():

  while True:
    lightLevel=readLight()
    print("Light Level : " + format(lightLevel,'.2f') + " lx")
    blynk.virtual_write(1,int(lightLevel))
    time.sleep(0.5)
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    if humidity is not None and temperature is not None:
        print("Temp={0:0.1f}*C  Humidity={1:0.1f}%".format(temperature, humidity))
    else:
        print("Failed to retrieve data from humidity sensor")
    blynk.virtual_write(2,int(temperature))
    blynk.virtual_write(3,int(humidity))

if __name__=="__main__":
   main()
   blynk.run()
