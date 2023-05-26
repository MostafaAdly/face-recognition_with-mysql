import face_recognition
import json
import cv2
import numpy as np
import math
import pathlib
import urllib
from gtts import gTTS
import os
from urllib.request import urlopen
import mysql.connector
from datetime import datetime


with open(f'{pathlib.Path(__file__).parent.resolve()}/mysql.json') as f:
    mysqldb = json.load(f)


def connectMySQL():
    return mysql.connector.connect(
        host=mysqldb["host"],
        user=mysqldb["user"],
        password=mysqldb["pass"],
        database=mysqldb["database"]
    )


def talk(msg):
    file = gTTS(text=msg, lang="en", tld="co.in")
    file.save("last-bot-message.mp3")
    os.system("start last-bot-message.mp3")
    return msg


def getCurrentDate():
    return datetime.today().strftime('%Y-%m-%d')


class MySQLInsert:
    def __init__(self):
        self.mysql = connectMySQL()
        pass

    def hasAttendedToday(self, name, cr):
        cur = self.mysql.cursor()
        cur.execute(
            f"select * from attendance where name='{name}' AND class='{cr}' AND time_attended='{getCurrentDate()}'")
        for x in cur:
            return True
        return False

    def insert(self, name, cr):
        cur = self.mysql.cursor()
        cur.execute(
            f"insert into attendance (`name`, `class`, `time_attended`) values('{name}', '{cr}', '{getCurrentDate()}')")
        self.mysql.commit()


class ClassAttendance:
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    def __init__(self, classroom, students, min_conf):
        self.classroom = classroom
        self.students = students
        self.min_conf = min_conf
        self.mysqlInsert = MySQLInsert()
        self.def_name = "Not found"

    def getImageFromURL(self, url):
        req = urllib.request.urlopen(url)
        arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
        print(arr)
        return cv2.imdecode(arr, -1)

    def getEncodedImages(self):
        imgs = []
        for x in self.students:
            print(x)
            imgs.append(face_recognition.face_encodings(
                cv2.cvtColor(self.getImageFromURL(x.img_url), cv2.COLOR_BGR2RGB))[0])
        return imgs

    def getConfidence(self, face_distance, face_match_threshold=0.6):
        range = (1.0 - face_match_threshold)
        linear_val = (1.0 - face_distance) / (range * 2.0)

        if face_distance > face_match_threshold:
            return str(round(linear_val * 100, 2)) + '%'
        else:
            value = (linear_val + ((1.0 - linear_val) *
                                   math.pow((linear_val - 0.5) * 2, 0.2))) * 100
            return (round(value, 2))

    def getStudentByIndex(self, index):
        i = 0
        for x in self.students:
            if i == index:
                return x.name
            i += 1
        return self.def_name

    def start(self):
        encodedStudentImages = self.getEncodedImages()
        print(encodedStudentImages)
        video_capture = cv2.VideoCapture(0)
        while True:
            ignored, img = video_capture.read()

            # print("checking video capture")
            faceCurentFrame = face_recognition.face_locations(img)
            encodeCurentFrame = face_recognition.face_encodings(
                img, faceCurentFrame)
            for encodeface, faceLoc in zip(encodeCurentFrame, faceCurentFrame):
                faceDis = face_recognition.face_distance(
                    encodedStudentImages, encodeface)
                matchIndex = np.argmin(faceDis)
                confidence = self.getConfidence(faceDis[matchIndex])
                detectedstudent = self.getStudentByIndex(matchIndex) if face_recognition.compare_faces(
                    encodedStudentImages, encodeface)[matchIndex] and confidence >= self.min_conf else self.def_name

                if detectedstudent != self.def_name:
                    if self.mysqlInsert.hasAttendedToday(detectedstudent, self.classroom) == True:
                        continue
                    self.mysqlInsert.insert(detectedstudent, self.classroom)

                # Draw rectangle around student face
                y1, x2, y2, x1 = faceLoc
                cv2.rectangle(img, (x1, y1), (x2, y2), (102, 0, 255), 2)
                if detectedstudent != self.def_name:
                    talk(detectedstudent)
                cv2.putText(img, f"{detectedstudent} {confidence}%" if detectedstudent != self.def_name else detectedstudent, (x1+6, y1-6),
                            cv2.FONT_HERSHEY_COMPLEX, 0.6, (102, 0, 255), 2)

            cv2.imshow(f'Attendance - Class [{self.classroom}]', img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        video_capture.release()
        cv2.destroyAllWindows()

