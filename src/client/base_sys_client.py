import os
import requests
import bluetooth
import ble_socket_client

# Dinh nghia cac tinh nang

def message_for_welcome():
    # Lam sach man hinh Terminal
    os.system('clear')
              
    print("\t************************************************")
    print("\t*** Chào mừng đến với Chương trình dòng lệnh ***")
    print("\t************************************************")
    
def get_user_choice():
    # Thu thap lua chon cua nguoi dung
    print("\nChọn tên chương trình [x] và gõ Enter để kết thúc!")
    print("DANH SÁCH:")
    print("[-2] Quét địa chỉ MAC của Bluetooth xung quanh")
    print("[-1] Kết nối đến Máy Chủ bằng địa chỉ Bluetooth")
    print("[:q] Thoát.")
    
    return input("Chọn: ")
    
def manual_signin():

    isValid = False
    
    while isValid != True:
        info_singin = input("\nCung cap: ten dang nhap, mat khau, ma xe ID. Nhung thong tin nay cach nhau boi khoang trang.\nVd: run_hockey  mat_khau_123 car_id_0001\n\n")
        info_array = info_singin.split(' ')
        
        if len(info_array) == 3:
            print("Ban da dien: %s" % info_singin)
            url = 'http://127.0.0.1:8000/api/signin'
            data = {"user_name": info_array[0], "password": info_array[1], "car_id": info_array[2]}
            response = requests.post(url, data=data)

            # Kiem tra ket qua phan hoi
            res = response.json()
            if len(res) > 0 :
                if res["result"] == "true":
                    isValid = True
                else:
                    print("Thong tin dang nhap khong ton tai!")  
        else:
            print("Thong tin ban nhap khong day du!")    

def connect_ble_server():
    
    is_Valid = True
    while is_Valid != False:
        ble_addr_input = input('Gõ địa chỉ Bluetooth của Máy Chủ: ')

        if len(ble_addr_input) == 17:
            print('Chuẩn bị kết nối đến địa chỉ: ', ble_addr_input)

            # Tạo BLE bluetooth socket cho máy khách 
            ble_client = ble_socket_client.BLEClient(ble_addr_input, 3)
            ble_client.connect()

            is_Valid = False
        elif len(ble_addr_input) > 0 and len(ble_addr_input) < 17:
            print('Địa chỉ Bluetooth không đúng. Địa chỉ giống như sau: A0:52:00:C7:4X:00')


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

        
def facial_recognition_sys():
    print("\n")


def qr_scan_recognition_sys():
    print("\n")

def ble_scan_recognition_sys():
    
    # cprint('\nQuét BLE...', 'red', attrs=['blink'])
    nearby_devices = bluetooth.discover_devices(
        duration=48, lookup_names=True, flush_cache=True, lookup_class=False
    )
    count = len(nearby_devices)
    print(f"Số thiết bị tìm được {count}")

    ble_mac_adds = []
    for addr, name in nearby_devices:
        try:
            ble_mac_adds.append(str(addr))
            print(f"{addr} - {name}")
        except UnicodeEncodeError:
            print(f"{addr} {name.encode('utf-8', 'replace')}")

    if len(ble_mac_adds) > 0:
        for e in ble_mac_adds:
            if e == "E9:C6:06:B5:65:90":
                print(f"Đã tìm thấy.")

if __name__ == "__main__":
    names = []

    choice = ''
    message_for_welcome()

    while choice != ':q':    
        
        
        # Respond to the user's choice.
        # message_for_welcome()
        
        choice = get_user_choice()

        if choice == '-2':
            scan_ble_nearby()
        elif choice == '-1':
            connect_ble_server()    
        # elif choice == '1':
        #     manual_signin()
        # elif choice == '2':
        #     facial_recognition_sys()
        # elif choice == '3':
        #     qr_scan_recognition_sys()
        # elif choice == '4':
        #     ble_scan_recognition_sys()    
        elif choice == ':q':
            print("\nTạm biệt. Hẹn gặp lại!")
        elif choice != None:
            print("\nLựa chọn không tìm thấy. Vui lòng chọn lại")