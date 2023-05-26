import mysql.connector
from FaceRecogClassConstructor import ClassAttendance
import pathlib
import json
from datetime import datetime

# Students list which contain all students from all classes [all data about them{name, img_url, classes}]
students = []


class Student:
    def __init__(self, name, img_url, classes):
        self.name = name
        self.img_url = img_url
        self.classes = classes


def path():
    return pathlib.Path(__file__).parent.resolve()


with open(f'{path()}/classes.json') as f:
    classes = json.load(f)

print("________________________________________")
print(f"Loaded {len(classes['classes'])} classes from local json file.")
active_class = input("Input current active class: ")

with open(f'{path()}/mysql.json') as f:
    mysqldb = json.load(f)


def connectMySQL():
    return mysql.connector.connect(
        host=mysqldb["host"],
        user=mysqldb["user"],
        password=mysqldb["pass"],
        database=mysqldb["database"]
    )

print("Connecting to MySQL...")
mysqlQuery = connectMySQL()


def LoadStudents():
    cur = mysqlQuery.cursor()
    cur.execute(
        f"select * from students")
    for x in cur:
        if x[2].find(active_class) >= 0:
            students.append(Student(x[0], x[1], x[2].split(";")))


LoadStudents()
print(f"Starting system in class: {active_class}")
print(f"Loaded {len(students)} students from MySQL.")
print("________________________________________")
if len(students) == 0:
    print(
        f'Stopping because of class [{active_class}] is not having any students.')
else:  # STARTING MAIN CONSTRUCTOR
    clas = ClassAttendance(active_class, students, 92)
    clas.start()
print("Shutting down...")
