from pydantic import BaseModel
from typing import List, Dict, Any, Optional


class HealthResponse(BaseModel):
    status: str


class LoadRequest(BaseModel):
    csv_path: str


class MessageResponse(BaseModel):
    message: str


class PreviewResponse(BaseModel):
    rows: int
    columns: List[str]
    preview: List[Dict[str, Any]]


class StatsResponse(BaseModel):
    stats: List[Dict[str, Any]] 


class ReportResponse(BaseModel):
    pdf_path: str
