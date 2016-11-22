#!/usr/bin/python
# coding: utf8


header = "\
###############################\n\
##  UDEV RULES                #\n\
##  CptSaucisson - USBerry    #\n\
##  v0.1                      #\n\
###############################\n\
"



from pyudev import Context, Monitor
from pyudev.glib import MonitorObserver
import atexit


rulepath = "/etc/udev/rules.d/badusb.conf"
mypath = ""
rule = ""


def create_rule():
	tmp = list()
	tmp.append(header)
	# Block HID
	#tmp.append('BUS=="usb", KERNEL=="hdb", OPTIONS+="ignore_device" RUN+="/home/olbaid/script.sh"\n')
	# Alert
	#OK : tmp.append('ACTION=="add", KERNEL=="sd*", OPTIONS+="ignore_device", RUN+="/home/olbaid/script.sh"\n')
	tmp.append('ACTION=="add", ATTRS{device_blocked}="1", RUN+="/home/olbaid/script.sh", OPTIONS=="ignore_device"\n')

	tmp.append('ACTION=="remove", RUN+="/home/olbaid/script2.sh"\n')

	global rule
	for s in tmp:
		rule = rule + s


def reload_rules():
	pass




def device_event(observer, device):
	print('event {0} on device {1}'.format(device.action, device))


def openhandler():
	open("/etc/udev/rules.d/badusb.rules", "w").write(rule)
	open("/home/olbaid/logs.log", "a+").write("_______________________\n")

def exithandler():
	open("/etc/udev/rules.d/badusb.rules", "w").write("")
	print "bye bye"

atexit.register(exithandler)

def main():
	context = Context()
	monitor = Monitor.from_netlink(context)
	#monitor.filter_by(subsystem='input')
	observer = MonitorObserver(monitor)

	observer.connect('device-event', device_event)
	monitor.start()

	for device in iter(monitor.poll, None):
	    print('{0.action} on {0.device_path}'.format(device))
	    print('=> {0} is {2} ({1})'.format(device.device_node, device.device_type, device.driver))






# On crée la rule udev
create_rule()
openhandler()
print rule

# On lance le watcher
main()
