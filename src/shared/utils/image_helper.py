import re
import requests
import cv2
import numpy as np
import logging
from typing import Optional

logger = logging.getLogger("uvicorn.error")

def convert_to_direct_link(url: str) -> str:
    """
    Chuyển đổi link Google Drive share sang link tải trực tiếp.
    """
    if "drive.google.com" in url and "/file/d/" in url:
        file_id = re.search(r"/file/d/([^/]+)", url)
        if file_id:
            return f"https://drive.google.com/uc?export=download&id={file_id.group(1)}"
    return url

def load_image_from_url(url: str, timeout: int = 10) -> Optional[np.ndarray]:
    """
    Tải ảnh từ URL (hỗ trợ Google Drive) và giải mã thành mảng numpy (OpenCV).
    """
    try:
        download_url = convert_to_direct_link(url)
        response = requests.get(download_url, timeout=timeout)
        
        if response.status_code != 200:
            logger.warning(f"--- [UTILS] Failed to download image. Status: {response.status_code} URL: {url} ---")
            return None
        
        file_bytes = np.frombuffer(response.content, dtype=np.uint8)
        return cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    except Exception as e:
        logger.error(f"--- [UTILS] Error loading image from URL {url}: {e} ---")
        return None

def load_image_from_path(path: str) -> Optional[np.ndarray]:
    """
    Đọc ảnh từ đường dẫn tệp cục bộ.
    """
    try:
        return cv2.imread(path)
    except Exception as e:
        logger.error(f"--- [UTILS] Error loading image from path {path}: {e} ---")
        return None

def is_url(path: str) -> bool:
    """Kiểm tra xem chuỗi có phải là URL hay không."""
    return path.startswith(("http://", "https://"))