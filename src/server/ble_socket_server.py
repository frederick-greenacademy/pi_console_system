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

def threaded(c):

    try:
        while True:
            # data received from client 
            
            data = recv_data_from(c) 
            print('Sever received: ', data)
            if str(data) == 'quit' or str(data) == 'exit': 
                print('Bye') 
                
                # lock released on exit 
                server_thread_lock.release() 
                break
    
            # reverse the given string from client 
            # data = data[::-1] 
    
            # send back reversed string to client 
            c.send(data)

    except:
        server_thread_lock.release() 
        c.close()
  
    # connection closed 
    c.close() 


class BLEServer:
    
    def __init__(self, server_port):
        super().__init__()
        self.server_port = server_port
        self.server = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.bltaddr = bluetooth.read_local_bdaddr()
        print("Địa chỉ BLE máy chủ: ", str(self.bltaddr[0]))

    def listen(self):
        self.server.bind((self.bltaddr[0], self.server_port))
        self.server.listen(backlog)
        print("Lang nghe tren socket")
        while True:
                c, addr = self.server.accept()
                print('Sender: ', str(addr))

                # lock acquired by client 
                server_thread_lock.acquire()
                print('Connected to :', addr[0], ':', addr[1]) 
        
                # Start a new thread and return its identifier 
                start_new_thread(threaded, (c,))
        