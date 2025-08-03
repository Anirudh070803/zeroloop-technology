# app/schemas.py
from pydantic import BaseModel
from typing import List, Optional, Any

class ScanTaskResponse(BaseModel):
    task_id: str
    status: str

class VulnerabilityDetail(BaseModel):
    name: str
    severity: str
    description: str
    simplified_explanation: Optional[str] = None

class HumanReadableReport(BaseModel):
    summary: str
    vulnerabilities: List[VulnerabilityDetail]

class ScanResultPayload(BaseModel):
    scan_type: str
    data: Any
    
class VulnerabilityDetail(BaseModel):
    name: str
    severity: str
    description: str
    simplified_explanation: Optional[str] = None
    confidence: Optional[str] = None # Add this line