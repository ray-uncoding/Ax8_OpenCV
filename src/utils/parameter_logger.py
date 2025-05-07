import csv
import os
from datetime import datetime

class ParameterLogger:
    def __init__(self, log_file="parameter_log.csv", headers=None):
        self.log_file = log_file
        self.headers = headers or ["Timestamp", "FPS", "Inference Time (ms)"]
        self.init_log_file()

    def init_log_file(self):
        """初始化記錄檔案，寫入標題行"""
        if not os.path.exists(self.log_file):
            with open(self.log_file, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(self.headers)

    def log_parameters(self, *args):
        """記錄參數到 CSV 文件"""
        with open(self.log_file, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            writer.writerow([timestamp, *args])