from model import db, StudentModel
import json


def SaveListJson():
    students = StudentModel.query.all()
    json_object = json.dumps(students, indent = 3)
    with open("sample.json", "w") as outfile:
        outfile.write(json_object)
