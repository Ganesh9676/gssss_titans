import RPi.GPIO as GPIO
import smbus
import time
import Adafruit_DHT
import BlynkLib
from Adafruit_CharLCD import Adafruit_CharLCD 
from time import sleep
GPIO.setmode(GPIO.BCM)
RELAIS_1_GPIO = 21
RELAIS_2_GPIO = 20
RELAIS_3_GPIO = 16
RELAIS_4_GPIO = 12
lcd = Adafruit_CharLCD(rs=7, en=8, d4=25, d5=24, d6=23, d7=18, cols=20, lines=4)
lcd.clear()
DHT_SENSOR  = Adafruit_DHT.DHT22
DHT_PIN = 4
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
    lcd.home()
    lcd.message('TEMP:'+str(int(temperature))+'*C')
    lcd.set_cursor(11,0)
    lcd.message('HUM:'+str(int(humidity))+'%')
    lcd.set_cursor(0,1)
    lcd.message('LIGHT:'+str(int(lightLevel))+' lx')
    GPIO.setup(RELAIS_1_GPIO, GPIO.OUT)
    GPIO.setup(RELAIS_2_GPIO, GPIO.OUT)
    GPIO.setup(RELAIS_3_GPIO, GPIO.OUT)
    GPIO.setup(RELAIS_4_GPIO, GPIO.OUT)
if __name__=="__main__":
   main()
   blynk.run()
