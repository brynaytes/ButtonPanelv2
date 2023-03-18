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





while True:
    if GPIO.input(desk_light_GPIO) == False:
        print("desk")
    
    if GPIO.input(ball_light_GPIO) == False:
        print("ball")

    if GPIO.input(color_white_toggle_GPIO) == False:
        print("toggle")

    if GPIO.input(dimmer_GPIO) == False:
        print("dimmer")
