import os
import bluetooth
import json

def manual_signin(client_socket):

    isValid = False
    # Lam sach man hinh Terminal
    os.system('clear')

    while isValid != True:
        
        # Lắng nghe thông tin đưa vào.
        info_singin = input(
            "\nGõ: tên đăng nhập, mật khẩu, mã xe - được cách nhau bởi khoảng trắng.\nVd: user_name_01  mat_khau_1 car_id_0001.\nThông tin: ")
        info_array = info_singin.split(' ')

        if len(info_array) == 3:
            # print("Ban da dien: %s" % info_singin)
            # url = 'http://127.0.0.1:8000/api/signin'
            message_info = {
                "user_name": info_array[0], "password": info_array[1], "car_id": info_array[2]}

            client_socket.send(json.dumps(message_info).encode('utf-8'))
            raw_data = recv_data(client_socket).decode('utf-8')
            
            # Lam sach man hinh Terminal
            os.system('clear')

            print("Dữ liệu nhận từ máy chủ gởi:", raw_data)
            # response = requests.post(url, data=data)

            # # Kiem tra ket qua phan hoi
            # res = response.json()
            # if len(res) > 0 :
            #     if res["result"] == "true":
            #         isValid = True
            #     else:
            #         print("Thong tin dang nhap khong ton tai!")
        else:
            # Lam sach man hinh Terminal
            # os.system('clear')
            print("Thong tin ban nhap khong day du!")


def listen_user_enter_on_socket():
    print("DANH SÁCH LỆNH [x]")
    print("[1] Đăng nhập vào hệ thống bằng gởi lệnh")
    print("[2] Đăng nhập bằng dùng khuôn mặt")
    print("[3] Mở thiết bị BLE để đăng nhập")
    print("[4] Quét mã QR để lấy thông tin ")
    print("[:quit] Thoát.")

    return input("Chọn: ")


def recv_data(client_socket):
    BUFF_SIZE = 4096  # 4 KiB
    data = b''
    while True:
        part = client_socket.recv(BUFF_SIZE)
        data += part
        if len(part) < BUFF_SIZE:
            # either 0 or end of data
            break
    return data


class BLEClient:
    def __init__(self, server_ble_addr, server_port):
        super().__init__()
        bdaddr = bluetooth.read_local_bdaddr()
        print("Địa chỉ BLE máy khách:", bdaddr[0])
        self.server_ble_addr = server_ble_addr
        self.server_port = server_port
        self.client = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

    def connect(self):
        # self.client.connect((serverMACAddress, port))

        # print("Gõ thông điệp gửi đi và nhấn Enter để kết thúc:")
        try:
            # Thực hiện kết nối đến máy chủ với: BLE MAC và cổng
            self.client.connect((self.server_ble_addr, self.server_port))

            while True:

                # text = input("Gõ thông điệp để gởi. Nhấn Enter để kết thúc.\n") # Nghe thông tin gõ trên bàn phím
                
                os.system('clear')

                # Lắng nghe thông điệp gõ trên socket
                choice = listen_user_enter_on_socket()

                if choice == ":quit" or choice == ":exit":
                    self.client.send(choice.encode('utf-8'))
                    self.client.close()
                    break

                if choice == '1':
                    print('')
                    manual_signin(self.client)
                elif choice == '2':
                    print('')
                elif choice == '3':
                    print('')
                elif choice == '4':
                    print('')
                ###
                # Gửi và nhận dữ liệu đến máy chủ socket
                ###
                # self.client.send(choice.encode('utf-8'))
                #data = recv_data(self.client)
                #print("Data client received from server:", str(data.decode('utf-8')))

            self.client.close()
        except Exception as ex:
            print("Có lỗi xuất hiện: ", ex)
            self.client.close()


# if __name__ == "__main__":
#     client = BLTCClient()
#     client.connect()
