# DiDeBoCCS - The Discharge Demo Box for CCS

Demonstrator for discharging a car via CCS connector

## Version 1

Work in progress, based on the FoccciCape

- Started here: https://openinverter.org/forum/viewtopic.php?p=87270#p87270
- instructions to setup the BeagleBone https://openinverter.org/forum/viewtopic.php?p=87295#p87295

### initial setup

#### Connection Variant A - standalone with boot from SD (not recommended)

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

Conclusion: Not practicable, because holding the boot button each time is not possible. Slow booting.

#### Connection Varient B - standalone with boot from eMMC (not recommended)

Conclusion: Not helpful, because the 4GB eMMC is already full after installing the full-blown desktop image.

#### Connection Variant C - with host PC via USB (not recommended)

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
- cloning a repository from github.com does not work in this setup, because the PC does not route the needed internet traffic to the USB network. Solution: Connect the BBB to internet router via network cable. Now the USB connection does not make much sense. Go to Variant D.

#### Connection Variant D - SSH (recommended)

We use the ethernet socket of the BBB for connecting to the local network. We connect via SSH from the PC (using Putty). File transfer is easy with scp.
Putty finds the BBB by using the name "beaglebone.local". If not, look in your router which IP address the beaglebone got. As a backup solution, you can connect a HDMI display and a keyboard directly to the BBB, and use ifconfig to find out the network settings and status.

- ping github.com works now

#### Image variants

The beagle bone website offer a lot of different images. They differ in multiple dimensions:
- content (minimal, IoT, desktop)
- intended to be run on SD or intended to flash automatically the eMMC 
- different linux versions

Decision criterias:
- we need a small image because the 4GB eMMC is limited.
- we need to flash the eMMC
- we need a half-way up-to-date system

For flashing an image to the eMMC there seem to be different ways (otherwise it would be too easy): Images which have "flasher" in the name, but newer images are not coming as "flasher", instead the "normal" images can be somehow transferred to the eMMC by commands like described in https://forum.beagleboard.org/t/emmc-not-found-beagle-bone-black-flasher-fails/37066/7, but this did not work.

So the working path is: use a minimal "flasher" image.

Let's use https://forum.beagleboard.org/t/debian-11-x-bullseye-monthly-snapshot-2023-10-07/31280
am335x-eMMC-flasher-debian-11.8-minimal-armhf-2023-10-07-2gb.img.xz

##### Boot-Issue: BeagleBone does not boot anymore.

4 LEDs are permenent on. No matter whether trying to boot from eMMC or SD. It is not clear what killed the BBB. Only solution: use a new one.

##### Imager issues

The combination of "bad" SD cards and BeagleBoneImager is not a good idea. The BeagleBoneImager pretents that it has flashed the image, but in fact the data on the SD card was corrupted. Recommendation: Use Etcher. This gives error messages if the write fails, and makes a verification. And do not buy the cheapest SD cards you can find.
Even considering these hints, the process is quite instable. During verification step, we got kicked-out (windows driver issues???) but at least the image was written. Multiple trials before ended in abort during writing the image.

##### Conclusion for flashing the image

- use am335x-eMMC-flasher-debian-11.8-minimal-armhf-2023-10-07-2gb.img.xz
- use a reliable SD card.
- use balena Etcher (not BeagleBoardImager) to write the image to the SD card.
 power-down the BBB. Insert the microSD card into the BBB. Hold the S2 button and power-on. If 4 LEDs are on, release the S2 button.
- after some blinking the LEDs will show "knight rider" pattern for several minutes. This indicates that the update is running. Finially all LEDs are off (or maybe steady on).
- Power off, remove SD card, power on.
- connect to network cable and power. Not USB. From PC, use putty to connect to beaglebone.local (or check in the router for "beaglebone" to find out the IP address)
- username:password is debian:temppwd
- `cat /etc/debian_version` now reports `11.7`
- Find out the kernel version:
```
debian@BeagleBone:~$ uname -r
5.10.168-ti-r72
debian@BeagleBone:~$ uname --all
Linux BeagleBone 5.10.168-ti-r72 #1bullseye SMP PREEMPT Sat Sep 30 03:37:21 UTC
2023 armv7l GNU/Linux
```

##### Install pyPLC

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


