import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

from .app.database import engine, Base, SessionLocal
from .app import models, auth
from .app.routers import auth as auth_router, campaigns, analytics, dashboard, tests

Base.metadata.create_all(bind=engine)

db = SessionLocal()
try:
    default_tech = db.query(models.Technician).filter(models.Technician.username == "admin").first()
    if not default_tech:
        hashed_pw = auth.get_password_hash("admin123")
        tech = models.Technician(
            username="admin",
            hashed_password=hashed_pw,
            full_name="Kỹ Thuật Viên Bảo Tàng"
        )
        db.add(tech)
        db.commit()
finally:
    db.close()

app = FastAPI(
    title="HISTAR - REST API",
    description="REST API for Web-AR experience and Admin Dashboard",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
os.makedirs(os.path.join(STATIC_DIR, "uploads", "markers"), exist_ok=True)
os.makedirs(os.path.join(STATIC_DIR, "uploads", "videos"), exist_ok=True)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

app.include_router(auth_router.router)
app.include_router(campaigns.router)
app.include_router(analytics.router)
app.include_router(dashboard.router)
app.include_router(tests.router)

@app.get("/")
def redirect_to_admin():
    return RedirectResponse(url="/admin")
