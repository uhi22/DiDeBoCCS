# DiDeBoCCS - The Discharge Demo Box for CCS

Demonstrator for discharging a car via CCS connector

## Version 1: FoccciCape and BeagleBone

![image](doc/2026-01-31_FoccciCape_on_Ioniq_with_bulbs.jpg)

- Demonstration video on Touran https://youtu.be/jTx41aqIouk
- Demonstration video on Ioniq https://youtu.be/E4KNq4u5nmQ
- Detailled setup-guide [setup_focccicape.md](setup_focccicape.md)

## Version 0: With Homeplug modem and Laptop

The test setup consists of
- notebook running pyPLC
- PLC modem
- arduino-based circuit which creates the 5% PWM on the control pilot
- two 230V light bulbs in series

Details can be found here:
- https://github.com/uhi22/pyPLC/blob/master/doc/EvseMode.md
- https://openinverter.org/forum/viewtopic.php?p=55942#p55942
- Demonstration video on Touran: https://www.youtube.com/watch?v=JHgeRtUz0qU
