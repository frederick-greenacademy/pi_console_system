import ble_socket_server

if __name__ == "__main__":
    # Tạo BLE máy chủ chạy trên port số 3
    # Port BLE hợp lệ là: [0, 3]
    
    server = ble_socket_server.BLEServer(3)
    server.listen()