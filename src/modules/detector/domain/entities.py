from pydantic import BaseModel
from typing import List, Dict

class DetectionResult(BaseModel):
    is_toxic: bool
    confidence_score: float
    details: List[Dict]