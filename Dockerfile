# ================================================
# Giai đoạn 1: Build dependencies (Cài đặt thư viện)
# ================================================
FROM python:3.11-slim AS builder

WORKDIR /app

# Khai báo biến môi trường tối ưu cho quá trình build bằng Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 🚀 TỐI ƯU 1: Tách riêng việc copy requirements để tận dụng Docker Cache Layer
COPY requirements.txt .

# 🚀 TỐI ƯU 2:
RUN pip install --no-cache-dir --user -r requirements.txt

# ================================================
# Giai đoạn 2: Runtime image (Bản chạy chính thức trên Production)
# ================================================
FROM python:3.11-slim AS runner

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/home/appuser/.local/bin:$PATH"

# Cài đặt thư viện hệ thống bắt buộc cho OpenCV và NudeNet
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# 🚀 TỐI ƯU 3: Bảo mật - Tạo một User thường, KHÔNG chạy bằng quyền ROOT
RUN useradd --create-home appuser
USER appuser

# Copy thư viện từ Stage builder sang đúng thư mục của User mới tạo
COPY --from=builder /root/.local /home/appuser/.local

# Copy source code và gán quyền sở hữu (chown) cho appuser
COPY --chown=appuser:appuser . .

# Mở cổng giao tiếp
EXPOSE 6000

# 🚀 TỐI ƯU 4: Sử dụng cấu trúc mảng JSON cho CMD để tránh lỗi Signal Handling (Zombi Process)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "6000", "--workers", "4"]