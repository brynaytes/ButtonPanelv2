from pywizlight.bulb import wizlight, PilotBuilder
import RPi.GPIO as GPIO
import asyncio


desk_lightIP = "192.168.0.43"
ball_light_1_IP = ""
ball_light_2_IP = ""

desk_light_GPIO = 17
ball_light_GPIO = 27
color_white_toggle_GPIO = 22
dimmer_GPIO = 23


GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)  
GPIO.setup(desk_light_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(ball_light_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(color_white_toggle_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(dimmer_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)


desk = wizlight(desk_lightIP)

#light info
isColor = False # false - warm white light    true - colored light
colorSelected = 0
colorProfiles = [[0,0,255], [0,255,0], [255,0,0]]
brightness = 255

async def deskPow():
    await desk.lightSwitch()

async def deskColor():
    await  desk.turn_on(PilotBuilder(rgb = (colorProfiles[colorSelected][0], colorProfiles[colorSelected][1], colorProfiles[colorSelected][2])))

async def deskWhite():
    await  desk.turn_on(PilotBuilder(warm_white = 255, brightness = brightness))

async def deskDim():
    await desk.turn_on(PilotBuilder(brightness = brightness))

def deskPowerFunc():
    print("desk")
    asyncio.run( deskPow())

def roomPowerFunc():
    print("room")

def toggleColorFunc():

    isColor = not isColor
    if isColor : 
        asyncio.run( deskWhite())
    else:
        asyncio.run( deskColor())

def changeColorOrDimFunc():
    if isColor : 
        colorSelected += 1
        if colorSelected >= len(colorProfiles) :
            colorSelected = 0
        asyncio.run( deskColor())
    else :
        brightness -= 75
        if brightness < 0:
            brightness = 255
        asyncio.run( deskDim())




GPIO.add_event_detect(desk_light_GPIO, GPIO.FALLING, callback=deskPowerFunc)