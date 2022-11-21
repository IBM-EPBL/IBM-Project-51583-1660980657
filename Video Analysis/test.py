import cv2
import urllib.request
import dropbox
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import cv2
import os
from datetime import datetime
import tensorflow as tf
from time import sleep
from keras.models import load_model
model = tf.keras.models.load_model("CNN.model")
CATEGORIES=["Fire","Normal"]
font = cv2.FONT_HERSHEY_SIMPLEX
class TransferData:
    def __init__(self, access_token):
        self.access_token = access_token

    def upload_file(self, file_from, file_to):
        """upload a file to Dropbox using API v2
        """
        dbx = dropbox.Dropbox(self.access_token)

        with open(file_from, 'rb') as f:
            dbx.files_upload(f.read(), file_to)
def prepare(file):
    IMG_SIZE = 150
    img_array = cv2.imread(file, 1)

    #img_array = cv2.Canny(img_array, threshold1=3, threshold2=10)
    #img_array = cv2.medianBlur(img_array,1)
    new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
    new_array=np.expand_dims(new_array, axis=0)
    return new_array

def detect(filename):
    prediction = model.predict(prepare(filename))
    prediction = list(prediction[0])
    print(prediction)
    l=CATEGORIES[prediction.index(max(prediction))]
    return l
    
cap = cv2.VideoCapture(0)
if (cap.isOpened()== False):
    print("Error opening video stream or file")
while(cap.isOpened()):
    ret, frame = cap.read()
    if ret == True:
        cv2.imwrite("temp.jpg",frame)
        #sleep(0.05)
        try:
            x=detect("temp.jpg")
        except:
            print("Hello")
        cv2.putText(frame, x, (7, 70), font, 3, (100, 255, 0), 3, cv2.LINE_AA)
        cv2.imshow('Frame',frame)
        if x in "Fire" and y==0:
            y=1
            lines="Alert"
            import win32com.client
            speaker = win32com.client.Dispatch("SAPI.SpVoice")
            speaker.Speak(lines)
            urllib.request.urlopen("https://api.thingspeak.com/update?api_key=C6TYSSCZS42F7QCI&field3=COIMBATORE&field4=FIRE_OCCURED")
            access_token = 'OudsSqZa1PgAAAAAAAAAAdeCwBUvj2J4OCpi3j14MFveumcsJt-itIziqL4ztb6J'
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            transferData = TransferData(access_token)
            file_from = 'temp.jpg'
            file_to = '/Accident_dropbox/'+dt_string+'.png'  # The full path to upload the file to, including the file name
            transferData.upload_file(file_from, file_to)
        else:
            y=0
        
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
    else:
        break
cap.release()
cv2.destroyAllWindows()