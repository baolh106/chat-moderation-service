from abc import ABC, abstractmethod
from modules.detector.domain.entities import ModerationResult

class ImageDetectorInterface(ABC):
    @abstractmethod
    def analyze_image(self, image_url: str) -> ModerationResult:
        pass

class ScanImageUseCase:
    def __init__(self, detector: ImageDetectorInterface):
        self.detector = detector

    def execute(self, image_url: str) -> ModerationResult:
        return self.detector.analyze_image(image_url)