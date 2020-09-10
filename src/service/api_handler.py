import os
import sqlalchemy as db
from flask import Flask, request
import json
import sys
import decimal
import config_pi_db

UPLOAD_FOLDER = 'uploads'



app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)

def is_user_exits_with(user, passwrd):

    try:
        conn = mariadb.connect(**config_pi_db.config)
    except mariadb.Error as e:
        print(f"Loi ket noi den MariaDB: {e}")
        return json.dumps({"result": "false", "error": "không thể kết nối đến db"})

    cur = conn.cursor()

    try:
        cur.execute(
            "SELECT account_id FROM Account WHERE user_name=? AND password=?", (user, passwrd))

        ttt = cur.fetchall()
        if len(ttt) <= 0:
            conn.close()
            return json.dumps({"result": "false", "error": "Không tìm thấy tên tài khoản và mật khẩu này!"})


        conn.close()
        return json.dumps({"result": "true", "message": "Mật khẩu của tài khoản này không đúng"})

    except mariadb.Error as e:
        print(f"Error SQL: {e}")
        return json.dumps({"result": "false", "error": e})

# Flask API
@app.route("/")
def main():
    return "chào bạn đến với Hệ thống cơ sở dòng lệnh"


@app.route("/api/signin", methods=['POST'])
def check_sign_in():
    _user_name = request.form['user_name']
    _password = request.form['password']
    # check user_name and password
    is_user_exits_with(_user_name, _password)



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
