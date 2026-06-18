# AI Chat Moderation Service

## 🚀 Giới thiệu

**AI Chat Moderation Service** là một dịch vụ backend được xây dựng bằng FastAPI, Python, sử dụng mô hình AI NudeNet để tự động phát hiện và kiểm duyệt nội dung không phù hợp (như ảnh khỏa thân, khiêu dâm) trong hình ảnh. Dịch vụ này được thiết kế để tích hợp dễ dàng vào các ứng dụng chat, diễn đàn hoặc bất kỳ nền tảng nào cần kiểm duyệt hình ảnh theo thời gian thực.

## ✨ Tính năng nổi bật

-   **Phát hiện nội dung không phù hợp:** Sử dụng NudeNet để phân tích hình ảnh và xác định mức độ độc hại.
-   **API Key Authentication:** Bảo mật API bằng cách yêu cầu `x-api-key` trong header, được quản lý và xác thực qua MongoDB.
-   **Hỗ trợ đa nguồn ảnh:** Có khả năng tải và xử lý hình ảnh từ URL (bao gồm cả link Google Drive đã chia sẻ) hoặc từ đường dẫn cục bộ.
-   **Xử lý lỗi mạnh mẽ:** Tích hợp các middleware xử lý lỗi tùy chỉnh cho HTTP, lỗi xác thực request và các lỗi không mong muốn khác.
-   **Dockerized:** Dễ dàng triển khai và mở rộng bằng Docker.
-   **Cấu trúc dự án rõ ràng:** Tuân thủ kiến trúc phân lớp (layered architecture) giúp dễ bảo trì và phát triển.

## 🛠️ Công nghệ sử dụng

-   **Backend Framework:** FastAPI
-   **ASGI Server:** Uvicorn
-   **AI Model:** NudeNet (dựa trên PyTorch)
-   **Xử lý ảnh:** OpenCV (`cv2`), NumPy
-   **HTTP Client:** `requests`
-   **Database:** MongoDB (sử dụng `motor` cho async driver)
-   **Quản lý biến môi trường:** `python-dotenv`
-   **Containerization:** Docker

## 🚀 Bắt đầu

### Yêu cầu

-   Python 3.11+
-   pip
-   Một instance MongoDB đang chạy (local hoặc cloud)
-   Docker (tùy chọn, nếu muốn triển khai bằng Docker)

### Cài đặt

1.  **Clone repository:**
    ```bash
    git clone https://github.com/your-username/chat-moderation-service.git
    cd chat-moderation-service
    ```

2.  **Tạo và kích hoạt môi trường ảo:**
    ```bash
    python -m venv venv
    # Trên Windows
    .\venv\Scripts\activate
    # Trên Linux/macOS
    source venv/bin/activate
    ```

3.  **Cài đặt các thư viện cần thiết:**
    ```bash
    pip install -r requirements.txt
    ```

### Cấu hình biến môi trường

Tạo một file `.env` ở thư mục gốc của dự án với các biến sau:

```dotenv
# MongoDB Connection
MONGO_URI="mongodb://localhost:27017/"
API_KEY_COLLECTION="service_keys" # Tên collection chứa API Keys

# Application Settings
APP_HOST="0.0.0.0"
APP_PORT="8000"
APP_RELOAD="True" # Đặt False cho môi trường production
```

### Chạy ứng dụng cục bộ

Đảm bảo môi trường ảo đã được kích hoạt và bạn đang ở thư mục gốc của dự án.

```bash
uvicorn main:app --reload
```
Dịch vụ sẽ chạy trên `http://0.0.0.0:8000` (hoặc cổng bạn đã cấu hình).

## 💡 Sử dụng API

### Xác thực (Authentication)

Tất cả các endpoint yêu cầu một `x-api-key` hợp lệ trong header của request. API Key này phải tồn tại trong collection `service_keys` của MongoDB và có `is_active: true`.

### Endpoint: `POST /api/v1/detect`

Kiểm duyệt một hình ảnh dựa trên URL được cung cấp.

-   **URL:** `/api/v1/detect`
-   **Method:** `POST`
-   **Headers:**
    -   `Content-Type: application/json`
    -   `x-api-key: YOUR_API_KEY`
-   **Request Body (JSON):**
    ```json
    {
      "image_url": "https://example.com/path/to/your/image.jpg"
    }
    ```
-   **Response (JSON):**
    ```json
    {
      "status": "success",
      "data": {
        "is_toxic": true,
        "confidence_score": 0.9876,
        "details": [
          {
            "box_2d": [100, 50, 200, 150],
            "score": 0.9876,
            "label": "EXPOSED_BREAST"
          }
        ]
      }
    }
    ```
    Hoặc khi có lỗi:
    ```json
    {
      "status": "error",
      "message": "Không thể đọc hoặc giải mã ảnh",
      "details": [{"error": "Không thể đọc hoặc giải mã ảnh"}]
    }
    ```

## 🐳 Triển khai với Docker

Dự án này đi kèm với một `Dockerfile` được tối ưu hóa cho quá trình build nhiều giai đoạn (multi-stage build) và bảo mật.

1.  **Build Docker image:**
    ```bash
    docker build -t chat-moderation-service .
    ```

2.  **Chạy Docker container:**
    ```bash
    docker run -d -p 6000:6000 --name moderation-app \
      -e MONGO_URI="mongodb://your_mongo_host:27017/" \
      -e API_KEY_COLLECTION="service_keys" \
      chat-moderation-service
    ```
    Thay thế `your_mongo_host` bằng địa chỉ MongoDB của bạn.

## 🤝 Đóng góp

Mọi đóng góp đều được hoan nghênh! Vui lòng tạo một issue hoặc gửi pull request.

## 📄 Giấy phép

Dự án này được cấp phép theo giấy phép MIT.