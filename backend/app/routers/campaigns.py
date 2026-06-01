import os
import shutil
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas, auth

router = APIRouter(prefix="/api/campaigns", tags=["Campaigns"])

UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "static", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

def save_uploaded_file(upload_file: UploadFile, subfolder: str) -> str:
    folder = os.path.join(UPLOAD_DIR, subfolder)
    os.makedirs(folder, exist_ok=True)
    
    safe_filename = os.path.basename(upload_file.filename).replace(" ", "_")
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"{timestamp}_{safe_filename}"
    
    file_path = os.path.join(folder, filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)
        
    return f"/static/uploads/{subfolder}/{filename}"

def delete_local_file(relative_url: str):
    if not relative_url:
        return
    relative_path = relative_url.lstrip("/")
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    local_path = os.path.join(base_dir, relative_path)
    
    if os.path.exists(local_path) and os.path.isfile(local_path):
        try:
            os.remove(local_path)
        except Exception as e:
            print(f"Error removing file {local_path}: {e}")

def validate_file_size(upload_file: UploadFile, max_size: int = 5 * 1024 * 1024):
    if not upload_file:
        return
    upload_file.file.seek(0, 2)
    size = upload_file.file.tell()
    upload_file.file.seek(0)
    
    if size > max_size:
        raise HTTPException(
            status_code=status.HTTP_413_PAYLOAD_TOO_LARGE,
            detail=f"Tệp tin '{upload_file.filename}' vượt quá dung lượng cho phép ({max_size // (1024 * 1024)}MB)"
        )

@router.get("", response_model=List[schemas.CampaignResponse])
def get_campaigns(db: Session = Depends(get_db)):
    return db.query(models.Campaign).order_by(models.Campaign.target_index.asc()).all()

@router.get("/{id}", response_model=schemas.CampaignResponse)
def get_campaign(id: int, db: Session = Depends(get_db)):
    campaign = db.query(models.Campaign).filter(models.Campaign.id == id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Chiến dịch không tồn tại")
    return campaign

@router.post("", response_model=schemas.CampaignResponse, status_code=status.HTTP_201_CREATED)
def create_campaign(
    target_index: int = Form(...),
    campaign_name: str = Form(...),
    key_color: str = Form("#00ff00"),
    chroma_threshold: float = Form(0.4),
    description: str = Form(""),
    marker_image: UploadFile = File(...),
    video: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_tech: models.Technician = Depends(auth.get_current_technician)
):
    existing_idx = db.query(models.Campaign).filter(models.Campaign.target_index == target_index).first()
    if existing_idx:
        raise HTTPException(status_code=400, detail="Target Index đã được gán cho một chiến dịch khác")

    validate_file_size(marker_image)
    validate_file_size(video)
    
    marker_url = save_uploaded_file(marker_image, "markers")
    video_overlay_url = save_uploaded_file(video, "videos")

    db_campaign = models.Campaign(
        target_index=target_index,
        campaign_name=campaign_name,
        key_color=key_color,
        chroma_threshold=chroma_threshold,
        description=description,
        marker_image_url=marker_url,
        video_overlay_url=video_overlay_url
    )
    
    db.add(db_campaign)
    db.commit()
    db.refresh(db_campaign)
    return db_campaign

@router.put("/{id}", response_model=schemas.CampaignResponse)
def update_campaign(
    id: int,
    campaign_name: Optional[str] = Form(None),
    key_color: Optional[str] = Form(None),
    chroma_threshold: Optional[float] = Form(None),
    description: Optional[str] = Form(None),
    marker_image: Optional[UploadFile] = File(None),
    video: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_tech: models.Technician = Depends(auth.get_current_technician)
):
    campaign = db.query(models.Campaign).filter(models.Campaign.id == id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Chiến dịch không tồn tại")

    if campaign_name is not None:
        campaign.campaign_name = campaign_name
    if key_color is not None:
        campaign.key_color = key_color
    if chroma_threshold is not None:
        campaign.chroma_threshold = chroma_threshold
    if description is not None:
        campaign.description = description

    if marker_image is not None:
        validate_file_size(marker_image)
        delete_local_file(campaign.marker_image_url)
        campaign.marker_image_url = save_uploaded_file(marker_image, "markers")

    if video is not None:
        validate_file_size(video)
        delete_local_file(campaign.video_overlay_url)
        campaign.video_overlay_url = save_uploaded_file(video, "videos")

    db.commit()
    db.refresh(campaign)
    return campaign

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_campaign(
    id: int,
    db: Session = Depends(get_db),
    current_tech: models.Technician = Depends(auth.get_current_technician)
):
    campaign = db.query(models.Campaign).filter(models.Campaign.id == id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Chiến dịch không tồn tại")

    delete_local_file(campaign.marker_image_url)
    delete_local_file(campaign.video_overlay_url)

    db.delete(campaign)
    db.commit()
    return None
