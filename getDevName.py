#!/usr/bin/python

import sys
import pyudev
import time

if __name__ == '__main__':
    if(len(sys.argv) != 2):
        print("NEED Mounted Kernel")
        sys.exit(1)
    
    time.sleep(15)
    #print("starting with kernel :"+sys.argv[1]+"\n") 
    
    context = pyudev.Context()
    usb = None
    for device in context.list_devices(subsystem='block'):
        try:
            #print(">"+str(device.device_node)+" <==> "+str(device.device_path))
            if(sys.argv[1] in device.device_path):
                #print(device)
                usb = device
                break
        except Exception as e:
            #print(e)
            sys.exit(1)

    path = usb.device_node
    print(path)

