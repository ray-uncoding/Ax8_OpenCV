# Ax8_OpenCV

## 概述
Ax8_OpenCV 是一個基於 PyQt 的應用程式，用於與 AX8 相機系統進行互動。該專案提供模組化且可擴展的架構，支援即時影像串流、物件偵測以及系統監控。專案使用 PyQt 作為使用者介面框架，YOLO 作為物件偵測模型，並包含多個實用工具模組來處理數據與記錄。

---

## 專案結構
```
Ax8_OpenCV
├── main.py                     # 應用程式的進入點
├── src
│   ├── config
│   │   └── yolov8n.pt          # YOLO 模型檔案
│   ├── core
│   │   ├── ax8_manager.py      # 管理相機連線、影像抓取與會話處理
│   │   ├── ax8_worker.py       # 處理影像串流的執行緒操作
│   │   ├── yolo_processor.py   # 封裝 YOLO 模型進行物件偵測
│   ├── ui
│   │   ├── main_window.py      # 主應用程式視窗
│   │   ├── camera_widget.py    # 顯示相機影像與偵測結果的元件
│   │   └── status_bar.py       # 顯示連線與偵測資訊的狀態列
│   ├── utils
│   │   ├── data_processor.py   # 計算 FPS 的工具
│   │   ├── logger.py           # 可配置的日誌記錄模組
│   │   └── parameter_logger.py # 將偵測參數記錄到 CSV 檔案
├── requirements.txt            # 專案依賴項
├── .gitignore                  # Git 忽略規則
└── README.md                   # 專案文件
```

---

## 安裝

### 先決條件
- Python 3.8 或更高版本
- pip（Python 套件管理工具）

### 安裝步驟
1. 複製此專案：
   ```bash
   git clone <repository-url>
   cd Ax8_OpenCV
   ```

2. 安裝所需的依賴項：
   ```bash
   pip install -r requirements.txt
   ```

3. （可選）建立虛擬環境：
   ```bash
   python -m venv env
   source env/bin/activate  # Windows 系統使用：env\Scripts\activate
   ```

---

## 使用方式

執行以下指令啟動應用程式：
```bash
python main.py
```

啟動後，應用程式將顯示 PyQt 視窗，允許您連接到 AX8 相機並查看即時影像與相關數據。

---

## 系統架構與工作流程

### **1. 相機連線與影像抓取**
- **模組**：`ax8_manager.py`
- **描述**：
  - 管理與 AX8 相機的連線。
  - 處理登入、影像抓取以及透過執行緒維持會話。
- **關鍵方法**：
  - `login()`: 驗證相機的使用者名稱與密碼。
  - `fetch_frame()`: 抓取相機的最新影像。
  - `start_keep_alive()`: 透過定期請求維持會話。

### **2. 影像串流與處理**
- **模組**：`ax8_worker.py`
- **描述**：
  - 啟動執行緒以持續抓取影像。
  - 發送信號更新 UI，顯示最新影像與連線狀態。
- **關鍵信號**：
  - `image_update`: 傳遞最新影像到 UI。
  - `connection_status`: 更新狀態列中的連線狀態。

### **3. YOLO 物件偵測**
- **模組**：`yolo_processor.py`
- **描述**：
  - 封裝 YOLO 模型進行物件偵測。
  - 處理每一幀影像並返回偵測結果。
- **關鍵方法**：
  - `predict(frame)`: 對輸入影像進行 YOLO 推論。

### **4. 使用者介面**
- **模組**：`main_window.py`, `camera_widget.py`, `status_bar.py`
- **描述**：
  - **`main_window.py`**：整合所有 UI 元件的主應用程式視窗。
  - **`camera_widget.py`**：顯示相機影像並疊加偵測結果。
  - **`status_bar.py`**：顯示連線狀態、FPS 與偵測參數。
- **工作流程**：
  1. `CameraWidget` 從 `AX8Worker` 抓取影像。
  2. 將影像傳遞給 `YOLOProcessor` 進行偵測。
  3. 在 UI 上顯示偵測結果。

### **5. 工具模組**
- **模組**：`data_processor.py`, `logger.py`, `parameter_logger.py`
- **描述**：
  - **`data_processor.py`**：計算影像串流的 FPS。
  - **`logger.py`**：配置日誌記錄，用於除錯與監控。
  - **`parameter_logger.py`**：將 FPS 與推論時間記錄到 CSV 檔案。

---

## 功能

### **1. 即時相機影像**
- 顯示來自 AX8 相機的即時影像串流。
- 支援使用 YOLO 進行即時物件偵測。

### **2. 連線監控**
- 提供連線狀態的視覺化指示。
- 自動維持會話，防止連線中斷。

### **3. FPS 監控**
- 計算並顯示影像串流的每秒幀數。

### **4. 物件偵測**
- 整合 YOLO 模型，對影像中的物件進行偵測。
- 在影像上顯示偵測結果（如邊界框與標籤）。

### **5. 參數記錄**
- 將 FPS 與推論時間記錄到 CSV 檔案，便於後續分析。

---

## 開發筆記

### **1. 新增 YOLO 模型**
- 更新 `yolo_processor.py` 中的模型路徑。
- 確保模型與 `ultralytics` 庫相容。

### **2. 除錯**
- 使用 `logger.py` 模組啟用詳細日誌記錄。
- 日誌將存儲於循環檔案中，避免磁碟空間不足。

### **3. 系統擴展**
- 若需支援多相機：
  - 建立多個 `AX8Manager` 與 `CameraWidget` 實例。
  - 在 `main_window.py` 中使用分頁介面切換相機。

---

## 貢獻
歡迎貢獻！請提交 Pull Request 或開啟 Issue 來提出改進建議或修復問題。

---

## 授權
此專案採用 MIT 授權條款。詳情請參閱 LICENSE 文件。