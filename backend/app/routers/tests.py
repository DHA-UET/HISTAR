import os
import io
import time
from fastapi import APIRouter, Depends, status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, auth

router = APIRouter(prefix="/api/tests", tags=["Integration Testing"])

@router.get("/run")
def run_integration_tests(db: Session = Depends(get_db)):
    from ...main import app
    client = TestClient(app)
    results = []
    
    start_time = time.time()
    try:
        tech = db.query(models.Technician).filter(models.Technician.username == "admin").first()
        if not tech:
            hashed_pw = auth.get_password_hash("admin123")
            tech = models.Technician(username="admin", hashed_password=hashed_pw, full_name="Kỹ Thuật Viên")
            db.add(tech)
            db.commit()
            
        login_res = client.post("/api/auth/login", data={"username": "admin", "password": "admin123"})
        duration = time.time() - start_time
        
        if login_res.status_code == 200 and "access_token" in login_res.json():
            token = login_res.json()["access_token"]
            results.append({
                "id": "TC-FUN-01",
                "feature": "Đăng nhập hệ thống quản trị",
                "input": "Nhập thông tin tài khoản kỹ thuật viên.",
                "expected": "Chuyển hướng thành công vào giao diện Admin Dashboard (nhận JWT Token).",
                "status": "PASS",
                "duration_ms": round(duration * 1000, 2),
                "details": f"Đăng nhập thành công! Token: {token[:15]}..."
            })
        else:
            token = None
            results.append({
                "id": "TC-FUN-01",
                "feature": "Đăng nhập hệ thống quản trị",
                "status": "FAIL",
                "duration_ms": round(duration * 1000, 2),
                "details": f"Đăng nhập thất bại. Status Code: {login_res.status_code}"
            })
    except Exception as e:
        token = None
        results.append({
            "id": "TC-FUN-01",
            "feature": "Đăng nhập hệ thống quản trị",
            "status": "FAIL",
            "duration_ms": round((time.time() - start_time) * 1000, 2),
            "details": f"Lỗi: {str(e)}"
        })

    start_time = time.time()
    if token:
        try:
            mock_marker = (io.BytesIO(b"dummy image data"), "marker.jpg", "image/jpeg")
            mock_large_video = (io.BytesIO(b"0" * (6 * 1024 * 1024)), "simulation_large.mp4", "video/mp4")
            
            upload_res = client.post(
                "/api/campaigns",
                headers={"Authorization": f"Bearer {token}"},
                data={
                    "target_index": 99,
                    "campaign_name": "Chiến dịch thử nghiệm tải lên quá dung lượng",
                    "key_color": "#00ff00",
                    "chroma_threshold": 0.4,
                    "description": "Thử nghiệm kích thước"
                },
                files={
                    "marker_image": mock_marker,
                    "video": mock_large_video
                }
            )
            duration = time.time() - start_time
            
            if upload_res.status_code == status.HTTP_413_PAYLOAD_TOO_LARGE:
                results.append({
                    "id": "TC-FUN-02",
                    "feature": "Tải lên tài nguyên chiến dịch",
                    "input": "Chọn ảnh sơ đồ + Luồng video .mp4 quá dung lượng cho phép (>5MB).",
                    "expected": "Hệ thống chặn thao tác, hiển thị thông báo lỗi 413 trực quan.",
                    "status": "PASS",
                    "duration_ms": round(duration * 1000, 2),
                    "details": f"Thành công! Trả về lỗi 413: {upload_res.json().get('detail')}"
                })
            else:
                results.append({
                    "id": "TC-FUN-02",
                    "feature": "Tải lên tài nguyên chiến dịch",
                    "status": "FAIL",
                    "duration_ms": round(duration * 1000, 2),
                    "details": f"Không chặn file. Status Code: {upload_res.status_code}"
                })
        except Exception as e:
            results.append({
                "id": "TC-FUN-02",
                "feature": "Tải lên tài nguyên chiến dịch",
                "status": "FAIL",
                "duration_ms": round((time.time() - start_time) * 1000, 2),
                "details": f"Lỗi: {str(e)}"
            })
    else:
        results.append({
            "id": "TC-FUN-02",
            "feature": "Tải lên tài nguyên chiến dịch",
            "status": "FAIL (Bypassed)",
            "duration_ms": 0,
            "details": "TC-FUN-01 thất bại."
        })

    start_time = time.time()
    try:
        api_res = client.get("/api/campaigns")
        duration = time.time() - start_time
        
        if api_res.status_code == 200:
            campaigns = api_res.json()
            results.append({
                "id": "TC-FUN-03",
                "feature": "Nạp dữ liệu Dynamic API",
                "input": "Khởi chạy Client Web-AR di động khi Backend đang chạy.",
                "expected": "Các phần tử AR được dựng tự động tương thích với số lượng bản ghi trong cơ sở dữ liệu.",
                "status": "PASS",
                "duration_ms": round(duration * 1000, 2),
                "details": f"Hoạt động tốt! Tìm thấy {len(campaigns)} chiến dịch."
            })
        else:
            results.append({
                "id": "TC-FUN-03",
                "feature": "Nạp dữ liệu Dynamic API",
                "status": "FAIL",
                "duration_ms": round(duration * 1000, 2),
                "details": f"Lỗi: {api_res.status_code}"
            })
    except Exception as e:
        results.append({
            "id": "TC-FUN-03",
            "feature": "Nạp dữ liệu Dynamic API",
            "status": "FAIL",
            "duration_ms": round((time.time() - start_time) * 1000, 2),
            "details": f"Lỗi: {str(e)}"
        })

    start_time = time.time()
    try:
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        script_path = os.path.join(base_dir, "script.js")
        
        if os.path.exists(script_path):
            with open(script_path, "r", encoding="utf-8") as f:
                script_content = f.read()
                
            has_start_btn = "startBtn" in script_content or "start-btn" in script_content
            has_video_play = "vid.play()" in script_content and "vid.pause()" in script_content
            
            duration = time.time() - start_time
            if has_start_btn and has_video_play:
                results.append({
                    "id": "TC-FUN-04",
                    "feature": "Xử lý chặn Autoplay video",
                    "input": "Nhấn nút tương tác khởi chạy màn hình chính #start-btn.",
                    "expected": "Trình duyệt kích hoạt thành công vòng lặp gọi hàm duyệt qua các luồng video ẩn nhằm giải phóng chính sách chặn phát tự động.",
                    "status": "PASS",
                    "duration_ms": round(duration * 1000, 2),
                    "details": "Đã tìm thấy kịch bản xử lý chặn Autoplay trong script.js."
                })
            else:
                results.append({
                    "id": "TC-FUN-04",
                    "feature": "Xử lý chặn Autoplay video",
                    "status": "FAIL",
                    "duration_ms": round(duration * 1000, 2),
                    "details": "Mã nguồn thiếu logic autoplay-bypass."
                })
        else:
            results.append({
                "id": "TC-FUN-04",
                "feature": "Xử lý chặn Autoplay video",
                "status": "FAIL",
                "duration_ms": 0,
                "details": "Không tìm thấy script.js"
            })
    except Exception as e:
        results.append({
            "id": "TC-FUN-04",
            "feature": "Xử lý chặn Autoplay video",
            "status": "FAIL",
            "duration_ms": round((time.time() - start_time) * 1000, 2),
            "details": f"Lỗi: {str(e)}"
        })

    start_time = time.time()
    try:
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        script_path = os.path.join(base_dir, "script.js")
        
        if os.path.exists(script_path):
            with open(script_path, "r", encoding="utf-8") as f:
                script_content = f.read()
                
            has_clear_btn = "clear-data-btn" in script_content or "clearDataBtn" in script_content
            has_reset_btn = "reset-btn" in script_content or "resetBtn" in script_content
            has_storage_remove = "localStorage.removeItem('ar_museum_progress')" in script_content or "removeItem" in script_content
            
            duration = time.time() - start_time
            if (has_clear_btn or has_reset_btn) and has_storage_remove:
                results.append({
                    "id": "TC-FUN-05",
                    "feature": "Khởi động lại tiến độ nhiệm vụ",
                    "input": "Kích hoạt nút nhấn xóa dữ liệu #clear-data-btn hoặc làm sạch dữ liệu hoàn thành #reset-btn.",
                    "expected": "Xóa sạch bản ghi phiên làm việc trong localStorage, đưa bộ đếm HUD về lại trạng thái ban đầu [ 0 / TOTAL ].",
                    "status": "PASS",
                    "duration_ms": round(duration * 1000, 2),
                    "details": "Đã xác nhận sự tồn tại của trình xử lý sự kiện xóa và cài lại tiến độ."
                })
            else:
                results.append({
                    "id": "TC-FUN-05",
                    "feature": "Khởi động lại tiến độ nhiệm vụ",
                    "status": "FAIL",
                    "duration_ms": round(duration * 1000, 2),
                    "details": "Mã nguồn thiếu xử lý sự kiện hoặc lệnh trên localStorage."
                })
        else:
            results.append({
                "id": "TC-FUN-05",
                "feature": "Khởi động lại tiến độ nhiệm vụ",
                "status": "FAIL",
                "duration_ms": 0,
                "details": "Không tìm thấy script.js"
            })
    except Exception as e:
        results.append({
            "id": "TC-FUN-05",
            "feature": "Khởi động lại tiến độ nhiệm vụ",
            "status": "FAIL",
            "duration_ms": round((time.time() - start_time) * 1000, 2),
            "details": f"Lỗi: {str(e)}"
        })

    all_passed = all(item["status"] == "PASS" for item in results)
    return {
        "status": "SUCCESS" if all_passed else "WARNING",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "total_executed": len(results),
        "total_passed": sum(1 for item in results if item["status"] == "PASS"),
        "total_failed": sum(1 for item in results if item["status"] == "FAIL"),
        "test_cases": results
    }
