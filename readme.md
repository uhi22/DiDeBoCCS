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

#### New issue: BeagleBone does not boot anymore.

4 LEDs are permenent on. No matter whether trying to boot from eMMC or SD.

#### Finding a way how to start with a clean setup

Try new setup:
- new BBB
- new SD card (samsung) in new SD card reader
- BeagleBoard Imager v0.0.17, image Debian 12 v6.12.x (LTS-Dec-2026) 2026-01-22
- Result: This boots the version 2026-01-22 (visible on HDMI) find, if the button S2 is hold. But it does boot the old 2023-04-06 image if we power up the BBB without SD card. --> not helpful.

Next try: search an image. Starting at https://www.beagleboard.org/distros and searching for "Flasher"
Taking the "IoT Flasher" am335x-eMMC-flasher-debian-11.7-iot-armhf-2023-09-02-4gb.img.xz
```
AM335x 11.7 2023-09-02 4GB eMMC IoT Flasher

Debian image for BeagleBone Black on-board eMMC flash Kernel: 5.10.168-ti-r71 U-Boot: v2022.04 default username:password is [debian:temppwd] For flashing instructions or other images, see https://forum.beagleboard.org/t/debian-11-x-bullseye-monthly-snapshot-2023-09-02/31280
```
But somehow this does not lead to flashing the eMMC. Discussion about an other way to flash the eMMC:
https://forum.beagleboard.org/t/emmc-not-found-beagle-bone-black-flasher-fails/37066/7
Not clear whether this works.

#### New trial using Etcher and a known-good-flasher image

Alternative tool for writing the image: balena Etcher.
For the am335x-eMMC-flasher-debian-11.7-iot-armhf-2023-09-02-4gb.img.xz it complains that this is broken. (In the end it is not clear, what is the root cause. Windows diskutil also showed problems with the microSD (not possible to delete the strange partitions). Other card works sporadically better, so maybe also a windows driver issue. At least, the Etcher shows an error message. The beagleBoneImager just looks like "finished" even if the image was not fully written to the SD card.)
Trying with 2023-10-07, from https://forum.beagleboard.org/t/debian-11-x-bullseye-monthly-snapshot-2023-10-07/31280
am335x-eMMC-flasher-debian-11.8-minimal-armhf-2023-10-07-2gb.img.xz

Flashing this image using Etcher to a 32GB microSD. During verification step, we got kicked-out (windows driver issues???) but at least the image was written. Multiple trials before ended in abort during writing the image. Quite instable situation.

Power-on the BBB while microSD card is in, and S2 button is hold. Shows "knight rider" LED pattern, this is a good sign. After some minutes, all LEDs are off. Remove microSD, and re-power. HDMI and keyboard connected.
On HDMI display, it shows "Debian Bullseye Minimal Image 2023-10-07" as expected.

- Using HDMI display and USB keyboard, log in with debian/temppwd. This works.
- sudo shutdown now
- disconnect power, connect LAN, re-power.
- on hdmi/usbkeyboard: log in, ifconfig. This shows the IP address.
- use Putty to connect from the windows PC to the BBB via SSH.
- Find out the kernel version:
```
debian@BeagleBone:~$ uname -r
5.10.168-ti-r72
debian@BeagleBone:~$ uname --all
Linux BeagleBone 5.10.168-ti-r72 #1bullseye SMP PREEMPT Sat Sep 30 03:37:21 UTC
2023 armv7l GNU/Linux
```

- install pyPLC

```
mkdir myprogs
cd myprogs
git clone https://github.com/uhi22/pyPLC
git clone http://github.com/uhi22/OpenV2Gx
cd OpenV2Gx/Release
make
```

- This leads to the error "make: command not found". Root cause: We have a minimal image, which does not contain the build tools. Solution: install build-essential

```
sudo apt-get update
sudo apt install build-essential
```

- Again try to build the OpenV2Gx: `make`. This takes some minutes.
- Test the EXI decoder/encoder

