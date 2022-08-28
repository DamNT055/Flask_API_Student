# Flask_API_Student

GET /students
This API will return a JSON string having all the student information

POST /students -d ‘{“name”: “Nguyen Xuan Quyet”}’
This API would create a student and save student to the student list saved in our storage

PUT /students -d ‘{“name”: “Nguyen Nam”}’
This API allow update a student

DELETE/students -d {"name": "Nguyen Thanh Tien"}
This API ability delete a student
