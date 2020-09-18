import os
from pathlib import Path
import bluetooth
import pi_local_storage
import json
import pyzbar.pyzbar as pyzbar
import datetime
# import imutils
import time
import cv2
import readline
import shutil
import requests
from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import imutils
import pickle
import struct

url_image_file = 'http://192.168.0.101:8000/display/'

# lấy địa chỉ hiện hành
path = os.getcwd()


def download_image(lable_user_name, file_name):
    # tạo nhãn thư mục ứng với user_name
    file_path = str(Path(path).parents[0]) + "/client/dataset"
    parent_path = os.path.join(file_path, lable_user_name)
    # nếu thư mục dataset chưa có cần tạo mới
    if not os.path.isdir(file_path):
        os.mkdir(file_path)

    full_file_name = lable_user_name + "_" + file_name
    url = url_image_file + full_file_name
    response = requests.get(url, stream=True)
    new_path_file = parent_path + "/" + full_file_name
    with open(new_path_file, 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response

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
    isValid = True
    # Lam sach man hinh Terminal
    # os.system('clear')

    while isValid != False:

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
                    {"command": "manual_signin",
                     "data": message_info}).encode('utf-8'))
            # Hoat
            try:
                data = recv_data(client_socket)
                raw_data = data.decode('utf-8')
                raw_data_json = json.loads(raw_data)

                print("XX:", raw_data_json)
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

