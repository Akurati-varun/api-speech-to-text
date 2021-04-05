from os import getenv
from dotenv import load_dotenv

load_dotenv()

class IBMCloudCred:
    organization = getenv("organization") 
    deviceType = getenv("deviceType") 
    deviceId = getenv("deviceId") 
    authMethod = getenv("authMethod") 
    authToken = getenv("authToken") 
    
    deviceOptions = {
        "org": organization, 
        "type": deviceType, 
        "id": deviceId, 
        "auth-method": authMethod, 
        "auth-token": authToken,
        "clean-session":True
    }