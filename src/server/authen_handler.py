import sqlalchemy as db
import json
import sys
import decimal
import mariadb


SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://pi:password@127.0.0.1:3306/pi_iot'

# Cau hinh CSDL
engine = db.create_engine(SQLALCHEMY_DATABASE_URI, echo=True)
metadata = db.MetaData()

config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'pi',
    'password': 'password',
    'database': 'pi_iot'
}


def is_user_exits_with(user, passwrd, car_id):

    try:
        conn = mariadb.connect(**config)
    except mariadb.Error as e:
        print(f"Loi ket noi den MariaDB: {e}")
        return json.dumps({"result":"false", "error": "không thể kết nối đến db"})
    
    cur = conn.cursor()

    try: 
        cur.execute(
        "SELECT account_id, password FROM Account WHERE user_name=?", (user,))
        ttt = cur.fetchall()
        if len(ttt) <= 0:
            conn.close()
            return json.dumps({"result":"false", "error": "Không tìm thấy tên tài khoản này: " + user})


        account_id_value = None
        for account_id, password in cur:
            if password == passwrd:
                account_id_value = account_id
                break
        
        if account_id_value != None:
            
            cur.execute(
                "SELECT vehicle_id, status FROM Rent WHERE account_id=? and vehicle_id=? and status=?", 
                (account_id, car_id, 'thuê'))
            
            vehicle_id_value = cur.fetchall()
            conn.close()

            if len(vehicle_id_value) > 0:
                return json.dumps({"result":"true", "message": "Tìm thấy mã xe của tk: " + user})
            else:
                return json.dumps({"result":"false", "error": "Không tìm thấy ma xe: " + car_id})          

        else:
            conn.close()
            return json.dumps({"result":"false", "error": "Mật khẩu của tài khoản này không đúng"})      
    

    except mariadb.Error as e: 
        print(f"Error SQL: {e}")
        return json.dumps({"result":"false", "error": e})

    