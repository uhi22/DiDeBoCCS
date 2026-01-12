# DiDeBoCCS - The Discharge Demo Box for CCS

Demonstrator for discharging a car via CCS connector

## Version 1

Work in progress, based on the FoccciCape

- Started here: https://openinverter.org/forum/viewtopic.php?p=87270#p87270
- instructions to setup the BeagleBone https://openinverter.org/forum/viewtopic.php?p=87295#p87295

### initial setup

#### Variant A - standalone (not recommended?)

Preconditions:
- BeagleBone Black. This has an AM335x.
- SD card (e.g. 32GB SanDisk) connected to Windows10 via USB card reader

Installation Steps:
- We want a graphical desktop, so we do NOT choose the IoT variant of the image.
- E.g. image "Debian 11.x (Bullseye) Xfce Desktop Snapshot" from https://forum.beagleboard.org/t/debian-11-x-bullseye-monthly-snapshot-2023-10-07/31280
so we download am335x-debian-11.8-xfce-armhf-2023-10-07-4gb.img.xz
- download the imager tool, which can burn the image to the microSD card. https://www.beagleboard.org/bb-imager
- install the imager tool and start it
- in the imager tool, select the board (BeagleBone Black) and the image (custom image -> am335x-debian-11.8-xfce-armhf-2023-10-07-4gb.img.xz), and the SD card as destination.
- Start flashing the image and wait until flashing is completed.
- Remove the SD card from the SD card reader and put it into the beaglebone black.
- Connect mouse and keyboard to the beaglebone black via an USB hub.
- Connect monitor to the beaglebone black with microHDMI cable.
- Hold S2 and connect 5V to the power connector of the beaglebone black. (When not holding the S2 while powering-on, the beaglebone will boot from internal eMMC instead of SD card. This is not what we want.
- LEDs are blinking and mouse cursor appears on (black) screen. After ~3 minutes the desktop appears.

#### Variant B - with host PC

- No SD card needed during operation, only for updating the image on the eMMC.
- connect beaglebone black (BBB) to the PC via mini-USB cable
- after some seconds, the BBB appears as mass storage (lets say it is drive E:)
- open the E:\README.htm
- install the drivers (for Win10: use E:\Drivers\Windows\BONE_D64.exe. If this fails, a likely root cause is that the signature of the driver is not accepted by windows 10. To work-around this, you need to disable driver signature enforcement before installing drivers if you are using Windows 10. Go to Setting > Updates & Security > Recovery > Advanced startup > click on Restart. After restarting, Windows switch to Advanced startup mode. Go to Troubleshoot > Advanced options > Startup settings > click on Restart. After restarting, press F7 to select Disable driver signature enforcement. Now you can install drivers for your board. This was explained in this tutorial https://youtu.be/mxMMf-8d6x4
- if the drivers are successfully installed, the BBB shall be reachable via http, e.g. http://192.168.7.2/bone101/Support/BoneScript/demo_blinkled/ where we can press the RUN button to blink the USR3 LED.
- putty and tightvnc: see https://www.youtube.com/watch?v=c81tmb7WJxw (this uses a network cable)
- SSH using putty also works via USB. Connect to 192.168.7.2. Login: root, no password.
- Install tightVNC on the desktop PC
- Install tightvnc server on the BBB using putty:
    - sudo apt-get install tightvncserver
    - tightvncserver PW (e.g. 12121212)
    - vncserver :1 -geometry 1280x800 -depth 24 -dpi 96
- on PC: open tightVNC viewer, connect to 192.168.7.2:1. Use the above defined VNC password.
- on PC, you see the desktop of the BBB. Open an LX terminal on this desktop.
- cloning a repository from github.com does not work in this setup, because the PC does not route the needed internet traffic to the USB network. Solution: Connect the BBB to internet router via network cable.
- after restart with network cable connected to the internet router, the SSH (putty) and the web server over USB (192.168.7.2) does not work anymore. So we need to use the Ethernet way, e.g. 192.168.2.112 (look into your router and search for "beaglebone").
- ifconfig should show that eth0 got ip-addresses
- ping github.com should work now
- mkdir myprogs
- install pyPLC (similar to installation on raspberry, https://github.com/uhi22/pyPLC/blob/master/doc/installation_on_raspberry.md)
    - cd myprogs
    - git clone https://github.com/uhi22/pyPLC
    - git clone http://github.com/uhi22/OpenV2Gx
    - cd OpenV2Gx/Release
    - make
    - We get an compile error regarding declaration in for loop. With the commit https://github.com/uhi22/OpenV2Gx/commit/ae21bce8acd8b4c183de9be95e5dfbad0022c68b this is fixed.
    - `make clean`, `make`
- `cd /root/myprogs/pyPLC`
- try to start pyPLC in EVSE mode: `sudo python3 pyPlc.py E`
- Python complains about `No module named _tkinter`. Todo: how to install tkinter?
- Should we update to a more recent debian version?  `cat /etc/debian_version` says `7.9`
    - incl desktop, for flashing the eMMC: "AM335x 11.7 2023-09-02 4GB eMMC Xfce Flasher" https://files.beagle.cc/file/beagleboard-public-2021/images/am335x-eMMC-flasher-debian-11.7-xfce-armhf-2023-09-02-4gb.img.xz
    - open beagleBoardImager, select beagle bone black and the image mentioned above, and a microSD drive. Burn the image to the microSD card.
    - power-down the BBB. Insert the microSD card into the BBB. Hold the S2 button and power-on. If 4 LEDs are on, release the S2 button.
    - after some blinking the LEDs will show "knight rider" pattern for several minutes. This indicates that the update is running. Finially all LEDs are off (or maybe steady on).
    - Power off, remove SD card, power on.
    - connect to network cable and power. Not USB.
    - putty connect to 192.168.2.112 (check in the router for "beaglebone" to find out the IP address)
    - username:password is debian:temppwd
    - `cat /etc/debian_version` now reports `11.7`
    - change password to debian `passwd`
- again try to install pyPLC
- but the eMMC disk is already nearly full:
```
df
Filesystem     1K-blocks    Used Available Use% Mounted on
udev              215500       0    215500   0% /dev
tmpfs              49404    1344     48060   3% /run
/dev/mmcblk1p1   3592716 3338636     51124  99% /
```
- so which version to install? Trying https://www.beagleboard.org/distros/am335x-11-7-2023-09-02-4gb-emmc-iot-flasher
Result after installing this on the eMMC and connecting with putty:
```
debian@BeagleBone:~$ df
Filesystem     1K-blocks    Used Available Use% Mounted on
udev              218148       0    218148   0% /dev
tmpfs              49404    1316     48088   3% /run
/dev/mmcblk1p1   3592716 2027576   1362184  60% /
tmpfs             247004       0    247004   0% /dev/shm
tmpfs               5120       0      5120   0% /run/lock
tmpfs              49400       0     49400   0% /run/user/1000
debian@BeagleBone:~$ pwd
/home/debian
debian@BeagleBone:~$ cat /etc/debian_version
11.7
debian@BeagleBone:~$ python --version
Python 3.9.2
```

- again try to install pyPLC

```
mkdir myprogs
cd myprogs
git clone https://github.com/uhi22/pyPLC
git clone http://github.com/uhi22/OpenV2Gx
cd OpenV2Gx/Release
make
cd /home/debian/myprogs/pyPLC/
```

- try to run plPLC in EVSE mode without graphical user interface `python evseNoGui.py`
- result: pcap is not found. Install it: `python -m pip install --upgrade pcap-ct` and `sudo python -m pip install --upgrade pcap-ct`

prepare the ini file with the settings for pyPLC:

```
cd /home/debian/myprogs/pyPLC/docs
cp pyPlc.ini.template ./../pyPlc.ini
cd ..
nano pyPlc.ini
```

- install the "requests" python module
```
pip install requests
sudo pip install requests
```

- `sudo python evseNoGui.py` works now. (still on eth0. No QCA driver yet.)

Find out the kernel version:

```
debian@BeagleBone:~/myprogs/pyPLC$ uname -r
5.10.168-ti-r71
```


## Version 0

The test setup consists of
- notebook running pyPLC
- PLC modem
- arduino-based circuit which creates the 5% PWM on the control pilot
- two 230V light bulbs in series

Details can be found here:
- https://github.com/uhi22/pyPLC/blob/master/doc/EvseMode.md
- https://openinverter.org/forum/viewtopic.php?p=55942#p55942
- Demonstration video on Touran: https://www.youtube.com/watch?v=JHgeRtUz0qU
