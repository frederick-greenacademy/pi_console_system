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


SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://pi:password@127.0.0.1:3306/pi_iot'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Cau hinh CSDL
engine = db.create_engine(SQLALCHEMY_DATABASE_URI, echo=True)
metadata = db.MetaData()
connection = engine.connect()
# print(engine.table_names())


@app.route("/")
def main():
    return "chào bạn đến với Hệ thống cơ sở dòng lệnh"


@app.route("/api/signin", methods=['POST'])
def check_sign_in():
    _user_name = request.form['user_name']
    _password = request.form['password']
    _car_id = request.form['car_id']


    acc = db.Table('Account', metadata, autoload=True, autoload_with=engine)
    #Lệnh điều tra với tham số: định danh, mật khẩu, mã xe
    query = db.select([acc]).where(
        db.and_(acc.columns.user_name == _user_name,
        db.and_(acc.columns.password == _password,
        acc.columns.car_id == _car_id)))

    # thuc thi cau lenh query
    result_proxy = connection.execute(query)
    # Hứng kết quả vào result_set
    result_set = result_proxy.fetchall()

    result_proxy.close()

    if len(result_set) > 0:
        return json.dumps({"result":"true"})
    else:
        return json.dumps({"result":"false"})


if __name__ == "__main__":
    app.run(port=8000)
