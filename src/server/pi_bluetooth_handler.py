# import thread module
from _thread import start_new_thread
import threading
import bluetooth
import json
import business_handler
import schedule
import sched
import time

backlog = 1

# Khai báo luồng khóa
server_thread_lock = threading.Lock()

s = sched.scheduler(time.time, time.sleep)

# xử lý khi dữ liệu nhận có kích thước lớn hơn 4 KiB


def recv_data_from(sock):
    BUFF_SIZE = 4096  # 4 KiB
    data = b''
    while True:
        part = sock.recv(BUFF_SIZE)
        data += part
        if len(part) < BUFF_SIZE:
            # either 0 or end of data
            break
    return data


def do_check_new_data(c, ble_cli_addr):
    print(time.time())
    print("Run: -----------------------")
    data_needs_update = business_handler.get_bluetooth_list(
        ble_cli_addr=ble_cli_addr)
    message_info = {
        "command": "update_data", "data": data_needs_update}
    c.send(json.dumps(message_info).encode('utf-8'))
    print(time.time())


# Xử lý từng luồng cho từng Máy Khách
# kết nối đến máy chủ
def threaded(c, ble_cli_addr):

    try:
        # data_needs_update = business_handler.get_bluetooth_list(ble_cli_addr=ble_cli_addr)
        # message_info = {
        #         "command": "update_data", "data": data_needs_update}
        # c.send(json.dumps(message_info).encode('utf-8'))

        while True:
            now = time.time()
            s.enterabs(now + 1, 1, do_check_new_data,
                       argument=(c, ble_cli_addr))
            t = threading.Thread(target=s.run)
            t.start()
            t.join()

            # dữ liệu nhận được
            data = recv_data_from(c)

            raw_data = data.decode("utf-8")
            # print('Máy chủ nhận được dữ liệu: ', raw_data)

            if raw_data == ':quit' or raw_data == ':exit':
                print('Ngắt kết nối từ: ', ble_cli_addr)

                # Luồng khóa đã được nhả ra
                server_thread_lock.release()
                break

            raw_data_json = json.loads(raw_data)
            action = raw_data_json.get('command', None)

            if action != None:  # kiem tra raw_data co phai la tu dien

                content = raw_data_json['data']

                if action == "manual_signin":

                    print(f"Thông tin của manual_signin nhận được: {content}")

                    user_name = content['user_name']
                    password = content['password']
                    car_id = content['car_id']

                    message = business_handler.is_user_exits_with(
                        user_name, password, car_id)
                    if message != None:
                        c.send(message.encode('utf-8'))
                        print("Gởi thông tin về máy khách:", message)

                elif action == 'qr_scanned':
                    print(f"Thông tin của qr code quét được: {content}")
                    message = business_handler.get_account_info(content)
                    if message != None:
                        message_info = {
                            "command": "show_qr_info", "data": message["message"]}
                        c.send(message_info.encode('utf-8'))
                        print("Gởi thông tin về máy khách:", message_info)

            # reverse the given string from client
            # data = data[::-1]

            # Gởi dữ liệu quay trở lại máy khách...
            # if data != None:
            #     c.send(data)

    except:
        # Nhả luồng đã khóa sau khi máy khách ngắt kết nối
        server_thread_lock.release()
        # đóng máy khách
        c.close()
        print('Đã ngắt kết nối: ', ble_cli_addr)

    # đóng máy khách
    # Không nên nhả ổ khóa luồng tiến trình ở đây.
    # chỉ nên gọi đóng kết nối của máy khách.
    c.close()
    print('Đóng ngắt kết nối: ', ble_cli_addr)


class BLEServer:

    def __init__(self, server_port):
        super().__init__()
        self.server_port = server_port
        self.server = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.bltaddr = bluetooth.read_local_bdaddr()
        print("Địa chỉ BLE máy chủ: ", str(self.bltaddr[0]))

    def listen(self):
        # Máy chủ sẽ đính kèm vào địa chỉ BLE và cổng của chính nó
        try:
            self.server.bind((self.bltaddr[0], self.server_port))
            self.server.listen(backlog)
            print("Máy chủ đang lắng nghe trên socket BLE...")
            while True:
                c, addr = self.server.accept()
                # khóa một luồng hiện tại
                server_thread_lock.acquire()
                print('Máy khách kết nối có địa chỉ :',
                      addr[0], '- tại cổng: ', addr[1])

                # Tạo một luồng mới và trả về một nhận diện của chính nó
                start_new_thread(threaded, (c, addr[0]))
        except KeyboardInterrupt as ki:
            print('Máy chủ sẽ ngắt kết nối vì lỗi:', ki)
            self.server.close()
