from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class LoginRequest(BaseModel):
    username: str = Field(..., example="admin")
    password: str = Field(..., example="admin123")

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    username: str
    full_name: Optional[str] = None

class TechnicianResponse(BaseModel):
    id: int
    username: str
    full_name: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class CampaignBase(BaseModel):
    target_index: int = Field(..., description="Target Index in the MindAR target.mind file (0-indexed)")
    campaign_name: str = Field(..., description="Historical campaign name")
    key_color: str = Field("#00ff00", description="Chroma-key color in hex format")
    chroma_threshold: float = Field(0.4, description="Threshold for chroma-key green screen shader")
    description: Optional[str] = Field(None, description="Detailed explanation of the military event")

class CampaignCreate(CampaignBase):
    pass

class CampaignUpdate(BaseModel):
    campaign_name: Optional[str] = None
    key_color: Optional[str] = None
    chroma_threshold: Optional[float] = None
    description: Optional[str] = None

class CampaignResponse(CampaignBase):
    id: int
    marker_image_url: Optional[str] = None
    video_overlay_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ProgressTrackRequest(BaseModel):
    visitor_session_id: str = Field(..., description="Unique persistent session ID of the visitor browser", example="uuid-12345-abcde")
    target_id: int = Field(..., description="Target ID of the scanned marker/map")

class VisitorLogResponse(BaseModel):
    id: int
    visitor_session_id: str
    campaign_id: int
    scanned_at: datetime

    class Config:
        from_attributes = True

class CampaignScanStat(BaseModel):
    campaign_id: int
    campaign_name: str
    scan_count: int

class AnalyticsSummary(BaseModel):
    total_campaigns: int
    total_scans: int
    total_unique_visitors: int
    campaign_popularity: List[CampaignScanStat]
    recent_scans: List[VisitorLogResponse]
