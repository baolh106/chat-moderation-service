import cv2
import logging
from nudenet import NudeDetector
from src.shared.utils.image_helper import load_image_from_url, load_image_from_path, is_url
from src.modules.detector.domain.entities import DetectionResult
from src.modules.detector.use_case.detection import ImageDetectorInterface

logger = logging.getLogger("uvicorn.error")

class NudeNetDetector(ImageDetectorInterface):
    def __init__(self):
        # initialize detector
        self.detector = NudeDetector()

    def analyze_image(self, image_url: str) -> DetectionResult:
        try:
            logger.info(f"--- [DETECTOR] Analyzing image: {image_url} ---")
            
            # 1. Sử dụng utility để tải/đọc ảnh
            if is_url(image_url):
                image_mat = load_image_from_url(image_url)
            else:
                image_mat = load_image_from_path(image_url)

            if image_mat is None:
                logger.warning(f"--- [DETECTOR] OpenCV could not read or decode image from {image_url}. image_mat is None. ---")
                return DetectionResult(
                    is_toxic=False, 
                    confidence_score=0.0, 
                    details=[{"error": "Không thể đọc hoặc giải mã ảnh"}]
                )

            # 2. Thực hiện nhận diện (NudeNet hỗ trợ nhận diện trực tiếp từ mảng numpy)
            detection = self.detector.detect(image_mat)
            logger.info(f"--- [DETECTOR] NudeNet detection raw result: {detection} ---")

        except Exception as e:
            logger.exception(f"--- [DETECTOR] An unexpected error occurred during image analysis for {image_url}: {e} ---")
            return DetectionResult(
                is_toxic=False, 
                confidence_score=0.0, 
                details=[{"error": str(e)}]
            )

        is_toxic = len(detection) > 0
        max_score = 0.0

        if is_toxic:
            scores = [item.get('score', 0.0) for item in detection if 'score' in item]
            if scores:
                max_score = max(scores)
            else:
                logger.warning(f"--- [DETECTOR] No 'score' found in detection results for {image_url} despite being toxic. ---")

        return DetectionResult(
            is_toxic=is_toxic,
            confidence_score=max_score,
            details=detection
        )
