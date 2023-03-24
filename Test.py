from pywizlight.bulb import wizlight, PilotBuilder
import RPi.GPIO as GPIO
import asyncio


desk_lightIP = "192.168.0.43"

desk_light_GPIO = 17
loop = None



desk = wizlight(desk_lightIP)

async def deskPow():
    await desk.lightSwitch()

def deskPowerFunc():
   if loop is None:
        print(":(")
        return       # should not come to this

    loop.call_soon_threadsafe(deskPow)

try:
    GPIO.setwarnings(False)

    GPIO.setmode(GPIO.BCM)  
    GPIO.setup(desk_light_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(desk_light_GPIO, GPIO.RISING, callback=lambda x: self.deskPowerFunc(), bouncetime=500)

    loop = asyncio.get_event_loop()
    loop.run_forever()
    loop.close()
except : 
    print("Error" , sys.exc_info()[0])
GPIO.cleanup()