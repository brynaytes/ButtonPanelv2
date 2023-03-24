import asyncio
import RPi.GPIO as GPIO
from pywizlight.bulb import wizlight, PilotBuilder

GPIO_PIN = 17  # Change this to the GPIO pin number you want to use

async def handle_gpio_event():
    # Your asynchronous function code here
    print("GPIO event detected!")
    desk = wizlight("192.168.0.43")
    await desk.lightSwitch()



def main():
    # Setup GPIO pin
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(GPIO_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    # Create event loop and add GPIO event detection task
    loop = asyncio.get_event_loop()
    loop.add_reader(GPIO_PIN, handle_gpio_event)

    # Start event loop
    try:
        loop.run_forever()
    finally:
        # Clean up GPIO and event loop
        GPIO.cleanup()
        loop.close()

if __name__ == "__main__":
    main()
