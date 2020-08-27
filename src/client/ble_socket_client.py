import bluetooth


def listen_user_enter_on_socket():
    print("DANH SÁCH LỆNH [x]")
    print("[1] Đăng nhập vào hệ thống bằng gởi lệnh")
    print("[2] Đăng nhập bằng dùng khuôn mặt")
    print("[3] Mở thiết bị BLE để đăng nhập")
    print("[4] Quét mã QR để lấy thông tin ")
    print("[:quit] Thoát.")
    
    return input("")

def recv_data(sock):
    BUFF_SIZE = 4096 # 4 KiB
    data = b''
    while True:
        part = sock.recv(BUFF_SIZE)
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
                
                text = input("Gõ thông điệp để gởi. Nhấn Enter để kết thúc.\n") # Nghe thông tin gõ trên bàn phím
                
                if text == "quit" or text == "exit":
                    self.client.send(text.encode('utf-8'))
                    self.client.close()
                    break
                
                self.client.send(text.encode('utf-8'))

                data = recv_data(self.client) #self.client.recv(1024)
                print("Data client received from server:", str(data.decode('utf-8')))
            self.client.close()
        except Exception as ex:
            print("Có lỗi xuất hiện: ", ex)
            self.client.close()


# if __name__ == "__main__":
#     client = BLTCClient()
#     client.connect()       
