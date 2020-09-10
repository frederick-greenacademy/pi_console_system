import os
import sqlalchemy as db
from flask import Flask, request
import json
import sys
import decimal

UPLOAD_FOLDER = 'uploads'


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



@app.route("/")
def main():
    return "chào bạn đến với Hệ thống cơ sở dòng lệnh"


@app.route("/api/signin", methods=['POST'])
def check_sign_in():
    _user_name = request.form['user_name']
    _password = request.form['password']


    


if __name__ == "__main__":
    app.run(port=8000)
