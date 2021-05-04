from PIL import Image, ImageOps
from keras import backend as K
import numpy as np 
from keras.models import load_model
import cv2 
def FacePrediction(file):
    #reading the file stream obj
    og_image=Image.open(file.stream)
    #converting it to grayscale
    gray_image = ImageOps.grayscale(og_image)
    #converting into array
    img_array = np.array(gray_image)
    #resizing 
    new_array=cv2.resize(img_array,(90,90))
    #reshaping the array
    new_array=np.array(new_array).reshape(-1,90,90,1)
    #normalizing the data
    new_array=new_array/255
    
    #Before prediction
    K.clear_session()
    #load model
    model =load_model('Gencproface.h5') 
    #model compiling
    model.compile(loss="categorical_crossentropy",optimizer="adam",metrics=["accuracy"])
    
    result=model.predict_classes(new_array)
    #After prediction
    K.clear_session()
    
    if(result[0]==0):
        return "Varun"
    elif(result[0]==1):
        return "Prajjwal"
    elif(result[0]==2):
        return "Akhil"
    
#    applying grayscale method
   
   
 
#     
#     
#     return result;