```
cd ~/myprogs/OpenV2Gx/Release
./OpenV2G.exe DD809a0010d0400000c800410c8000
./OpenV2G.exe EDB_5555aaaa5555aaaa
```

This should run without error and show the decoded/encoded data in the command window.

Now we go to the python part.

```
cd ~/myprogs/pyPLC
```

Check python version:
```
debian@BeagleBone:~/myprogs/pyPLC$ python --version
-bash: python: command not found
debian@BeagleBone:~/myprogs/pyPLC$ python3 --version
Python 3.9.2
debian@BeagleBone:~/myprogs/pyPLC$
```
This means: A senseful version of python is already installed.

Install the python library for accessing the network interface. Also for the superuser (otherwise the import pcap fails).

```
debian@BeagleBone:~/myprogs/pyPLC$ python3 -m pip install --upgrade pcap-ct
/usr/bin/python3: No module named pip
```

Means: We first need to install pip: `sudo apt install python3-pip` Then again:

```
debian@BeagleBone:~/myprogs/pyPLC$ python3 -m pip install --upgrade pcap-ct
debian@BeagleBone:~/myprogs/pyPLC$ sudo python3 -m pip install --upgrade pcap-ct
```

`sudo apt install tcpdump`

Try-out whether the python is able to sniff ethernet packets:

```
cd ~/myprogs/pyPLC/tests
sudo python3 test_pcap.py
```

This shows the available network interfaces and runs a loops 0 to 9 showing ethernet traffic.

Try-out the cooperation of Python with the EXI encoder/decoder:

```
cd ~/myprogs/pyPLC
python3 exiConnector.py
```

This shows some message content for demonstation purpose.

Prepare the ini file with the settings for pyPLC:

```
cd ~/myprogs/pyPLC/doc
cp pyPlc.ini.template ./../pyPlc.ini
cd ..
nano pyPlc.ini
```

The important settings for the beginning are:
```
mode = EvseMode
eth_interface = eth0 (later change this to the name of the QCA interface)
display_via_serial = no
digital_output_device = beaglebone
```
- try to run plPLC in EVSE mode without graphical user interface `sudo python evseNoGui.py`

This leads to error message `No module named 'serial'` We need to install the pySerial (normal and as sudo).

Same for Adafruit_BBIO, but this leads to errors. So setting digital_output_device to none in the pyPlc.ini for the moment.

- install the "requests" python module
```
pip install requests
sudo pip install requests
```

- SUCCESS: `sudo python evseNoGui.py` works now. (still on eth0. No QCA driver yet.)

#### Next step: integrate the QCA7000 SPI driver

some description here: https://openinverter.org/forum/viewtopic.php?p=72982#p72982


##### Step-by-step

Step 1: create a device tree source file (.dts)

You'll need to add a device tree overlay to configure the SPI interface and QCA7000 device. Create a device tree source file (.dts) with the content shown in https://openinverter.org/forum/viewtopic.php?p=87295#p87295

cd /opt/source/bb.org-overlays/src/arm/
nano BB-SPI0-QCASPI-00A0.dts
and paste the file content from the forum.

Step 2: Compile and install the overlay

cd /opt/source/bb.org-overlays/
make
This should lead to the following files:
```
debian@BeagleBone:/opt/source/bb.org-overlays/src/arm$ ls -al | grep QCA
-rw-r--r-- 1 debian debian   926 Jan 25 20:51 .BB-SPI0-QCASPI-00A0.dtbo.cmd
-rw-r--r-- 1 debian debian    76 Jan 25 20:51 .BB-SPI0-QCASPI-00A0.dtbo.d.dtc.tmp
-rw-r--r-- 1 debian debian   231 Jan 25 20:51 .BB-SPI0-QCASPI-00A0.dtbo.d.pre.tmp
-rw-r--r-- 1 debian debian  2001 Jan 25 20:51 .BB-SPI0-QCASPI-00A0.dtbo.dts.tmp
-rw-r--r-- 1 debian debian  1720 Jan 25 20:51 BB-SPI0-QCASPI-00A0.dtbo
-rw-r--r-- 1 debian debian  2689 Jan 25 20:45 BB-SPI0-QCASPI-00A0.dts
```

