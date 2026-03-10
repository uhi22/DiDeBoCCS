#!/bin/bash

# Starting tcpdump, each time with a new file name
# To use tcpdump, this script must be ran with sudo.
# To have permissions to the log directory, run chmod 777 logs

index=`cat /home/debian/myprogs/DiDeBoCCS/logs/logindex`
index=$(($index + 1))
pcapfile=`printf "/home/debian/myprogs/DiDeBoCCS/logs/%05d_tcpdump.pcap" $index`
echo "current index is $index"
echo $index > /home/debian/myprogs/DiDeBoCCS/logs/logindex
echo "will start tcpdump with pcapfile $pcapfile"

tcpdump -i eth1 -w $pcapfile

