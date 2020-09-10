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

def is_user_exits_with(user, passwrd, car_id):

    try:
        conn = mariadb.connect(**config_pi_db.config)
    except mariadb.Error as e:
        print(f"Loi ket noi den MariaDB: {e}")
        return json.dumps({"result": "false", "error": "không thể kết nối đến db"})

    cur = conn.cursor()

    try:
        cur.execute(
            "SELECT account_id, password FROM Account WHERE user_name=?", (user,))
        ttt = cur.fetchall()
        if len(ttt) <= 0:
            conn.close()
            return json.dumps({"result": "false", "error": "Không tìm thấy tên tài khoản này: " + user})

        account_id_value = None
        for x in ttt:
            print(f"U: {x[0]}, P: {x[1]}")
            if x[1] == passwrd:
                account_id_value = x[0]
                break

        if account_id_value != None:

            cur.execute(
                "SELECT vehicle_id, status FROM Rent WHERE account_id=? and vehicle_id=? and status=?",
                (account_id_value, car_id, 'thuê'))

            vehicle_id_value = cur.fetchall()
            conn.close()

            if len(vehicle_id_value) > 0:
                return json.dumps({"result": "true", "message": "Tìm thấy mã xe của tk: " + user})
            else:
                return json.dumps({"result": "false", "error": "Không tìm thấy ma xe: " + car_id})

        else:
            conn.close()
            return json.dumps({"result": "false", "error": "Mật khẩu của tài khoản này không đúng"})

    except mariadb.Error as e:
        print(f"Error SQL: {e}")
        return json.dumps({"result": "false", "error": e})


@app.route("/")
def main():
    return "chào bạn đến với Hệ thống cơ sở dòng lệnh"


@app.route("/api/signin", methods=['POST'])
def check_sign_in():
    _user_name = request.form['user_name']
    _password = request.form['password']





if __name__ == "__main__":
    app.run(port=8000)
