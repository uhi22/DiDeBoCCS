import Adafruit_BBIO.GPIO as GPIO
from time import sleep

# If the P9_28 does not work as general purpose output (GPIO), check whether the
# SPI1 consumes this pin (seems to be default on debian 5.10.168-ti-r72). In this
# case, a solution is to create a special overlay which removes the SPI1 and
# configures the P9_28 as GPIO. See setup_focccicape.md.

PIN_buttonLedControl = "P9_28"
PIN_buttonReadback = "P9_30"


print("Testing button with LED")
GPIO.setup(PIN_buttonLedControl, GPIO.OUT)
GPIO.setup(PIN_buttonReadback, GPIO.IN)


for i in range(0, 1000):
    GPIO.output(PIN_buttonLedControl, 1)
    sleep(0.02)
    b = GPIO.input(PIN_buttonReadback)
    if (b==0):
        print("Button is pressed")
    sleep(0.4)
    GPIO.output(PIN_buttonLedControl, 0)
    sleep(0.1)
    

