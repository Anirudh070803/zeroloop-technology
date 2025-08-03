# app/schemas.py
from pydantic import BaseModel
from typing import List, Optional, Any 

class ScanRequest(BaseModel):
    contract_code: str

class ScanResponse(BaseModel):
    task_id: str
    status: str
    
class VulnerabilityDetail(BaseModel):
    name: str
    severity: str
    description: str
    
class HumanReadableReport(BaseModel):
    summary: str
    vulnerabilities: List[VulnerabilityDetail]
    
class ResultResponse(BaseModel):
    task_id: str
    status: str
    result: Optional[Any] = None