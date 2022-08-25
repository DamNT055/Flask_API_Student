from flask_sqlalchemy import SQLAlchemy
from flask import jsonify

db = SQLAlchemy()

class StudentModel(db.Model):
    __tablename__ = "table"
    
    id = db.Column(db.Integer(), primary_key=True)
    student_id = db.Column(db.Integer(),unique = True)
    name = db.Column(db.String())
    birth_date = db.Column(db.DateTime())
    birth_place = db.Column(db.String())
    grade = db.Column(db.Integer())
    exam_score = db.Column(db.Float()) 

    def __init__(self, student_id, name, birth_date, birth_place, grade, exam_score):
        self.student_id = student_id
        self.name = name
        self.birth_date = birth_date
        self.birth_place = birth_place
        self.grade = grade
        self.exam_score = exam_score
        
    
    def __repr__(self):
        return  f"student: {self.student_id}\n name: {self.name}\n Date of Birth: {self.birth_date}\n Place of Birth: {self.birth_place}\n Grade: {self.grade}\n Overall exam score: {self.exam_score}"
    
    
    @property
    def serialize(self):
       """Return object data in easily serializable format"""
       return {
           'student_id' : self.student_id,
           'name' : self.name,
           'birth_date' : self.birth_date,
           'birth_place' : self.birth_place,
           'grade' : self.grade,
           'exam_score' : self.exam_score
       } 