```
/*
 * Copyright (C) 2019 Tomas Arturo Herrera Castro <taherrera@uc.cl>
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License version 2 as
 * published by the Free Software Foundation.
 * 
 * Written as part of my master's thesis at PUC Chile,
 * to run the BeagleBone as an OpenThread Border Router w/o an NCP.
 *
 * https://www.sltech.cl
 *
 * Compiled using: make ./src/arm/BB-SPI0-QCASPI-00A0.dtbo
 *
 * Tested on BeagleBone Black Rev. C + REB233-XPRO. Linux beaglebone 4.14.71-ti-r80.
 *
 */

/dts-v1/;
/plugin/;

#include <dt-bindings/board/am335x-bbw-bbb-base.h>
#include <dt-bindings/pinctrl/am33xx.h>
#include <dt-bindings/interrupt-controller/irq.h>

/ {
	/*
	 * Helper to show loaded overlays under: /proc/device-tree/chosen/overlays/
	 */
	fragment@0 {
		target-path="/";
		__overlay__ {

			chosen {
				overlays {
					BB-SPI0-QCASPI-00A0 = __TIMESTAMP__;
				};
			};
		};
	};

	/*
	 * Free up the pins used by the cape from the pinmux helpers.
	 */
	fragment@1 {
		target = <&ocp>;
		__overlay__ {
			P9_17_pinmux { status = "disabled"; };	/* P9_17 (A16) spi0_cs0.spi0_cs0 */
			P9_18_pinmux { status = "disabled"; };	/* P9_18 (B16) spi0_d1.spi0_d1 */
			P9_21_pinmux { status = "disabled"; };	/* P9_21 (B17) spi0_d0.spi0_d0 */
			P9_22_pinmux { status = "disabled"; };	/* P9_22 (A17) spi0_sclk.spi0_sclk */

			P9_15_pinmux { status = "disabled"; };	/* irq P9_15 (R13) gpmc_a0.gpio1[16] */
		};
	};

	fragment@2 {
		target = <&am33xx_pinmux>;
		__overlay__ {
			bb_qca_pins: bb_qca_pins {
				pinctrl-single,pins = <
					AM33XX_PADCONF(AM335X_PIN_GPMC_A0, PIN_INPUT_PULLDOWN, MUX_MODE7)    /* irq P9_15 (R13) gpmc_a0.gpio1[16] */
				>;
			};
			spi0_qca_s0: spi0_qca_s0 {
				pinctrl-single,pins = <
					AM33XX_PADCONF(AM335X_PIN_SPI0_SCLK, PIN_INPUT, MUX_MODE0) /* P9_22 (A17) spi0_sclk.spi0_sclk */
					AM33XX_PADCONF(AM335X_PIN_SPI0_D0, PIN_INPUT, MUX_MODE0)   /* P9_21 (B17) spi0_d0.spi0_d0 */
					AM33XX_PADCONF(AM335X_PIN_SPI0_D1, PIN_INPUT, MUX_MODE0)   /* P9_18 (B16) spi0_d1.spi0_d1 */
					AM33XX_PADCONF(AM335X_PIN_SPI0_CS0, PIN_INPUT, MUX_MODE0)  /* P9_17 (A16) spi0_cs0.spi0_cs0 */
				>;
			};
		};
	};

	fragment@3 {
		target = <&spi0>;
		__overlay__ {
			#address-cells = <1>;
			#size-cells = <0>;

			status = "okay";
			pinctrl-names = "default";
			pinctrl-0 = <&spi0_qca_s0>;

			eth1: qcaspi@0 {
				compatible = "qca,qca7000";

				pinctrl-names = "default";
				pinctrl-0 = <&bb_qca_pins>;

				spi-max-frequency = <12000000>;
				reg = <0>;
				interrupt-parent = <&gpio1>;
				interrupts = <16 IRQ_TYPE_EDGE_RISING>; /* gpio1[16] active high */
			};
		};
	};
	
};
```

cd /opt/source/bb.org-overlays/src/arm/
nano BB-SPI0-QCASPI-00A0.dts
and paste the file content from the forum.

Step 2: Compile and install the overlay

cd /opt/source/bb.org-overlays/
make
This should lead to the following files:
```
cd /opt/source/bb.org-overlays/src/arm
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
cd /lib/firmware
debian@BeagleBone:/lib/firmware$ ls -al | grep QCA
-rw-r--r--  1 root root    1720 Jan 25 20:58 BB-SPI0-QCASPI-00A0.dtbo
```

Load the overlay at boot by editing /boot/uEnv.txt
sudo nano /boot/uEnv.txt
Add: dtb_overlay=/lib/firmware/BB-SPI0-QCASPI-00A0.dtbo

Step 3 Kernel Configuration

Ensure the QCA7000 driver is enabled in your kernel. Check if the module exists:

```
debian@BeagleBone:/lib/firmware$ modinfo qcaspi
modinfo: ERROR: Module qcaspi not found.
```
This means, the kernel does not yet contain the QCA driver.

