import cv2
import numpy as np
import os

class Trainer():
    def __init__(self, path='face', recognizer=cv2.face.LBPHFaceRecognizer_create(), detector=cv2.CascadeClassifier("haarcascade_frontalface_default.xml")):
        self.path = path
        self.recognizer = recognizer
        self.detector = detector

    def getImagesAndLabels(self, path, detector):

        imagePaths = [os.path.join(path,f) for f in os.listdir(path)]
        faceSamples=[]
        ids = []

        for imagePath in imagePaths:
            img = cv2.imread(imagePath)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            img_numpy = np.array(img,'uint8')

            id = int(os.path.split(imagePath)[-1].split(".")[1])
            faces = detector.detectMultiScale(img_numpy)

            for (x,y,w,h) in faces:
                faceSamples.append(img_numpy[y:y+h,x:x+w])
                ids.append(id)

        return faceSamples,ids

    def Train(self):
        faces,ids = self.getImagesAndLabels(self.path, self.detector)
        self.recognizer.train(faces, np.array(ids))
        self.recognizer.write('trainer/trainer.yml')

