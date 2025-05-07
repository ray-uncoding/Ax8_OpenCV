import requests
import threading
import time
import cv2
import numpy as np
from ultralytics import YOLO
import os

class AX8Manager:
    def __init__(self, url, username, password):
        self.url = url
        self.username = username
        self.password = password
        self.session = None
        self.running = False
        self.keep_alive_thread = None
        self.keep_alive_running = False

        # 載入 YOLO 模型
        model_path = os.path.join(os.path.dirname(__file__), "../config/yolov8n.pt")
        try:
            self.model = YOLO(model_path)
            print(f"[AX8Manager] 成功載入 YOLO 模型：{model_path}")
        except Exception as e:
            print(f"[AX8Manager] 無法載入 YOLO 模型: {e}")
            self.model = None

    def login(self):
        login_url = self.url.replace("/snapshot.jpg", "/check_login")
        self.session = requests.Session()
        payload = {"_username": self.username, "_password": self.password}
        try:
            response = self.session.post(login_url, data=payload, timeout=5)
            if response.status_code == 200:
                print("[AX8Manager] 登錄成功")
                self.start_keep_alive()
                return True
            else:
                print(f"[AX8Manager] 登錄失敗，HTTP 狀態碼: {response.status_code}")
        except Exception as e:
            print(f"[AX8Manager] 登錄時發生錯誤: {e}")
        return False

    def fetch_frame(self):
        if not self.session:
            print("[AX8Manager] 尚未登錄，無法抓取影像")
            return None
        try:
            response = self.session.get(self.url, stream=True, timeout=2)
            if response.status_code == 200:
                img_arr = np.asarray(bytearray(response.content), dtype=np.uint8)
                frame = cv2.imdecode(img_arr, cv2.IMREAD_COLOR)
                return frame
            else:
                print(f"[AX8Manager] 無法抓取影像，HTTP 狀態碼: {response.status_code}")
        except Exception as e:
            print(f"[AX8Manager] 抓取影像時發生錯誤: {e}")
        return None

    def start_keep_alive(self):
        self.keep_alive_running = True
        self.keep_alive_thread = threading.Thread(target=self._keep_alive_loop, daemon=True)
        self.keep_alive_thread.start()

    def _keep_alive_loop(self):
        while self.keep_alive_running:
            self.keep_alive()
            time.sleep(10)

    def keep_alive(self):
        keep_alive_url = self.url.replace("/snapshot.jpg", "/camera/state")
        try:
            response = self.session.get(keep_alive_url, timeout=5)
            if response.status_code == 200:
                print("[AX8Manager] 心跳請求成功")
            else:
                print(f"[AX8Manager] 心跳請求失敗，HTTP 狀態碼: {response.status_code}")
        except Exception as e:
            print(f"[AX8Manager] 心跳請求時發生錯誤: {e}")

    def stop_keep_alive(self):
        self.keep_alive_running = False
        if self.keep_alive_thread:
            self.keep_alive_thread.join()

    def stop(self):
        self.running = False
        self.stop_keep_alive()