def face_recognization():
    try:
        file_path = str(Path(path).parents[0]) + "/client/"

        protoPath = file_path + "/face_detection_model/" + "deploy.prototxt"
        modelPath = file_path + "/face_detection_model/" + "res10_300x300_ssd_iter_140000.caffemodel"
        detector = cv2.dnn.readNetFromCaffe(protoPath, modelPath)
        # load our serialized face embedding model from disk
        print("[INFO] loading face recognizer...")
        embedder = cv2.dnn.readNetFromTorch(file_path + "/openface_nn4.small2.v1.t7")
        # load the actual face recognition model along with the label encoder
        recognizer = pickle.loads(open(file_path + "/output/recognizer.pickle", "rb").read())
        le = pickle.loads(open(file_path + "/output/le.pickle", "rb").read())

        # initialize the video stream, then allow the camera sensor to warm up
        print("[INFO] starting video stream...")
        #vs = VideoStream(usePiCamera=True).start()
        vs = VideoStream(src=0).start()
        continue_run = True
        
        time.sleep(2.0)
        # start the FPS throughput estimator
        fps = FPS().start()
        # loop over frames from the video file stream
        while continue_run != False:
            # grab the frame from the threaded video stream
            frame = vs.read()
            # resize the frame to have a width of 600 pixels (while
            # maintaining the aspect ratio), and then grab the image
            # dimensions
            frame = imutils.resize(frame, width=600)
            (h, w) = frame.shape[:2]
            # construct a blob from the image
            imageBlob = cv2.dnn.blobFromImage(
                cv2.resize(frame, (300, 300)), 1.0, (300, 300),
                (104.0, 177.0, 123.0), swapRB=False, crop=False)
            # apply OpenCV's deep learning-based face detector to localize
            # faces in the input image
            detector.setInput(imageBlob)
            detections = detector.forward()
                # loop over the detections
            for i in range(0, detections.shape[2]):
                # extract the confidence (i.e., probability) associated with
                # the prediction
                confidence = detections[0, 0, i, 2]
                # filter out weak detections
                if confidence > 0.75: ##args["confidence"]
                    # compute the (x, y)-coordinates of the bounding box for
                    # the face
                    box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                    (startX, startY, endX, endY) = box.astype("int")
                    # extract the face ROI
                    face = frame[startY:endY, startX:endX]
                    (fH, fW) = face.shape[:2]
                    # ensure the face width and height are sufficiently large
                    if fW < 20 or fH < 20:
                        continue
                    
                    # construct a blob for the face ROI, then pass the blob
                    # through our face embedding model to obtain the 128-d
                    # quantification of the face
                    faceBlob = cv2.dnn.blobFromImage(face, 1.0 / 255,
                        (96, 96), (0, 0, 0), swapRB=True, crop=False)
                    embedder.setInput(faceBlob)
                    vec = embedder.forward()
                    # perform classification to recognize the face
                    preds = recognizer.predict_proba(vec)[0]
                    j = np.argmax(preds)
                    proba = preds[j]
                    name = le.classes_[j]
                    # draw the bounding box of the face along with the
                    # associated probability
                    text = "{}: {:.2f}%".format(name, proba * 100)
                    y = startY - 10 if startY - 10 > 10 else startY + 10
                    cv2.rectangle(frame, (startX, startY), (endX, endY),
                        (0, 0, 255), 2)
                    cv2.putText(frame, text, (startX, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
                    time.sleep(3.0)		
                    if name != 'unknown':
                        found_user = name
                        continue_run = False
                        break
            # update the FPS counter
            fps.update()
            # show the output frame
            cv2.imshow("Frame", frame)
            key = cv2.waitKey(1) & 0xFF
            # if the `q` key was pressed, break from the loop
            if key == ord("q"):
                break        
            
        # stop the timer and display FPS information
        fps.stop()
        print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
        print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
        # do a bit of cleanup
        cv2.destroyAllWindows()
        vs.stop()
        cv2.waitKey(1)
        
        if found_user != None and found_user != 'unknown':
            return found_user

    except KeyboardInterrupt:
        print("[X] cleaning up - L2")
        cv2.destroyWindow('Barcode Scanner')
        cv2.waitKey(1)
        return None

def scan_qrcode_from_cam():
    try:

        cap = cv2.VideoCapture(0)
        is_valid = True
        founds = None
        while is_valid:
            _, frame = cap.read()
            # frame = imutils.resize(frame, width=1024)
            # Tim barcode trong khung Frame va giai ma
            barcodes = pyzbar.decode(frame)
            # kiem tra neu co nhieu barcodes

            for barcode in barcodes:

                (x, y, w, h) = barcode.rect
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

                # Kiem tra thong tin cua barcode
                bar_code_data = barcode.data.decode("utf-8")
                text = "{} ({})".format(bar_code_data, barcode.type)
                cv2.putText(
                    frame, text,
                    (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

                if bar_code_data != None:
                    founds = bar_code_data
                    print("Tim thay du lieu trong QR nhu sau:", bar_code_data)
                    is_valid = False
                    break

            # Hien thi khung frame khi quet
            cv2.imshow("QRScanner", frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord("x"):
                is_valid = False
                break

        print("[X] cleaning up - L1...")
        cv2.destroyWindow('QRScanner')
        cap.release()
        cv2.waitKey(1)
        # Gui QR code den may chu
        if founds != None and is_valid == False:
            return founds
        return None

    except KeyboardInterrupt:
        print("[X] cleaning up - L2")
        cv2.destroyWindow('Barcode Scanner')
        cap.release()
        cv2.waitKey(1)
        return None


def scan_ble_nearby():
    print('Đang quét BLE xung quanh...')

    nearby_devices = bluetooth.discover_devices(
        duration=48, lookup_names=True, flush_cache=True, lookup_class=False
    )
    count = len(nearby_devices)
    print(f"-----Số thiết bị tìm được: {count}-------")

    founds = []
    if count <= 0:
        return founds

    for addr, name in nearby_devices:
        try:
            print(f"{addr.decode('utf-8')} - {name}")
            founds.append(addr.decode("utf-8"))
        except UnicodeEncodeError:
            print(f"{addr} {name.encode('utf-8', 'replace')}")
    print("\n")

    return founds


def listen_user_enter_on_socket():
    print("\t**********************************************************")
    print("\t\tDANH SÁCH LỆNH [x] thao tác với Máy Chủ")
    print("\t\t[1] Đăng nhập vào hệ thống bằng gởi lệnh")
    print("\t\t[2] Đăng nhập bằng dùng khuôn mặt")
    print("\t\t[3] Hệ thống nhận diện bằng Bluetooth")
    print("\t\t[4] Quét mã QR để lấy thông tin ")
    print("\t\t[:quit] Đóng kết nối với máy chủ.")
    print("\t**********************************************************\n\n")

    return input("Chọn: ")

def recv_msg(sock):
    # Read message length and unpack it into an integer
    raw_msglen = recvall(sock, 4)
    if not raw_msglen:
        return None
    msglen = struct.unpack('>I', raw_msglen)[0]
    # Read the message data
    return recvall(sock, msglen)

def recvall(sock, n):
    # Helper function to recv n bytes or return None if EOF is hit
    data = bytearray()
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data.extend(packet)
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

        pi_local_storage.read_config()

        # print("Gõ thông điệp gửi đi và nhấn Enter để kết thúc:")
        try:
            # Thực hiện kết nối đến máy chủ với: BLE MAC và cổng
            self.client.connect((self.server_ble_addr, self.server_port))

            try:
                json_data = recv_msg(self.client)
                print('My JSON at Local:', json_data)
                raw_data_json = json.loads(json_data.decode("utf-8"))
                
                # data = recv_data(self.client)
                # raw_data = data.decode('utf-8')
                # raw_data_json = json.loads(raw_data)

                print("\n\nDữ liệu đc gởi từ máy chủ:", raw_data_json)
                command = raw_data_json.get('command', None)
                if command != None:
                    if command == 'update_data':
                        data_will_update = raw_data_json["data"]
                        # print("\n\nDữ liệu can dc update:", data_will_update)
                        pi_local_storage.add_list_data(data_will_update)
                        pi_local_storage.save_config()

                        
                        images_list = raw_data_json["images"]
                        # print("DS ảnh cần tải về: ", images_list)
                        for item in images_list:
                            user_name = item["user_name"]
                            file_name = item["file_name"]
                            # print("\n\nDia chi hien hanh", path)
                            download_image(lable_user_name=user_name, file_name=file_name)
                            # print(item["user_name"])


            except Exception as f:
                print("\n\n2.--Lỗi nhan du lieu Tai máy khách là:", f)

            while True:

                # text = input("Gõ thông điệp để gởi. Nhấn Enter để kết thúc.\n") # Nghe thông tin gõ trên bàn phím

                # os.system('clear')

                # Lắng nghe thông điệp gõ trên socket
                choice = listen_user_enter_on_socket()

                if choice == ":quit" or choice == ":exit":
                    self.client.send(choice.encode('utf-8'))
                    break

                if choice == '1':
                    manual_signin(self.client)

                elif choice == '2':
                    user_recognization = face_recognization()
                    print('\n\nĐã tìm thấy: ', user_recognization)
                    if user_recognization != 'unknown'  and user_recognization != None:
                        print('\n\nĐã tìm thấy: ', user_recognization)

                elif choice == '3':
                    founds = scan_ble_nearby()
                    config = pi_local_storage.get_config()

                    if config != None and len(founds) > 0:
                        is_found = False
                        for x in founds:
                            if x in config["items"]:
                                print(f"\n\nBluetooth: {x} tìm thấy.")
                                print("Bạn có thể dùng nó để mở cửa")
                                is_found = True
                                break
                        if is_found == False:
                            print("\n\nThiết bị của bạn chưa được đăng ký")

                elif choice == '4':
                    qr = scan_qrcode_from_cam()

                    if qr != None:
                        message = { "command": "qr_scanned", "data": qr }
                        # print('XXXXXX-XXXX-YYYY', message)
                        self.client.send(json.dumps(message).encode('utf-8'))

                        try:
                            data = recv_data(self.client)
                            raw_data = data.decode('utf-8')
                            raw_data_json = json.loads(raw_data)
                            command = raw_data_json.get('command', None)
                            if command != None:
                                if command == 'show_qr_info':
                                    data_will_show = raw_data_json["data"]
                                    print('\n\nThông tin chi tiết của mã QR là: ', data_will_show)

                        except Exception as f:
                            print("\n\nLỗi nhan du lieu Tai máy khách là:", f)

            self.client.close()
        except KeyboardInterrupt as ex:
            print("Có lỗi xuất hiện: ", ex)
            self.client.send(":quit".encode('utf-8'))
            self.client.close()
