import os
from time import sleep

def setPwmFivePercent(blOn):
    with open(pwmbase + "duty_cycle", "w") as f:
        if (blOn):
            # f.write("50000") # 5%
            f.write("48000") # a little bit below 5% to compensate hardware delay
        else:
            # we want stable 12V on the CP, so we set the PWM to 100%
            # Deviation: The BeagleBone Black produces a ~20ns negative spike even if
            # we here set 100%. This is faster than the power stage can react -> tolerable.
            f.write("1000000")


# Step 1: switch the PWM pin P9_42 to function "pwm"
# (bash) config-pin -q P9_42
# shows that the pin is in default mode, so it does not make pwm. We change it to PWM mode:
# (bash) config-pin P9_42 pwm
print("changing P9_42 to pwm")
os.system("config-pin P9_42 pwm")

# Step 2: configure the period and duty cycle, and turn the PWM on.
print("setting periode, duty and enable for P9_42")
# For P9_42: chip=0, channel=0
pwmbase = "/sys/class/pwm/pwmchip0/pwm0/"

with open(pwmbase + "period", "w") as f:
	f.write("1000000")

setPwmFivePercent(True)

with open(pwmbase+ "enable", "w") as f:
	f.write("1")

print("PWM configured. Entering endless loop for CP-PWM control. Press ctrl-C to abort.")


isDemo = False
while True:
    # read voltage
    # control the PWM
    sleep(0.2)
    if (isDemo):
        setPwmFivePercent(True)
        sleep(2)
        setPwmFivePercent(False)
        sleep(4)
    else:
        pass
        # Todo: read the voltage on the PWM pin. Turn the PWM on if the voltage changes from 12V to 9V (state B).
        #  Turn the PWM off if the voltage is back at 12V (state A).    
