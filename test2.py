import asyncio
import RPi.GPIO as GPIO
from pywizlight.bulb import wizlight, PilotBuilder


GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN)

async def handle_gpio_event():
    # Your asynchronous function code here
    print("GPIO event detected!")
    desk = wizlight("192.168.0.43")
    await desk.lightSwitch()


async def main():
    while True:
        # wait for a GPIO event to occur
        await asyncio.wait_for(
            asyncio.to_thread(GPIO.wait_for_edge, 17, GPIO.RISING),
            None
        )
        # call the async event handler function
        asyncio.create_task(handle_gpio_event())

# start the event loop
asyncio.run(main())