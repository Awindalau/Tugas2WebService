# 6C/19090023/Muchammad Nachirul Ichsan
# 6C/19090063/Arwinda Laurisma

#username/pass
#19090023/123
#19090063/123

import os, random, string

from flask import Flask
from flask import jsonify, request
from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "user.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app)

class User(db.Model):
  username = db.Column(db.String(80), unique=True, nullable=False)
  password = db.Column(db.String(80), unique=False, nullable=False)
  token = db.Column(db.String(225), unique=True, nullable=True)
  db.create_all()
  
#curl -i -X POST http://127.0.0.1:7005/api/v1/login/api/v1/login -H 'Content-Type: application/json' -d '{"username":19090023, "password": 123}'
@app.route("/api/v1/login", methods=["POST"])
def login():
  username = request.form['username']
  password = request.form['password']

  user = User.query.filter_by(username=username, password=password).first()

  if user:
    token = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    
    User.query.filter_by(username=username, password=password).update({'token': token})
    db.session.commit()

    return jsonify({
      'msg': 'Login Sukses',
      'username': username,
      'token': token,
      'status': 200 
      })

  else:
    return jsonify({
      'msg': 'Login Failed',
      'status': 401,
      })

@app.route("/api/v2/users/info", methods=["POST"])
def info():
  token = request.values.get('token')
  user = User.query.filter_by(token=token).first()
  if user:
      return jsonify({
        'msg': 'Get User Berhasil',
        'username': user.username,
        'status': 200
        })
  else:
      return jsonify({
        'msg': 'token error'
        })

if __name__ == '__main__':
   app.run(debug = True, port=7005)