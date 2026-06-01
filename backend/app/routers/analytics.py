from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from ..database import get_db
from .. import models, schemas, auth

router = APIRouter(prefix="/api/analytics", tags=["Analytics"])

@router.post("/track", response_model=schemas.VisitorLogResponse, status_code=status.HTTP_201_CREATED)
def track_visitor_progress(payload: schemas.ProgressTrackRequest, db: Session = Depends(get_db)):
    campaign = db.query(models.Campaign).filter(models.Campaign.target_index == payload.target_id).first()
    if not campaign:
        raise HTTPException(
            status_code=404, 
            detail=f"Mã Marker (target_index={payload.target_id}) không khớp với bất kỳ chiến dịch nào"
        )
        
    existing_log = db.query(models.VisitorLog).filter(
        models.VisitorLog.visitor_session_id == payload.visitor_session_id,
        models.VisitorLog.campaign_id == campaign.id
    ).first()
    
    if existing_log:
        return existing_log
        
    new_log = models.VisitorLog(
        visitor_session_id=payload.visitor_session_id,
        campaign_id=campaign.id
    )
    db.add(new_log)
    db.commit()
    db.refresh(new_log)
    return new_log

@router.get("", response_model=schemas.AnalyticsSummary)
def get_analytics_summary(
    db: Session = Depends(get_db), 
    current_tech: models.Technician = Depends(auth.get_current_technician)
):
    total_campaigns = db.query(models.Campaign).count()
    total_scans = db.query(models.VisitorLog).count()
    total_unique_visitors = db.query(models.VisitorLog.visitor_session_id).distinct().count()
    
    popularity_query = db.query(
        models.Campaign.id,
        models.Campaign.campaign_name,
        func.count(models.VisitorLog.id).label("scan_count")
    ).outerjoin(
        models.VisitorLog, models.Campaign.id == models.VisitorLog.campaign_id
    ).group_by(
        models.Campaign.id
    ).order_by(
        func.count(models.VisitorLog.id).desc()
    ).all()
    
    campaign_popularity = [
        schemas.CampaignScanStat(
            campaign_id=row.id,
            campaign_name=row.campaign_name,
            scan_count=row.scan_count
        ) for row in popularity_query
    ]
    
    recent_scans = db.query(models.VisitorLog).order_by(
        models.VisitorLog.scanned_at.desc()
    ).limit(20).all()
    
    return schemas.AnalyticsSummary(
        total_campaigns=total_campaigns,
        total_scans=total_scans,
        total_unique_visitors=total_unique_visitors,
        campaign_popularity=campaign_popularity,
        recent_scans=recent_scans
    )