Step 4 Build the Kernel with QCA support --- Attention, this is a mess --- todo cleanup the description

debian@BeagleBone:/lib/firmware$ uname -r
5.10.168-ti-r72

sudo apt-get update
sudo apt-get install -y git build-essential libncurses5-dev libssl-dev bc bison flex lzop u-boot-tools device-tree-compiler lsb-release lz4 man-db gettext pkg-config libmpc-dev zstd libdw-dev

mkdir ~/kernel
cd ~/kernel
git clone https://github.com/RobertCNelson/bb-kernel.git
cd bb-kernel
git checkout origin/am33x-v5.10 -b am33x-v5.10

(df shows that this disk is 91% full already, `/dev/mmcblk1p1   1804184 1533468    160740  91% /`)

./build_kernel.sh

runs into error:
remote: Finding sources: 100% (2744/2744)
fatal: Out of memory, calloc failed

```
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
```

Same error on a newer BBB with 4GB eMMC, where the df shows this:
`/dev/mmcblk1p1   3592716 1370808   2018952  41% /`

The error message `fatal: Out of memory, calloc failed` indicates missing RAM space. A solution is to add swap space. (This is slow, because missing RAM is trying to be compensated by place on the eMMC memory.)

- Create a swap file (this example creates a 1GB swap file): sudo fallocate -l 1G /swapfile
- Set the correct permissions: sudo chmod 600 /swapfile
- Set up the swap area: sudo mkswap /swapfile
- Enable the swap file: sudo swapon /swapfile
- Verify it's working: sudo swapon --show
- free -h
- Make it permanent: To automatically enable the swap file on boot, add this line to /etc/fstab: echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
- Adjust swappiness: The "swappiness" value controls how aggressively the system uses swap. Lower values mean it prefers RAM. For a kernel compilation workload, you might want: sudo sysctl vm.swappiness=10
- To make this permanent, add vm.swappiness=10 to /etc/sysctl.conf.

Try to build the kernel again: `./build_kernel.sh`
Result: better, but during cloning into '/home/debian/kernel/bb-kernel/ignore/linux-src' the 4GB eMMC fills from 72% to 100%, so the build fails: `fatal: write error: No space left on device 946.58 MiB | 1.23 MiB/s`

Conclusion: Building the linux kernel on a 4GB eMMC does not work in this way.
Next option: try cross-compiling on an other machine.

#### Cross compiling on windows 10 machine using WSL2

- powershell as admin. `wsl --install` This installs Ubuntu as "Windows Subsystem For Linux".
- restart the PC.
- startmenu -> Ubuntu
- sudo apt update
- sudo apt install git build-essential libncurses-dev bison flex libssl-dev bc gcc-arm-linux-gnueabihf
- cd ~
- mkdir linuxkernels
- cd linuxkernels
- git clone https://github.com/beagleboard/linux.git
- cd linux
- git checkout 5.10.168-ti-r72
- make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- menuconfig
- In menuconfig, navigate to enable QCA7000:

Device Drivers --->
    Network device support --->
        Ethernet driver support --->
            Qualcomm devices (NEW) --->
                <M> Qualcomm Atheros QCA7000 SPI support
- save and exit the menuconfig.
- Explanation: The <M> means, we want the qca driver to be a "module". This is a piece of software which the linux kernel can load on demand, in contrast to the "built-in", which are always loaded. The "modules" are stored as .ko (kernel object) files.

