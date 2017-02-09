#!/usr/bin/python

import requests
import json
import os
import glob

irma_brain = "172.16.1.30"
api = "http://"+irma_brain+"/api/v1.1/"

class scanner:

    def __init__(self, rootPath):
        self.files = list()
        # files : list( [path, result] )
        self.root = rootPath
        self.api = API(api)


    def getFiles(self):
        files = [file for file in glob.glob(self.root + '/**/*', recursive=True)if not os.path.isdir(file)]
        print(files)
        for f in files:
            self.files.append((f,None))


    def scanFiles(self):
        self.scan = self.api.createScan()
        for f in self.files:
            self.api.uploadFiles(f[0],self.scan)

        self.api.startScan(self.scan)


    def getResult(self):
        pass



class API:
    
    def __init__(self, api):
        self.url = api

    def sendRequest(self, url, request, payload, files=None, json=None):
        print("______________________")
        print("Request : "+str(request)+"  "+str(url))
        print("payload :"+str(payload))
        if(request == "GET"):
            r = requests.get(self.url+url, payload, files=files)
        else:
            r = requests.post(self.url+url, data=payload, files=files, json=json)
        print("SendRequest : "+str(r.status_code))
        if(r.status_code != 200):
            print("ERROR !")
            print(r.status_code)
            print(r.json())

        return (r.status_code, r.json(), r.headers)

    def createScan(self):
        r = self.sendRequest("scans", "POST", None)
        if(r[0] == 200):
            res = r[1]
            #print(res['id'])
            return res['id']
        return r

    def uploadFiles(self, files, scan):
        r = self.sendRequest("scans/"+scan+"/files", "POST", {'scanId':scan}, files={'file':open(files, 'rb')})
        if(r[0] == 200):
            print("file added : "+str(r[1]))

    def startScan(self, scan):
        payload = {'scanId':scan, 'options':{'force':True, 'mimetype_filtering':True,'resubmit_files':True}}
        #payload = {'force':True, 'mimetype_filtering':True,'resubmit_files':True}
        
        
        pay = json.dumps(payload)
        print(pay)
        r = self.sendRequest("scans/"+scan+"/launch", "POST", {}, json=payload )
        if(r[0] == 200):
            print("SCAN LAUNCHED")


    def getAllProbes(self):
        return "all"
        r = self.sendRequest("probes", "GET", {})
        if(r[0] == 200):
            result = r[1]["data"]
            return result
        return "[]"


s = scanner("/home/olbaid/Documents/tests/")
s.getFiles()
s.scanFiles()
