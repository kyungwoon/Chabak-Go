from flask import Flask, render_template, jsonify, request

import login_api

app = Flask(__name__)
app.register_blueprint(login_api.login_api)

from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbsparta

## HTML을 주는 부분
@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

i = 1