sudo cp /opt/source/bb.org-overlays/src/arm/BB-SPI0-QCASPI-00A0.dtbo /lib/firmware/

Now we have the compiled overlay here:
```
debian@BeagleBone:/lib/firmware$ ls -al | grep QCA
-rw-r--r--  1 root root    1720 Jan 25 20:58 BB-SPI0-QCASPI-00A0.dtbo
```

Load the overlay at boot by editing /boot/uEnv.txt
sudo nano /boot/uEnv.txt
Add: dtb_overlay=/lib/firmware/QCA7000-00A0.dtbo

Step 3 Kernel Configuration

Ensure the QCA7000 driver is enabled in your kernel. Check if the module exists:

```
debian@BeagleBone:/lib/firmware$ modinfo qca_spi
modinfo: ERROR: Module qca_spi not found.
```
This means, the kernel does not yet contain the QCA driver.

Step 4 Build the Kernel with QCA support

debian@BeagleBone:/lib/firmware$ uname -r
5.10.168-ti-r72

sudo apt-get update
sudo apt-get install -y git build-essential libncurses5-dev libssl-dev bc bison flex lzop u-boot-tools device-tree-compiler

mkdir ~/kernel
cd ~/kernel
git clone https://github.com/RobertCNelson/bb-kernel.git
cd bb-kernel
git checkout origin/am33x-v5.10 -b am33x-v5.10

(df shows that this disk is 91% full already, /dev/mmcblk1p1   1804184 1533468    160740  91% /)

Install dependencies for the build: `sudo apt-get install lsb-release lz4 man-db gettext pkg-config libmpc-dev zstd libdw-dev`

./build_kernel.sh

runs into error:
remote: Finding sources: 100% (2744/2744)
fatal: Out of memory, calloc failed

top
top - 21:57:09 up  3:01,  2 users,  load average: 0.01, 0.49, 0.57
Tasks:  89 total,   1 running,  88 sleeping,   0 stopped,   0 zombie
%Cpu(s):  0.0 us,  1.0 sy,  0.0 ni, 99.0 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st
MiB Mem :    482.4 total,     79.9 free,     50.1 used,    352.5 buff/cache
MiB Swap:      0.0 total,      0.0 free,      0.0 used.    419.7 avail Mem

debian@BeagleBone:~/kernel/bb-kernel$ df
Filesystem     1K-blocks    Used Available Use% Mounted on
udev              218748       0    218748   0% /dev
tmpfs              49404    1344     48060   3% /run
/dev/mmcblk1p1   1804184 1560424    133784  93% /
tmpfs             247004       0    247004   0% /dev/shm
tmpfs               5120       0      5120   0% /run/lock
tmpfs              49400       0     49400   0% /run/user/1000





------- untested from here on ------------------------------

In menuconfig, navigate to enable QCA7000:

Device Drivers --->
    Network device support --->
        Ethernet driver support --->
            Qualcomm devices --->
                <M> Qualcomm Atheros QCA7000 support
                <M>   Qualcomm Atheros QCA7000 SPI support

cd ~/kernel/bb-kernel

Edit system.sh to match your kernel version
nano system.sh
Set: kernel_tag="5.10.168-ti-r72"

Build
./build_kernel.sh

Install the kernel
cd ~/kernel/bb-kernel/deploy
sudo ./install_kernel.sh


Step 5 Load the driver

Load the SPI driver if not already loaded
sudo modprobe spi_omap2_mcspi

Load the QCA7000 driver
sudo modprobe qca_spi

Step 6 Verification and trouble shooting

ip link show
dmesg | grep qca

Check SPI devices
ls /dev/spi*

Check kernel logs
dmesg | tail -50

Verify device tree overlay loaded
cd /proc/device-tree/chosen/overlays
ls -al



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
