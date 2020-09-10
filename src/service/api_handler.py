import os
import mariadb
from flask import Flask, request
import json
import sys
import decimal

UPLOAD_FOLDER = 'uploads'
db_config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'pi',
    'password': 'password',
    'database': 'pi_iot'
}


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)

def is_user_exits_with(user, password):

    # check user_name and password
    try:
        conn = mariadb.connect(**db_config)
    except mariadb.Error as e:
        print(f"\n\nLoi ket noi den MariaDB: {e}\n\n")
        return json.dumps({"result": "false", "error": "không thể kết nối đến db"})

    cur = conn.cursor()

    try:
        cur.execute(
            "SELECT account_id, last_name, first_name, user_name FROM Account WHERE user_name=? AND password=?", (user, password))

        result_set = cur.fetchall()
        if len(result_set) <= 0:
            conn.close()
            return json.dumps({"result": "false", "error": "Không tìm thấy tên tài khoản và mật khẩu này!"})


        conn.close()
        
        user = {
            "last_name": result_set[0][1],
            "first_name": result_set[0][2],
            "user_name": result_set[0][3],
            "account_id": result_set[0][0]
        }
        return json.dumps({"result": "true", "data": user})

    except mariadb.Error as e:
        print(f"Error SQL: {e}")
        return json.dumps({"result": "false", "error": e})

# Flask API
@app.route("/")
def main():
    return "chào bạn đến với Hệ thống cơ sở dòng lệnh"


@app.route("/api/signin", methods=['POST'])
def check_sign_in():
    user = request.form['user_name']
    password = request.form['password']
    return is_user_exits_with(user, password)
    



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
