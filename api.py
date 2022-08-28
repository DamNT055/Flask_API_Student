import sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS
import json

def connect_to_db():
    conn = sqlite3.connect('databasestudent.db')
    return conn


def create_db_table():
    try:
        conn = connect_to_db()
        conn.execute('''DROP TABLE IF EXISTS students''')
        conn.execute('''
            CREATE TABLE "students" (
                "student_id"	INTEGER NOT NULL,
                "name"	TEXT NOT NULL,
                "birth_date"	TEXT NOT NULL,
                "birth_place"	TEXT NOT NULL,
                "grade"	INTEGER NOT NULL CHECK(grade > 0 AND grade <=12),
                "exam_score"	REAL NOT NULL CHECK(exam_score > 0 AND exam_score <=10),
                PRIMARY KEY("student_id")
            );
        ''')

        conn.commit()
        print("User table created successfully")
    except:
        print("User table creation failed - Maybe table")
    finally:
        conn.close()


def insert_student(student):
    inserted_student = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO students (student_id, name, birth_date, birth_place, grade, exam_score) VALUES (?, ?, ?, ?, ?, ?)", (student['student_id'], student['name'], student['birth_date'], student['birth_place'], student['grade'], student['exam_score']) )
        conn.commit()
        inserted_student = get_student_by_id(cur.lastrowid)
    except:
        conn.rollback()
    finally:
        conn.close()
    return inserted_student    


def get_students():
    students = []
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM students")
        rows = cur.fetchall()

        # convert row objects to dictionary
        for i in rows:
            student = {}
            student["student_id"] = i["student_id"]
            student["name"] = i["name"]
            student["birth_date"] = i["birth_date"]
            student["birth_place"] = i["birth_place"]
            student["grade"] = i["grade"]
            student["exam_score"] = i["exam_score"]
            students.append(student)

    except:
        students = []

    return students


def get_student_by_id(student_id):
    student = {}
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM students WHERE student_id = ?", (student_id,))
        row = cur.fetchone()
        # convert row object to dictionary
        student["student_id"] = row["student_id"]
        student["name"] = row["name"]
        student["birth_date"] = row["birth_date"]
        student["birth_place"] = row["birth_place"]
        student["grade"] = row["grade"]
        student["exam_score"] = row["exam_score"]
    except:
        student = {}

    return student


def update_student(student):
    updated_student = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("UPDATE students SET name = ?, birth_date = ?, birth_place = ?, grade = ?, exam_score = ? WHERE student_id =?", (student["name"], student["birth_date"], student["birth_place"], student["grade"], student["exam_score"], student["student_id"],))
        conn.commit()
        #return the user
        updated_student = get_student_by_id(student["student_id"])

    except:
        conn.rollback()
        updated_student = {}
    finally:
        conn.close()

    return updated_student


def delete_student(student_id):
    message = {}
    try:
        conn = connect_to_db()
        conn.execute("DELETE from students WHERE student_id = ?", (student_id,))
        conn.commit()
        message["status"] = "Student deleted successfully"
    except:
        conn.rollback()
        message["status"] = "Cannot delete student"
    finally:
        conn.close()

    return message

def SaveListJson():
    students = get_students()
    json_object = json.dumps([student for student in students], indent=4, default=str)
    with open("student.json", "w") as outfile:
        outfile.write(json_object)
    with open('student.json', 'r') as openfile:
        json_open = json.load(openfile) 
    print(json_open)
    print("Save list json successfull")
    return json_open

def load_json():
    loaded_student = []
    with open('student.json', 'r') as openfile:
        json_object = json.load(openfile)
        for json_ob in json_object:
            loaded_student.append(insert_student(json_ob))
        print("Load list json successfull")
        return loaded_student



students = []
student0 = {
        "student_id": 123,
        "name": "Nguyen Thanh Dam",
        "birth_date": "2001-12-05",
        "birth_place": "Binh Dinh",
        "grade": 5,
        "exam_score": 6.5
    }

student1 = {
        "student_id": 126,
        "name": "Nguyen Thanh Huy",
        "birth_date": "2001-12-08",
        "birth_place": "Nha Trang",
        "grade": 12,
        "exam_score": 5.0
    }

student2 = {
        "student_id": 115,
        "name": "Nguyen Xuan Thang",
        "birth_date": "2001-06-05",
        "birth_place": "Ha Noi",
        "grade": 12,
        "exam_score": 5.0
    }

student3 = {
        "student_id": 152,
        "name": "Nguyen Manh Hung",
        "birth_date": "2001-06-05",
        "birth_place": "Ha Noi",
        "grade": 12,
        "exam_score": 5.0
    }

students.append(student0)
students.append(student1)
students.append(student2)
students.append(student3)

create_db_table()

for i in students:
    print(insert_student(i))




app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.before_first_request
def api_load_json():
    return load_json()

@app.route('/<json_file>', methods=['GET'])
def api_load_any_json(json_file):
    with open(json_file, 'r') as openfile:
        json_object = json.load(openfile)
    return json_object

@app.route('/api/students', methods=['GET'])
def api_get_students():
    return jsonify(get_students())

@app.route('/api/students/<student_id>', methods=['GET'])
def api_get_student(student_id):
    return jsonify(get_student_by_id(student_id))

@app.route('/api/students/add',  methods = ['POST'])
def api_add_student():
    student = request.get_json()
    return jsonify(insert_student(student))

@app.route('/api/students/update',  methods = ['PUT'])
def api_update_user():
    student = request.get_json()
    return jsonify(update_student(student))

@app.route('/api/students/delete/<student_id>',  methods = ['DELETE'])
def api_delete_user(student_id):
    return jsonify(delete_student(student_id))

@app.route('/api/students/savejson', methods = ['GET'])
def api_save_json():
    return jsonify(SaveListJson())



if __name__ == "__main__":
    #app.debug = True
    #app.run(debug=True)
    app.run(host='localhost', port=9000)