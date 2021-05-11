from keras import backend as K 
from keras.models import load_model
from keras_preprocessing import image
import numpy as np 


def FacePrediction(file):
    
    #reading the file stream and converting to greyscale
    image_data=file.resize((90,90))

    #converting into array
    image_array=image.img_to_array(image_data)
    #reshaping the array
    new_array=np.array(image_array).reshape(-1,90,90,1)
    #normalizing the data
    new_array=new_array/255;
    
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
