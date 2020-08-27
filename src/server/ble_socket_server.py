# import thread module 
from _thread import start_new_thread
import threading 
import bluetooth

backlog = 1

# Khai báo luồng khóa 
server_thread_lock = threading.Lock() 

# xử lý khi dữ liệu nhận có kích thước lớn hơn 4 KiB 
def recv_data_from(sock):
    BUFF_SIZE = 4096 # 4 KiB
    data = b''
    while True:
        part = sock.recv(BUFF_SIZE)
        data += part
        if len(part) < BUFF_SIZE:
            # either 0 or end of data
            break
    return data

# Xử lý từng luồng cho từng Máy Khách 
# kết nối đến máy chủ
def threaded(c, ble_cli_addr):

    try:
        c.send(f"{ble_cli_addr} đã được kết nối!".encode('utf-8'))
        while True:
            # dữ liệu nhận được 
            data = recv_data_from(c) 
            
            raw_data = data.decode("utf-8")
            print('Máy chủ nhận được dữ liệu: ', raw_data)

            if raw_data == ':quit' or raw_data == ':exit': 
                print('Ngắt kết nối từ: ', ble_cli_addr) 
                
                # Luồng khóa đã được nhả ra
                server_thread_lock.release()
                c.close()
                break
    
            # reverse the given string from client 
            # data = data[::-1] 
    
            # Gởi dữ liệu quay trở lại máy khách...
            if data != None:
                c.send(data)

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
                    print('Máy khách kết nối có địa chỉ :', addr[0], '- tại cổng: ', addr[1]) 
            
                    # Tạo một luồng mới và trả về một nhận diện của chính nó 
                    start_new_thread(threaded, (c, addr[0]))
        except KeyboardInterrupt as ki:
            print('Máy chủ sẽ ngắt kết nối vì lỗi:', ki)
            self.server.close()


        # KeyboardInterrupt
        