#!/usr/bin/python

import requests
import json
import os
import glob
import pyudev
import sys
import time
import subprocess
import logging


mypath = os.path.dirname(os.path.realpath(__file__)) 

irma_brain = "172.16.1.30"
api = "http://"+irma_brain+"/api/v1.1/"

test_format_file = mypath+"/formats.txt"


listOfTest = list()
with open(test_format_file) as f:
    for l in f.readlines():
        tmp = l[:-1]
        listOfTest.append(tmp.lower())
        listOfTest.append(tmp.upper())
#logging.debug(listOfTest)

logging.basicConfig(filename='/var/log/usberry.log',level=logging.DEBUG)



class scanner:

    def __init__(self, rootPath):
        self.files          = list() # files : list( [path, result] )
        self.root           = rootPath
        self.api            = API(api)
        self.nFilesToScan   = 0


    def shouldBeScanned(self, file):


        filename    = file.rsplit('/')[-1]
        fileformat  = file.rsplit('.')[-1]

        logging.debug(filename+" ==> "+fileformat)


        logging.debug(listOfTest)
        
        #if no extension
        if(fileformat == filename):
            return True

        if(fileformat in listOfTest):
            return True

        return False


    def getFiles(self):
        files = [file for file in glob.glob(self.root + '/**/*', recursive=True)if not os.path.isdir(file)]
        logging.info(files)
        for f in files:
            if(self.shouldBeScanned(f)):
                self.nFilesToScan = self.nFilesToScan + 1
                self.files.append((f,None))


    def scanFiles(self):
        self.scan = self.api.createScan()
        for f in self.files:
            logging.debug("FILE : "+str(f[0]))
            self.api.uploadFiles(f[0],self.scan)

        self.api.startScan(self.scan)


    def getResult(self):
        pass



class API:
    
    def __init__(self, api):
        self.url = api

    def sendRequest(self, url, request, payload, files=None, json=None):
        logging.info("______________________")
        logging.info("Request : "+str(request)+"  "+str(url))
        logging.info("payload :"+str(payload))
        if(request == "GET"):
            r = requests.get(self.url+url, payload, files=files)
        else:
            r = requests.post(self.url+url, data=payload, files=files, json=json)
        logging.info("SendRequest : "+str(r.status_code))
        if(r.status_code != 200):
            logging.info("ERROR !")
            logging.info(r.status_code)
            logging.info(r.json())

        return (r.status_code, r.json(), r.headers)

    def createScan(self):
        r = self.sendRequest("scans", "POST", None)
        if(r[0] == 200):
            res = r[1]
            #logging.info(res['id'])
            return res['id']
        return r

    def uploadFiles(self, files, scan):
        r = self.sendRequest("scans/"+scan+"/files", "POST", {'scanId':scan}, files={'file':open(files, 'rb')})
        if(r[0] == 200):
            logging.info("file added : "+str(r[1]))

    def startScan(self, scan):
        payload = {'scanId':scan, 'options':{'force':True, 'mimetype_filtering':True,'resubmit_files':True}}
        #payload = {'force':True, 'mimetype_filtering':True,'resubmit_files':True}
        
        
        pay = json.dumps(payload)
        logging.info(pay)
        r = self.sendRequest("scans/"+scan+"/launch", "POST", {}, json=payload )
        if(r[0] == 200):
            logging.info("SCAN LAUNCHED")
            logging.debug(r)

            logging.info("GO TO : http://"+irma_brain+"/scan/"+r[1]["id"]+"/")



    def getAllProbes(self):
        return "all"
        r = self.sendRequest("probes", "GET", {})
        if(r[0] == 200):
            result = r[1]["data"]
            return result
        return "[]"



#
########################################################################################
#


def write(p):
    with open("/var/log/usberry.log","a+") as f:
        f.write(p)

def getDevName(kernelId):
    context = pyudev.Context()
    usb = None
    for device in context.list_devices(subsystem='block'):
        try:
            #logging.info(">"+str(device.device_node)+" <==> "+str(device.device_path))
            if(sys.argv[1] in device.device_path):
                logging.info(device)
                usb = device
                break
        except Exception as e:
            logging.info(e)

    path = usb.device_node
    return path

def mountFS(path):
    logging.info("Mounting file system")

    errors = False

    try:
        res_mkdir = subprocess.check_call(["mkdir","/mnt/usberry"])
    except Exception as e:
        logging.error(e)
        errors = True
    
    try:
        res_mount = subprocess.check_call(["mount", path, "/mnt/usberry"])
        if(res_mount != 0):
            logging.error("ERREUR mounting")
            sys.exit(1)
    except Exception as e:
        logging.error(e)
        errors = True


    if(not errors):
        logging.info("System mounted")
    else:
        logging.error("FAILED MOUNTING !")
    
    return errors


def startScan(path):
    logging.info("STARTING SCAAAAAAAAAN !!!")

    s = scanner(path)
    s.getFiles()
    if(s.nFilesToScan > 0):
        s.scanFiles()
    else:
        logging.info("NO FILES TO SCAN !")
    

if __name__ == '__main__':
    if(len(sys.argv) != 2):
        logging.info("NEED Mounted Kernel")
        sys.exit(0)
    
    time.sleep(5)
    logging.info("starting with kernel :"+sys.argv[1]+"\n") 
  
    path = getDevName(sys.argv[1])
    logging.info("path = "+path)
    res = False
    try:
        res = mountFS(path)
    except Exception as e:
        logging.error(e)
        res = True
    if(res):sys.exit(1)



    try:
        startScan("/mnt/usberry")
    except Exception as e:
        logging.error(e)