from flask import render_template, request, Blueprint, jsonify

from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbsparta
login_api = Blueprint("login_api", __name__)

@login_api.route("/login")
def login_page():
    return render_template('login.html')

@login_api.route('/login', methods=['POST'])
def login():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']

    user = db.signup.find_one({'id': id_receive, 'pw': pw_receive})
    if user is None:
        return jsonify({'msg': '아이디나 비밀번호를 확인해주세요.'})
    else:
        return jsonify({'msg': '로그인되었습니다.'})
