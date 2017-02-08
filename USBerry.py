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
import os
from subprocess import Popen, PIPE


rulepath = "/etc/udev/rules.d/75-USBerry.rules"
mypath = os.path.dirname(os.path.realpath(__file__)) 
rule = ""


def create_rule():
	tmp = list()
	tmp.append(header)

        with open('baserules.rules') as f:
            for l in f.readlines():
                if(l[0] != '#'):tmp.append(l)


        tmp.append('SUBSYSTEMS=="usb", ATTR{bInterfaceClass}=="08", ACTION=="add", ATTR{authorized}="1", RUN+="'+mypath+'/script.sh", GOTO="usb_end"')
       

        #tmp.append('SUBSYSTEMS=="usb", ATTR{bInterfaceClass}=="08", ACTION=="add", ATTR{authorized}="1", GROUP="USBerry", OWNER="USBerry", MODE="0600", RUN+="'+mypath+'/script.sh", GOTO="usb_end"')

        tmp.append('SUBSYSTEMS=="usb", ATTR{bInterfaceClass}=="09", ACTION=="add", ATTR{authorized}="1", GOTO="usb_end"')
       
        tmp.append('SUBSYSTEMS=="usb", ATTR{bInterfaceClass}!="08", ACTION=="add", ATTR{authorized}="0", RUN="'+mypath+'/script2.sh"')
        
        tmp.append('LABEL="usb_end"')
        global rule
	for s in tmp:
		rule = rule + s + '\n'


def reload_rules():
        p = Popen(["udevadm", "control", "--reload-rules"], stdout=PIPE, stderr=PIPE, stdin=PIPE)
        output, err = p.communicate()
        print "reload : "+str(output)
        print ""+str(err)

def device_event(observer, device):
	print('event {0} on device {1}'.format(device.action, device))


def openhandler():
	open("/etc/udev/rules.d/badusb.rules", "w").write(rule)
	open(mypath+"/logs.log", "a+").write("_______________________\n")

def exithandler():
	open("/etc/udev/rules.d/badusb.rules", "w").write("")
	print("bye bye")
        reload_rules()

atexit.register(exithandler)

def main():
	context = Context()
	monitor = Monitor.from_netlink(context)
	#monitor.filter_by(subsystem='input')
	observer = MonitorObserver(monitor)
        reload_rules()


	observer.connect('device-event', device_event)
	monitor.start()

	for device in iter(monitor.poll, None):
	    print('{0.action} on {0.device_path}'.format(device))
	    print('=> {0} is {2} ({1})'.format(device.device_node, device.device_type, device.driver))






# On crée la rule udev
create_rule()
openhandler()
print(rule)

# On lance le watcher
main()
