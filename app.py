from flask import Flask, render_template, jsonify, request, session, redirect, url_for

app = Flask(__name__)

from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbsparta

# JWT 토큰 비밀문자열
SECRET_KEY = 'CHABAK'

import jwt

# 토큰만료시간
import datetime

# 비밀번호 암호화
import hashlib

@app.route("/")
def login_page():
    return render_template('login.html')

###API###

@app.route('/', methods=['POST'])
def login():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']

    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    user = db.signup.find_one({'id': id_receive, 'pw': pw_hash})

    if user is None:
        payload ={
            'id':id_receive,
            'exp':datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256').decode('utf-8')

        return jsonify({'msg': '아이디나 비밀번호를 확인해주세요.', 'token':token})
    else:
        payload = {
            'id': id_receive,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }
        token = list(jwt.encode(payload, SECRET_KEY, algorithm='HS256', ))

        return jsonify({'result': 'success', 'token': token, 'msg': '로그인되었습니다.'})

@app.route('/name', methods=['GET'])
def api_valid():
    token_receive = request.cookies.get('mytoken')

    # try / catch 문?
    # try 아래를 실행했다가, 에러가 있으면 except 구분으로 가란 얘기입니다.

    try:
        # token을 시크릿키로 디코딩합니다.
        # 보실 수 있도록 payload를 print 해두었습니다. 우리가 로그인 시 넣은 그 payload와 같은 것이 나옵니다.
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        # print(payload)

        # payload 안에 id가 들어있습니다. 이 id로 유저정보를 찾습니다.
        # 여기에선 그 예로 닉네임을 보내주겠습니다.
        userinfo = db.signup.find_one({'id': payload['id']}, {'_id': 0})
        return jsonify({'result': 'success', 'name': userinfo['name']})
    except jwt.ExpiredSignatureError:
        # 위를 실행했는데 만료시간이 지났으면 에러가 납니다.
        return jsonify({'result': 'fail', 'msg': '로그인 시간이 만료되었습니다.'})
    except jwt.exceptions.DecodeError:
        return jsonify({'result': 'fail', 'msg': '로그인 정보가 존재하지 않습니다.'})


# 회원가입
@app.route('/signup')
def sing_up_page():
    return render_template('registe.html')


@app.route('/signup', methods=['POST'])
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


# 메인페이지
@app.route('/main')
def main_page():
    return render_template('index.html')


@app.route('/main_page', methods=['GET'])
def show_card():
    category_card = list(db.prac.find({}, {'_id': False}))
    return jsonify({'all_card': category_card})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)