from fastapi import Depends, APIRouter
from pydantic import BaseModel
from src.modules.detector.domain.entities import DetectionResult
from src.modules.detector.infrastructure.ai.nudenet_detector import NudeNetDetector
from src.modules.detector.use_case.detection import ScanImageUseCase
from src.shared.middleware.validate_api_key import validate_api_key

router = APIRouter(prefix="/api/v1", tags=["detector"])

class ImageRequest(BaseModel):
    image_url: str

def get_scan_image_use_case() -> ScanImageUseCase:
    detector = NudeNetDetector()
    return ScanImageUseCase(detector)

@router.post("/detect")
def scan_image_endpoint(
    request: ImageRequest,
    use_case: ScanImageUseCase = Depends(get_scan_image_use_case),
    _service_info: dict = Depends(validate_api_key) # Đổi tên biến để chỉ ra rằng nó không được sử dụng trực tiếp
):
    """
    Endpoint kiểm duyệt hình ảnh, yêu cầu x-api-key hợp lệ trong header
    """
    result = use_case.execute(request.image_url)
    return {
        "status": "success",
        "data": result
    }