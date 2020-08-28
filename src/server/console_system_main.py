import pi_bluetooth_handler

if __name__ == "__main__":
    # Tạo BLE máy chủ chạy trên port số 3
    # Port BLE hợp lệ là: [0, 3]
    
    server = pi_bluetooth_handler.BLEServer(3)
    server.listen()