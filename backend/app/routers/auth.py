from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas, auth

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

@router.post("/login", response_model=schemas.TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    tech = db.query(models.Technician).filter(models.Technician.username == form_data.username).first()
    
    if not tech and form_data.username == "admin":
        hashed_pw = auth.get_password_hash("admin123")
        tech = models.Technician(
            username="admin",
            hashed_password=hashed_pw,
            full_name="Kỹ Thuật Viên Bảo Tàng"
        )
        db.add(tech)
        db.commit()
        db.refresh(tech)
        
    if not tech or not auth.verify_password(form_data.password, tech.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Tên đăng nhập hoặc mật khẩu không chính xác",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": tech.username}, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "username": tech.username,
        "full_name": tech.full_name
    }

@router.get("/me", response_model=schemas.TechnicianResponse)
def get_me(current_user: models.Technician = Depends(auth.get_current_technician)):
    return current_user
