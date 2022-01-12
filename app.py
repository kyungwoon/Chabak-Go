<<<<<<< HEAD
import hashlib

from flask import Flask, render_template, jsonify, request
=======
from flask import Flask, render_template, jsonify, request, session, redirect, url_for
>>>>>>> c17ec80954279b4add68f57dd8d862108b390fbd

app = Flask(__name__)

from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbsparta

<<<<<<< HEAD
#JWT 패키지를 사용합니다.(설치해야할 패키지 이름 : pyJWT)
import jwt

@app.route("/")
def login_page():
    return render_template('login.html')
=======
#JWT 토큰 비밀문자열
SECRET_KEY = 'CHABAK'

import jwt

#토큰만료시간
import datetime

#비밀번호 암호화
import hashlib
>>>>>>> c17ec80954279b4add68f57dd8d862108b390fbd

## HTML을 주는 부분
@app.route('/signup')
def home():
<<<<<<< HEAD
    return render_template('index.html')

=======
    return render_template('login.html')
>>>>>>> c17ec80954279b4add68f57dd8d862108b390fbd

@app.route("/signup")
def login_page():
    return render_template('index.html')

###API###

@app.route('/api/login', methods=['POST'])
def login():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']

    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    user = db.signup.find_one({'id': id_receive, 'pw': pw_hash})
    if user is None:
        return jsonify({'msg': '아이디나 비밀번호를 확인해주세요.'})
    else:
        payload = {
            'id': id_receive,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256').decode('utf-8')

        return jsonify({'result': 'success', 'token': token, 'msg' : '로그인되었습니다.'})



@app.route('/api/signup', methods=['POST'])
def sign_up():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']
    name_receive = request.form['name_give']

    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    doc = {
        'id': id_receive,
        'pw': pw_hash,
        'name': name_receive
    }
    db.signup.insert_one(doc)
    return jsonify({'msg': '회원가입되었습니다.'})


@app.route('/sign_up/check_dup', methods=['POST'])
def check_dup():
    username_receive = request.form['username_give']
    exists = bool(db.signup.find_one({"id": username_receive}))
    return jsonify({'result': 'success', 'exists': exists})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)