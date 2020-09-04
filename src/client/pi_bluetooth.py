import os
import bluetooth
import pi_local_storage
import json
import pyzbar.pyzbar as pyzbar
import datetime
import imutils
import time
import cv2

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

            client_socket.send(
                json.dumps(
                    { "command": "manual_signin", 
                    "data": message_info}).encode('utf-8'))
            
            try:
                data = recv_data(client_socket)
                raw_data = data.decode('utf-8')
                raw_data_json = json.loads(raw_data)
        
                # print("XX:", raw_data_json)
                is_result = raw_data_json['result']
                
                if is_result == 'false':
                     print(u'\n\nLỗi: {}\n\n'.format(raw_data_json['error']))
                else:
                    print(f"\n\n Thông tin: {message_info} đã tìm thấy!!!\n\n")
                    isValid = False

            except Exception as f:
                print("Loi:", f)
            
        else:
            # Lam sach man hinh Terminal
            # os.system('clear')
            print("Thong tin ban nhap khong day du!")

def scan_qrcode_from_came(client_socket):
     
    found = None
    
    try:
        cap = cv2.VideoCapture(0)
        cv2.namedWindow("QRScanner")
        while True:
            _, frame = cap.read()
            frame = imutils.resize(frame, width=1024)
            # Tim barcode trong khung Frame va giai ma
            barcodes = pyzbar.decode(frame)
            # kiem tra neu co nhieu barcodes
            
            for barcode in barcodes:
                
                (x, y, w, h) = barcode.rect
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

                # Kiem tra thong tin cua barcode 
                barcodeData = barcode.data.decode("utf-8")
                print(barcodeData)
                if barcodeData != None:
                    print("add add add")
                    found = barcodeData
                    break

                barcodeType = barcode.type
                # # draw the barcode data and barcode type on the image
                text = "{} ({})".format(barcodeData, barcodeType)
                cv2.putText(
                    frame, text, 
                    (x, y - 10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                
            # Hien thi khung frame khi quet
            cv2.imshow("QRScanner", frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord("x") or found != None:
                break
    
        print("[X] cleaning up...")
        cv2.destroyWindow('QRScanner')
        cap.release()
        cv2.waitKey(1)

    except KeyboardInterrupt:
        print("[X] cleaning up...")
        cv2.destroyWindow('Barcode Scanner')
        cap.release()
        cv2.waitKey(1)
        
def scan_ble_nearby():
    print('Đang quét BLE xung quanh...')

    nearby_devices = bluetooth.discover_devices(
        duration=48, lookup_names=True, flush_cache=True, lookup_class=False
    )
    count = len(nearby_devices)
    print(f"Số thiết bị tìm được: {count}")

    if count <= 0:
        return

    for addr, name in nearby_devices:
        try:
            print(f"{addr} - {name}")
        except UnicodeEncodeError:
            print(f"{addr} {name.encode('utf-8', 'replace')}")

    return nearby_devices           


def listen_user_enter_on_socket():
    print("\nDANH SÁCH LỆNH [x] thao tác với Máy Chủ")
    print("[1] Đăng nhập vào hệ thống bằng gởi lệnh")
    print("[2] Đăng nhập bằng dùng khuôn mặt")
    print("[3] Hệ thống nhận diện bằng Bluetooth")
    print("[4] Quét mã QR để lấy thông tin ")
    print("[:quit] Đóng kết nối với máy chủ.\n")

    return input("Chọn: ")

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
                    
                    break

                    
                if choice == '1':
                    print('')
                    manual_signin(self.client)
                elif choice == '2':
                    print('')
                elif choice == '3':
                    nearby_device = scan_ble_nearby()
                elif choice == '4':
                    scan_qrcode_from_came(self.client)
                    print('')

            self.client.close()
        except KeyboardInterrupt as ex:
            print("Có lỗi xuất hiện: ", ex)
            self.client.send(":quit".encode('utf-8'))
            self.client.close()
