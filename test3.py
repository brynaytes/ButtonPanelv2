from pywizlight.bulb import wizlight, PilotBuilder
from urllib.parse import urlencode
import RPi.GPIO as GPIO
import asyncio
import time
import requests
import pycurl


lightIP = "192.168.0.43"
rokuIP = "192.168.1.70"

lbr = 250
lshuff = 1
lshuffMax = 4
lightPowerGPIO = 17
lightShuffleGPIO = 23
lightDimGPIO = 27
lightBrightGPIO = 17
lightErrorGPIO = 21

#netflix:12   LiveTV:tvinput.dtv   Youtube:837
rokuChanels = ['12','tvinput.dtv','837']
rokuChanelShuff = 0;
rokuChanelMax = 3;
rokuPower = 25
rokuVolDown = 23
rokuVolUp = 24
rokuChanel= 16



async def lightPow():
    await light.lightSwitch()

async def lightShuffle(l):
    #sets light to warm white
    await light.turn_on(PilotBuilder(scene = l))
    
async def lightDim():
    await light.turn_on(PilotBuilder(lbr))
    print(lbr)
    
async def lightBrighten():    
    await light.turn_on(PilotBuilder(lbr))
    print(lbr)
        
def changeChanel():
    rokuSendRequest("launch/"+rokuChanels[rokuChanelShuff])
    #requests.post("http://"+rokuIP+":8060/launch/" + rokuChanels[rokuChanelShuff])
    if(rokuChanelShuff == 0):
        time.sleep(2)
        rokuSendRequest("keypress/Select")
        #requests.post("http://192.168.1.70:8060/keypress/Select")
        time.sleep(1)
        rokuSendRequest("keypress/Select")

        #requests.post("http://192.168.1.70:8060/keypress/Select")
        
def rokuSendRequest(action):
    #This needs to be a post command, but it doesnt need any paramiters.
    c = pycurl.Curl()
    try:
        c = pycurl.Curl()
        c.setopt(c.URL, "http://"+rokuIP+":8060/"+action)
        #c.setopt(c.URL, "http://192.168.1.70:8060/keypress/power")
        data = {'': ''}
        pf = urlencode(data)
        c.setopt(c.POSTFIELDS,pf)
        c.perform()
        c.close()
        GPIO.output(lightErrorGPIO, GPIO.LOW)

    except pycurl.error:
        GPIO.output(lightErrorGPIO, GPIO.HIGH)

    #finally:
        

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)  
GPIO.setup(lightPowerGPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(lightShuffleGPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(lightDimGPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(lightBrightGPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(lightErrorGPIO, GPIO.OUT)


GPIO.setup(rokuPower, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(rokuVolDown, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(rokuVolUp, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(rokuChanel, GPIO.IN, pull_up_down=GPIO.PUD_UP)



light = wizlight(lightIP)


while True:
    #this set is for 
    if GPIO.input(lightPowerGPIO) == False:
        print("switch")
        try:
            asyncio.run(lightPow())
            GPIO.output(lightErrorGPIO, GPIO.LOW)
        except:
            print("error")
            GPIO.output(lightErrorGPIO, GPIO.HIGH)
        finally:
            lbr = 250
    
    if GPIO.input(lightShuffleGPIO) == False:
        if(lshuff > lshuffMax):
            lshuff = 1
        else:
            lshuff +=1
        asyncio.run(lightShuffle(lshuff))
        
    if GPIO.input(lightDimGPIO) == False:
        if lbr > 0:
            lbr -= 50
        asyncio.run(lightDim())
        
    if GPIO.input(lightBrightGPIO) == False:
        if lbr < 250:
            lbr += 50
        asyncio.run(lightBrighten())
        
        
        
        
    if GPIO.input(rokuPower) == False:
        rokuSendRequest("keypress/power")    
        time.sleep(.3)
        
    if GPIO.input(rokuVolDown) == False:
        #requests.post("http://"+rokuIP+":8060/keypress/VolumeDown")
        rokuSendRequest("keypress/VolumeDown")  
        time.sleep(.3)

    
    if GPIO.input(rokuVolUp) == False:
        #requests.post("http://"+rokuIP+":8060/keypress/VolumeUp")
        rokuSendRequest("keypress/VolumeUp")  
        time.sleep(.3)
        
    if GPIO.input(rokuChanel) == False:
        if rokuChanelShuff == len(rokuChanels) -1 :
            rokuChanelShuff = 0
        else:
            rokuChanelShuff += 1
        changeChanel()
        time.sleep(.3)

        
GPIO.cleanup()
