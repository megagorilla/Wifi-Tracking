#!/bin/sh

if [ "$(id -u)" != "0" ]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi

killall airodump-ng
service network-manager restart

cd /var/log/
echo "" > syslog
echo "" > daemon.log

airmon-ng | grep mon | cut -c 1-4 | while read -r line ; do
	echo "Processing $line"
	iw dev $line del
done

