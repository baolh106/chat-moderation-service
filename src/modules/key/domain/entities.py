from pydantic import BaseModel
from typing import Optional

class ServiceKey(BaseModel):
    service_name: str
    key: str
    is_active: bool
    description: Optional[str] = None