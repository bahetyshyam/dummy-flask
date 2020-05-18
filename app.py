from flask import Flask, request, flash, redirect, jsonify
from dotenv import load_dotenv
import os
from flask_cors import CORS


# mongo db
import pymongo
from pymongo import MongoClient
from bson import ObjectId

#mongo db initialization
load_dotenv('.env')
client = MongoClient(os.getenv('MONGO_URI'))
db = client['automated-attendance']
students_collection = db.students
attendance_collection = db.attendance

app = Flask(__name__)
CORS(app)


@app.route('/')
def hello():
    return "Hello World!"

#GET request to get details of all the students
@app.route('/students', methods=['GET'])
def getAllStudents():
    students = []
    try:
        x = students_collection.find()
        for item in x:
            item['_id'] = str(item['_id'])
            students.append(item)
        return jsonify({
            "success" : True,
            "students" : students
        })
    except pymongo.errors.PyMongoError:
        return jsonify({
            "success" : False,
            "message" : "Internal Server Error"
        }), 500


#GET request to get the attendance of all instances of attendance
@app.route('/attendance', methods=['GET'])
def getAllAttendance():
    attendance = []
    try: 
        x = attendance_collection.find().sort("date",pymongo.DESCENDING)
        for item in x:
            item['_id'] = str(item['_id'])
            attendance.append(item)
        return jsonify({
            "success" : True,
            "attendance": attendance
        })
    except pymongo.errors.PyMongoError:
        return jsonify({
            "success" : False,
            "message" : "Internal Server Error"
        }), 500


if __name__ == '__main__':
    app.run()