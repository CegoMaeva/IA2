import cv2
import face_recognition
import numpy as np
from deepface import DeepFace
import pygame
import mysql.connector
from datetime import datetime
import os

pygame.init()
pygame.mixer.init()
alarm=pygame.mixer.Sound("images/alert.wav")

conn = mysql.connector.connect(
    host="localhost",         
    user="root", 
    password="", 
    database="detections_db",
    port=3309
)
c = conn.cursor()

face_dir = 'detected_faces'
os.makedirs(face_dir, exist_ok=True)

capture = cv2.VideoCapture(0)
signature_nom=np.load('SignaturesAll.npy')
signatures=signature_nom[:,:-1].astype('float')
noms=signature_nom[:,-1]

while True:
    reponse, image = capture.read()
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    face_location = face_recognition.face_locations(image_rgb)
    face_encoding = face_recognition.face_encodings(image_rgb, face_location)

    for encode,loc in zip(face_encoding, face_location):
            tab=face_recognition.compare_faces(signatures, encode)
            distance_face=face_recognition.face_distance(signatures, encode)
            minDist=np.argmin(distance_face)
            y1, x2, y2, x1 = loc

            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            face_img = image[y1:y2, x1:x2]
            img_path = None


            if tab[minDist]== True:
                cv2.rectangle(image, (x1, y1), (x2, y2), (255,0,0), 3)
                nom= str(noms[minDist])
                cv2.putText(image, nom, (x1 + 5, y1 + 25), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 3)
                c.execute("INSERT INTO detections (nom, date_heure) VALUES (%s, %s)", (nom, now))
                conn.commit()
            else:
                cv2.rectangle(image, (x1, y1), (x2, y2), (0,0,255), 3)
                nom= "Inconnu"
                cv2.putText(image, nom, (x1 + 5, y1 + 25), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 3)
                alarm.play()
                c.execute("INSERT INTO detections (nom, date_heure) VALUES (%s, %s)", (nom, now))
                conn.commit()

                try:
                    fac_image=image[y1:y2, x1:x2]
                    analyse=DeepFace.analyze(fac_image, actions=['emotion'], enforce_detection=False)

                    if isinstance(analyse, list):
                        analyse = analyse[0]

                    emotion = analyse.get('dominant_emotion', 'Nothing')
                    cv2.putText(image, emotion, (x1 + 5, y1 + 25), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 3)
                except:
                    print("Erreur lors de l'analyse des émotions.")

    cv2.imshow('Capture',image)
    if cv2.waitKey(1) == ord('q'):
        break

c.close()
conn.close()