- make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- -j$(nproc) zImage dtbs modules
- this will create:
    - Kernel: arch/arm/boot/zImage
    - Device trees: arch/arm/boot/dts/*.dtb
    - Modules: the .ko files. This is what we need.

- after compilation, find the wanted .ko files
```
uwemi@DESKTOP-OKFJ35V:~/linuxkernels/linux$ find . -name "*.ko" | grep qca
./drivers/net/ethernet/qualcomm/qca_7k_common.ko
./drivers/net/ethernet/qualcomm/qcaspi.ko
```

- copy the two .ko from the PC to the beaglebone, e.g. using secureCopy (scp)
```
uwemi@DESKTOP-OKFJ35V:~/linuxkernels/linux$ scp ./drivers/net/ethernet/qualcomm/*.ko debian@beaglebone.local:/home/debian/
Debian GNU/Linux 11

BeagleBoard.org Debian Bullseye Minimal Image 2023-10-07
Support: https://bbb.io/debian
default username:password is [debian:temppwd]

debian@beaglebone.local's password:
qca_7k_common.ko                                                                                                100% 4424   573.7KB/s   00:00
qcaspi.ko                                                                                                       100%   26KB   1.3MB/s   00:00
```

- on the BBB, copy the .ko to the place where the kernel expects it. This is /lib/modules/$(uname -r)/kernel/drivers/net/ethernet/qualcomm.

```
cd /lib/modules/5.10.168-ti-r72/kernel/drivers/net/ethernet/qualcomm
sudo cp ~/*.ko .
```

- check:
```
debian@BeagleBone:/lib/modules/5.10.168-ti-r72/kernel/drivers/net/ethernet/qualcomm$ ls -al
total 44
drwxr-xr-x 2 root root  4096 Jan 26 17:46 .
drwxr-xr-x 5 root root  4096 Jan 26 17:45 ..
-rw-r--r-- 1 root root  4424 Jan 26 17:46 qca_7k_common.ko
-rw-r--r-- 1 root root 27016 Jan 26 17:46 qcaspi.ko
```

- Now we have the .ko files in the correct place, but the kernel is not yet aware of them. Run `sudo depmod -a` to update the dependencies. In summary: depmod -a = "Update the module dependency database so modprobe knows how to load modules correctly"

Result:
- `sudo modprobe qcaspi` says `Exec format error`
- `dmesg | grep qca` complains about mismatch of the version magic. This is preventing the loading. qca_7k_common: version magic '5.10.168 SMP mod_unload ARMv7 p2v8 ' should be '5.10.168-ti-r72 SMP preempt mod_unload modversions ARMv7 p2v8 '
- `modinfo qcaspi` confirms that the .ko has the version magic without the "-ti-r72": "vermagic:       5.10.168 SMP mod_unload ARMv7 p2v8"
- conclusion: The cross-compiling did not lead to the correct version magic, even if we checked-out the correct commit. Strange.

Three possible options to proceed:

- (A) native-build only the two .ko files on the BBB.
- (B) find out, how to get the exact version on PC
- (C) transfer the complete kernel from the PC to the BBB, to have full consistency. (not chosen if other options work)

#### For Option (A): Natively compile only the two .ko files

uname -r
5.10.168-ti-r72
sudo apt install linux-headers-5.10.168-ti-r72
But how to compile the sources into a .ko, and how to satisfy the "sudo depmod -a"?

#### For Option (B): Configure the exact version on the PC

Multiple points to check:
- the tag in the checkout command needs to be correct. This was already fulfilled.
- the .config needs to be used from the BBB.
    - # On BeagleBone, check if config is available
    - zcat /proc/config.gz > running_config
    - # Copy to your PC
    - scp debian@beaglebone.local:~/running_config ~/linuxkernels/linux/.config
    - This overwrites the settings which have been made in the menuconfig, so we need to enable the QCA again.
- Check the makefile: `~/linuxkernels/linux$ nano Makefile` and change the empty entry correcty: EXTRAVERSION = -ti-r72
- Set the architecture
    - export ARCH=arm
    - export CROSS_COMPILE=arm-linux-gnueabihf-
- If we use menuconfig to activate the QCA, this could lead to change of version magic. But we have no other chance.
make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- olddefconfig
make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- menuconfig
make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- prepare
make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- modules_prepare

To safe time, we you build just the QCA objects `make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- M=drivers/net/ethernet/qualcomm modules` but this leads to errors.

So we do a full build (needs ~2 hours on an slow i5).

make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf-

find drivers/net/ethernet/qualcomm -name "*.ko"

copy the two .ko files on beaglebone into /lib/modules/5.10.168-ti-r72/kernel/drivers/net/ethernet/qualcomm
sudo depmod -a
sudo modprobe qcaspi
dmesg | grep qca

This does not show the compatibility error anymore. It shows the missing QCA communication, which is normal when no FoccciCape is connected.
So shutdown and install the foccciCape.
Observation: after applying 5V to the BBB DC jack, all LEDs stay off. Pushing the power-button brings the BBB back to life.

SUCCESS: The BBB finds the QCA.

```
debian@BeagleBone:~$ dmesg | grep qca
[   41.659782] qcaspi spi0.0: ver=0.2.7-i, clkspeed=12000000, burst_len=5000, pluggable=0
[   41.660168] qcaspi spi0.0: Using random MAC address: 6e:85:7e:4d:21:8f
[   54.431229] qcaspi spi0.0 eth1: SPI thread created
debian@BeagleBone:~$ uname -r
5.10.168-ti-r72
debian@BeagleBone:~$ modinfo qcaspi
filename:       /lib/modules/5.10.168-ti-r72/kernel/drivers/net/ethernet/qualcomm/qcaspi.ko
version:        0.2.7-i
license:        Dual BSD/GPL
author:         Stefan Wahren <stefan.wahren@i2se.com>
author:         Qualcomm Atheros Communications
description:    Qualcomm Atheros QCA7000 SPI Driver
srcversion:     41C3E0CD499A4984F2E7663
alias:          of:N*T*Cqca,qca7000C*
alias:          of:N*T*Cqca,qca7000
alias:          spi:qca7000
depends:        qca_7k_common
intree:         Y
name:           qcaspi
vermagic:       5.10.168-ti-r72+ SMP preempt mod_unload modversions ARMv7 p2v8
parm:           qcaspi_clkspeed:SPI bus clock speed (Hz). Use 1000000-16000000. (int)
parm:           qcaspi_burst_len:Number of data bytes per burst. Use 1-5000. (int)
parm:           qcaspi_pluggable:Pluggable SPI connection (yes/no). (int)
parm:           wr_verify:SPI register write verify trails. Use 0-3. (int)
debian@BeagleBone:~$ modinfo qca_7k_common
filename:       /lib/modules/5.10.168-ti-r72/kernel/drivers/net/ethernet/qualcomm/qca_7k_common.ko
license:        Dual BSD/GPL
author:         Stefan Wahren <stefan.wahren@i2se.com>
author:         Qualcomm Atheros Communications
description:    Qualcomm Atheros QCA7000 common
depends:
intree:         Y
name:           qca_7k_common
vermagic:       5.10.168-ti-r72+ SMP preempt mod_unload modversions ARMv7 p2v8
debian@BeagleBone:~$ ip link show
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP mode DEFAULT group default qlen 1000
    link/ether 04:a3:16:b0:ec:67 brd ff:ff:ff:ff:ff:ff
3: usb0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc pfifo_fast state DOWN mode DEFAULT group default qlen 1000
    link/ether 04:a3:16:b0:ec:6a brd ff:ff:ff:ff:ff:ff
4: usb1: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc pfifo_fast state DOWN mode DEFAULT group default qlen 1000
    link/ether 04:a3:16:b0:ec:6c brd ff:ff:ff:ff:ff:ff
5: eth1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP mode DEFAULT group default qlen 100
    link/ether ba:f0:f2:e5:43:a4 brd ff:ff:ff:ff:ff:ff
6: can0: <NOARP,ECHO> mtu 16 qdisc noop state DOWN mode DEFAULT group default qlen 10
    link/can
7: can1: <NOARP,ECHO> mtu 16 qdisc noop state DOWN mode DEFAULT group default qlen 10
    link/can
debian@BeagleBone:~$ cd /proc/device-tree/chosen/overlays
debian@BeagleBone:/proc/device-tree/chosen/overlays$ ls -al
total 0
drwxr-xr-x 2 root root  0 Jan 27 08:48 .
drwxr-xr-x 3 root root  0 Jan 27 08:48 ..
-r--r--r-- 1 root root 25 Jan 27 08:48 BB-ADC-00A0.kernel
-r--r--r-- 1 root root 25 Jan 27 08:48 BB-BONE-eMMC1-01-00A0.kernel
-r--r--r-- 1 root root 25 Jan 27 08:48 BB-HDMI-TDA998x-00A0.kernel
-r--r--r-- 1 root root 25 Jan 27 08:48 BB-SPI0-QCASPI-00A0
-r--r--r-- 1 root root  9 Jan 27 08:48 name
```

#### Commands for Verification and trouble shooting

```
modinfo qcaspi
ip link show
dmesg | grep qca

Check SPI devices
ls /dev/spi*

Check kernel logs
dmesg | tail -50

Verify device tree overlay loaded
cd /proc/device-tree/chosen/overlays
ls -al
```


#### First steps with the QCA

```
sudo apt update
sudo apt install git build-essential libpcap-dev
cd ~/myprogs
git clone https://github.com/qca/open-plc-utils.git
cd open-plc-utils
make
sudo make install
sudo plctool -i eth1 -I
debian@BeagleBone:~/myprogs$ plctool -i eth1 -I
        PIB 0-0 8080 bytes
        MAC 04:65:65:FF:FF:00
        DAK 68:9F:07:4B:8B:02:75:A2:71:0B:0B:57:79:AD:16:30 (HomePlugAV)
        NMK 77:77:DB:90:BD:44:4B:77:77:77:77:77:77:77:77:77
        NID 01:02:A5:30:46:15:07
        Security level 0
        NET Qualcomm Atheros Enabled Network
        MFG Qualcomm Atheros HomePlug AV Device
        USR EVSE
        CCo Always
        MDU N/A
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
