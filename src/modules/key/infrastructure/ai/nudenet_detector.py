from nudenet import NudeDetector
from modules.detector.domain.entities import ModerationResult
from modules.detector.use_case.moderation import ImageDetectorInterface

class NudeNetDetector(ImageDetectorInterface):
    def __init__(self):
        self.detector = NudeDetector()

    def analyze_image(self, image_url: str) -> ModerationResult:
        detection = self.detector.detect(image_url)

        is_toxic = len(detection) > 0
        max_score = 0.0

        if is_toxic:
            max_score = max([item.get('score', 0 ) for item in detection])

        return ModerationResult(
            is_toxic=is_toxic,
            confidence_score=max_score,
            details=detection
        )

