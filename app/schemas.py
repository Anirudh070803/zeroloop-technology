from pydantic import BaseModel, ConfigDict
from typing import List, Optional, Any

# --- For Authentication ---
class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# --- For Scanning ---
class ScanTaskResponse(BaseModel):
    task_id: str
    status: str

class ScanResultPayload(BaseModel):
    scan_type: str
    data: Any

class VulnerabilityDetail(BaseModel):
    name: Optional[str] = None
    severity: Optional[str] = None
    description: Optional[str] = None
    simplified_explanation: Optional[str] = None

class HumanReadableReport(BaseModel):
    summary: str
    vulnerabilities: List[VulnerabilityDetail]