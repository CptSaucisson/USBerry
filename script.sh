#!/bin/sh

LOG="/var/log/usberry.log"

echo "_____________________" >> $LOG

echo "USB storage detected $1" >> $LOG

nohup python /home/olbaid/Documents/USBerry/launch-scan.py $1 &