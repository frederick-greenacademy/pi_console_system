import os
import json
import sys
import mariadb
import decimal
from flask_cors import CORS
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

path = os.getcwd()
# file Upload
UPLOAD_FOLDER = os.path.join(path, 'static/uploads')
# Make directory if "uploads" folder not exists
print(UPLOAD_FOLDER)
if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


db_config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'pi',
    'password': 'password',
    'database': 'pi_iot'
}


app = Flask(__name__)


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# It will allow below 16MB contents only, you can change it
# app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
CORS(app)


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
        return json.dumps({"result": False, "error": "không thể kết nối đến db"})

    cur = conn.cursor()

    try:
        cur.execute(
            "SELECT account_id, last_name, first_name, user_name FROM Account WHERE user_name=? AND password=?", (user, password))

        result_set = cur.fetchall()
        if len(result_set) <= 0:
            conn.close()
            return json.dumps({"result": False, "error": "Không tìm thấy tên tài khoản và mật khẩu này!"})

        conn.close()

        user = {
            "last_name": result_set[0][1],
            "first_name": result_set[0][2],
            "user_name": result_set[0][3],
            "account_id": result_set[0][0]
        }
        return json.dumps({"result": True, "data": user})

    except mariadb.Error as e:
        print(f"Error SQL: {e}")
        return json.dumps({"result": False, "error": "Không thể truy vấn csdl"})

# Flask API
@app.route("/")
def main():
    return "chào bạn đến với Hệ thống cơ sở dòng lệnh"


@app.route("/upload/files", methods=['POST'])
def upload_file():
    if request.method == 'POST':
        number_image_files = request.form['number_image_files']
        user_name = request.form['user_name']
        print('So luong anh tai len: ', number_image_files)

        if 'files[]' not in request.files:
            print('No file part')
            # return json.dumps({"result": False, "error": "Không tìm thấy tệp tải lên"})

        files = request.files.getlist('files[]')

        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                new_filename = str(user_name) + "_" + filename.lower()
                    
                file.save(os.path.join(
                    app.config['UPLOAD_FOLDER'], new_filename))

        print('Tải anh lên thành công')
        return json.dumps({"result": True, "message": "Tệp tải lên hoàn tất"})


@app.route('/api/register', methods=['POST'])
def register():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    user_name = request.form['user_name']
    password = request.form['password']

    # kiểm tra xem có tồn tại tài khoản chuẩn bị thêm vào
    try:
        conn = mariadb.connect(**db_config)
    except mariadb.Error as e:
        print(f"\n\nLoi ket noi den MariaDB: {e}\n\n")
        return json.dumps({"result": False, "error": "không thể kết nối đến db"})

    cur = conn.cursor()

    try:
        cur.execute(
            "SELECT account_id FROM Account WHERE user_name=?", (user_name,))

        result_set = cur.fetchall()
        if len(result_set) > 0:
            conn.close()
            return json.dumps({"result": False, "error": "Tài khoản bạn đăng ký đã tồn tại!"})

        try:
            role_id = 3
            cur.execute(
                "INSERT INTO Account(user_name, password, role_id, first_name, last_name) VALUES(?,?,?,?,?)", (user_name, password, role_id, first_name, last_name))
        except mariadb.Error as e:
            print(f"Lỗi thêm mới dữ liệu: {e}")
            conn.close()
            return json.dumps({"result": False, "error": 'Ghi danh không thành công!'})

        conn.commit()
        print(f"ID vừa đc thêm vào là: {cur.lastrowid}")

        conn.close()
        return json.dumps({"result": True, "data": ""})

    except mariadb.Error as e:
        print(f"Error SQL: {e}")
        return json.dumps({"result": False, "error": "Không thể truy vấn csdl"})


@app.route("/api/signin", methods=['POST'])
def check_sign_in():
    user = request.form['user_name']
    password = request.form['password']
    return is_user_exits_with(user, password)

@app.route('/display/<filename>')
def display_image(filename):
	#print('display_image filename: ' + filename)
	return redirect(url_for('static', filename='uploads/' + filename), code=301)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True, threaded=True)
