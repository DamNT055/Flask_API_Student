from flask import Flask, render_template, request, redirect, abort, jsonify
from model import db, StudentModel
from datetime import datetime
import templates
import json


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///studentdb.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

@app.before_first_request
def create_table():
    db.create_all()
    print("table successfull")

@app.before_first_request
def load_json():
    with open('sample.json', 'r') as openfile:
        json_object = json.load(openfile)
        for json_ob in json_object:
            student_id = json_ob['student_id']
            student_check = StudentModel.query.filter_by(student_id=student_id).first()
            if student_check is not None:
                continue
            name = json_ob['name']
            birth_date = datetime.strptime(json_ob['birth_date'].split()[0], '%Y-%m-%d')
            birth_place = json_ob['birth_place']
            grade = json_ob['grade']
            exam_score = json_ob['exam_score']
            student = StudentModel(student_id=student_id, name=name, birth_date=birth_date, 
                              birth_place = birth_place, grade=grade, exam_score = exam_score )
            db.session.add(student)
            db.session.commit()
        return redirect('/data')        

@app.route('/data/create' , methods = ['GET','POST'])
def create():
    if request.method == 'GET':
        return render_template('createpage.html')
     
    if request.method == 'POST':
        student_id = request.form['student_id']
        student_check = StudentModel.query.filter_by(student_id=student_id).first()
        if student_check is None:
            name = request.form['name']
            birth_date = datetime.strptime(request.form['birth_date'], '%Y-%m-%d')
            birth_place = request.form['birth_place']
            grade = request.form['grade']
            exam_score = request.form['exam_score']
        
            student = StudentModel(student_id=student_id, name=name, birth_date=birth_date, 
                                birth_place = birth_place, grade=grade, exam_score = exam_score )
            db.session.add(student)
            db.session.commit()
        return redirect('/data')

@app.route('/data')
def RetrieveList():
    students = StudentModel.query.all()
    return render_template('datalist.html', students = students)

@app.route('/data/<int:id>')
def RetrieveStudent(id):
    student = StudentModel.query.filter_by(student_id=id).first()
    print(type(student))
    if student:
        return render_template('data.html', student = student)
    return f"Student with ID ={id} Doenst exist"

@app.route('/data/<int:id>/update',methods = ['GET','POST'])
def update(id):
    student = StudentModel.query.filter_by(student_id=id).first()
    if request.method == 'POST':
        if student:
            name = request.form['name']
            birth_date = datetime.strptime(request.form['birth_date'], '%Y-%m-%d')            
            birth_place = request.form['birth_place']
            grade = request.form['grade']
            exam_score = request.form['exam_score']
            student2 = StudentModel(student_id=id, name=name, birth_date=birth_date, 
                              birth_place = birth_place, grade=grade, exam_score = exam_score )            
            
            db.session.delete(student)
            db.session.commit()

            db.session.add(student2)
            db.session.commit()
            return redirect(f'/data/{id}')
        return f"Employee with id = {id} Does nit exist"
 
    return render_template('update.html', student = student)


@app.route('/data/<int:id>/delete', methods=['GET','POST'])
def delete(id):
    student = StudentModel.query.filter_by(student_id=id).first()
    if request.method == 'POST':
        if student:
            db.session.delete(student)
            db.session.commit()
            return redirect('/data')
        else: abort(404)
 
    return render_template('delete.html', student = student)
 

@app.route('/data/savejson')
def SaveListJson():
    students = StudentModel.query.all()    
    json_object = json.dumps([dict(student.serialize) for student in students], indent=4, default=str)
    with open("sample.json", "w") as outfile:
        outfile.write(json_object)
    with open('sample.json', 'r') as openfile:
        json_open = json.load(openfile) 
    print(json_open)
    return jsonify(json_open)
    
if __name__ == '__main__':
    db.init_app(app)
    app.run(host='localhost', port=8000)
    app.debug = True
    