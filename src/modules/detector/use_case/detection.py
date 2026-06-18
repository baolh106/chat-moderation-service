from abc import ABC, abstractmethod
from src.modules.detector.domain.entities import DetectionResult

class ImageDetectorInterface(ABC):
    @abstractmethod
    def analyze_image(self, image_url: str) -> DetectionResult:
        pass

class ScanImageUseCase:
    def __init__(self, detector: ImageDetectorInterface):
        self.detector = detector

    def execute(self, image_url: str) -> DetectionResult:
        return self.detector.analyze_image(image_url)