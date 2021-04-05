import time 
import sys 
import ibmiotf.application 
import ibmiotf.device 
from config import IBMCloudCred


def processTextCommand(textCommand):
    
    deviceOptions = IBMCloudCred.deviceOptions
    
    deviceCli = ibmiotf.device.Client(deviceOptions)
    
    #connect to the cloud
    deviceCli.connect() 
        
    data1={"spoken":textCommand}
    #publish the event
    deviceCli.publishEvent(event="command",msgFormat="json",data=data1)
    time.sleep(0.5)
    #dissconect from cloud
    deviceCli.disconnect()   
    
