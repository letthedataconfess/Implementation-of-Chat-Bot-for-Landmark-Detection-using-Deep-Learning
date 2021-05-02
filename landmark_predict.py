import pandas as pd
import pickle
import numpy as np
#from keras.models import load_model
#from keras.preprocessing import image
import cv2
#from PIL import Image

filename = 'notebook/finalmodel.sav'

loaded_model = pickle.load(open(filename, 'rb'))
loaded_model._make_predict_function()


# You can also use pretrained model from Keras
# Check https://keras.io/applications/


def model_predict(img_path ):
    #img = image.load_path(img_path,target_size =(299,299))
    #img = Image.load_path(img_path,target_size =(299,299))
    img = cv2.resize(cv2.imread(img_path),(299,299))
     # Preprocessing the image
    img=img.reshape(1,299,299,3)
    imd=np.array(img) 
    # x = np.true_divide(x, 255)
    # x = np.expand_dims(x, axis=0)

    # Be careful how your trained model deals with the input
    # otherwise, it won't make correct prediction!
    #x = preprocess_input(x, mode='caffe')


    preds = loaded_model.predict(imd)
    
    print(np.argmax(preds))
    return np.argmax(preds)


#model_predict("C:/Users/training_b6b.01.07/Desktop/elephant.jpg")