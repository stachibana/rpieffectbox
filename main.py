import serial
import spidev
from time import *
import RPi.GPIO as GPIO
import os
import subprocess

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN)
GPIO.setup(18, GPIO.IN)
GPIO.setup(4, GPIO.IN)
preset = 0
preset_old = 0
name_file = open ("/home/pi/rpieffectbox/names.txt")
names = name_file.read().splitlines()
print names
function_file = open ("/home/pi/rpieffectbox/functions.txt")
functions = function_file.read().splitlines()
print functions
ser = serial.Serial('/dev/serial0', baudrate=115200, timeout=3.0)
print("Port" + ser.portstr + ", opened : " + str(ser.isOpen()))
spi = spidev.SpiDev()
spi.open(0, 0)

def readadc(adcnum):
# read SPI data from MCP3008 chip, 8 possible adc's (0 thru 7)
    if adcnum > 7 or adcnum < 0:
        return -1
    r = spi.xfer2([1, 8 + adcnum << 4, 0])
    adcout = ((r[1] & 3) << 8) + r[2]
    return adcout

def forwardEffect(channel):
  global preset, preset_old, names, functions
  if(preset < len(names) - 1):
    logging.warning("incremented : " + str(preset))
    preset_old = preset
    preset = preset + 1
    os.system("echo '1 "+ str(preset_old) +";' | pdsend 5000 localhost")
    os.system("echo '0 "+ str(preset) +";' | pdsend 5000 localhost")
    ser.write("?f" + str(names[preset]) + "?n" + str(functions[preset]))
GPIO.add_event_detect(18, GPIO.RISING, callback=forwardEffect, bouncetime=200)

def backEffect(channel):
  global preset, preset_old, names, functions
  if (GPIO.input(17) and preset > 0):
    preset_old = preset
    preset = preset - 1
    os.system("echo '1 "+ str(preset_old) +";' | pdsend 5000 localhost")
    os.system("echo '0 "+ str(preset) +";' | pdsend 5000 localhost")
    ser.write("?f" + str(names[preset]) + "?n" + str(functions[preset]))
GPIO.add_event_detect(17, GPIO.RISING, callback=backEffect, bouncetime=200)

isToggleOn = False
def toggleMode(channel):
  global preset, presest_old, isToggleOn
  isToggleOn = not isToggleOn
  if(not isToggleOn):
    ser.write("?f" + str(names[preset]) + "?n" + str(functions[preset]))
GPIO.add_event_detect(4, GPIO.RISING, callback=toggleMode, bouncetime=200)


ser.write("?fRaspberry Pi?nEffects Module")
sleep(1)
ser.write("?fBuilt By ?nBen Jacobs")
sleep(2)
ser.write("?fOpening PD...")
sleep(2)
subprocess.call("pd-extended -nogui -audioindev 3 -inchannels 2 -audiooutdev 2 -outchannels 2 /home/pi/rpieffectbox/server.pd &", shell=True)
ser.write("?f" + str(names[preset]) + "?n" + str(functions[preset]))
sleep(1)
os.system("echo '0 "+ str(preset) +";' | pdsend 5000 localhost")
while True:
 sleep(.01)

 if(isToggleOn):
   value0 = readadc(0)
   value1 = readadc(1)
   value2 = readadc(2)
   value3 = readadc(3)

   os.system("echo '3 " + str(value0) + ";' | pdsend 5001 localhost udp")
   os.system("echo '0 " + str(value1) + ";' | pdsend 5001 localhost udp")
   os.system("echo '1 " + str(value2) + ";' | pdsend 5001 localhost udp")
   os.system("echo '2 " + str(value3) + ";' | pdsend 5001 localhost udp")
   ser.write("?fE1:" + str(value3) + " E2:" + str(value2) + "?nE3:" + str(value1) + " E4:" + str(value0))
