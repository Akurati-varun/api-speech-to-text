import time 
import sys 
import ibmiotf.application 
import ibmiotf.device 

def processTextCommand(textCommand):
    
    # Implement cloud command functionality here
    organization = "pn9oxd" 

    deviceType = "Varun" 

    deviceId = "24062810" 

    authMethod = "token" 

    authToken = "&PPfTQV!s8c)996eZ)" 
    deviceOptions = {"org": organization, "type": deviceType, "id": deviceId, "auth-method": authMethod, "auth-token": authToken,"clean-session":True} 
        
    deviceCli = ibmiotf.device.Client(deviceOptions)
    #connect to the cloud
    deviceCli.connect() 
        
    data1={"spoken":textcommand}
    #publish the event
    deviceCli.publishEvent(event="command",msgFormat="json",data=data1)
    time.sleep(0.5)
    #dissconect from cloud
    deviceCli.disconnect()   
    pass
    
