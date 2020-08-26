# import thread module 
from _thread import start_new_thread
import threading 
import bluetooth

backlog = 1

server_thread_lock = threading.Lock() 

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

def threaded(c, ble_cli_addr):

    try:
        while True:
            # dữ liệu nhận được 
            data = recv_data_from(c) 
            print('Máy chủ nhận được dữ liệu: ', data)

            if str(data) == 'quit' or str(data) == 'exit': 
                print('Ngắt kết nối từ: ', ble_cli_addr) 
                
                # Luồng khóa đã được nhả ra
                server_thread_lock.release() 
                break
    
            # reverse the given string from client 
            # data = data[::-1] 
    
            # Gởi dữ liệu quay trở lại máy khách...
            c.send(data)

    except:
        # Nhả luồng đã khóa sau khi máy khách ngắt kết nối
        server_thread_lock.release()
        # đóng máy khách
        c.close()
  
    # đóng máy khách
    c.close() 


class BLEServer:
    
    def __init__(self, server_port):
        super().__init__()
        self.server_port = server_port
        self.server = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.bltaddr = bluetooth.read_local_bdaddr()
        print("Địa chỉ BLE máy chủ: ", str(self.bltaddr[0]))

    def listen(self):
        # Máy chủ sẽ đính kèm vào địa chỉ BLE và cổng của chính nó 
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
        