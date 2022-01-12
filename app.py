import datetime
import hashlib

from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbsparta

#이 문자열은 서버만 알고있기 때문에, 내 서버에서만 토큰을 인코딩(=만들기)/디코딩(=풀기) 할 수 있습니다.
SECRET_KEY = 'SPARTA'

#JWT 패키지를 사용합니다.(설치해야할 패키지 이름 : pyJWT)
import jwt

@app.route("/")
def login_page():
    return render_template('login.html')

## HTML을 주는 부분
@app.route('/signup')
def home():
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']

    # 회원가입 때와 같은 방법으로 pw를 암호화합니다.
    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    # id, 암호화 된 pw을 가지고 해당 유정를 찾습니다.
    # 시크릿키가 있어야 토큰을 디코딩(=풀기) 해서 payload 값을 볼 수 있습니다.
    # 아래에선 id와 exp를 담았습니다. 즉,JWT 토큰을 풀면 유저ID 값을 알 수 있습니다.
    # exp에는 만료시간을 넣어줍니다. 만료시간이 지나면, 시크릿키로 토큰을 풀 때 만료되었다고 에러가 납니다.

    user = db.signup.find_one({'id': id_receive, 'pw': pw_receive})
    if user is None:
        payload ={
            'id':id_receive,
            'exp':datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256').decode('utf-8')

        return jsonify({'msg': '아이디나 비밀번호를 확인해주세요.', 'token':token})
    else:
        return jsonify({'msg': '로그인되었습니다.'})

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


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)