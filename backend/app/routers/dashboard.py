from fastapi import APIRouter, status
from fastapi.responses import HTMLResponse

router = APIRouter(tags=["Admin Dashboard"])

@router.get("/admin", response_class=HTMLResponse)
def get_admin_dashboard():
    """
    Serves the premium, self-contained HISTAR Admin Dashboard interface.
    Includes built-in HTML/CSS/JS with full interactive client capabilities
    to manage campaigns, upload assets, and inspect museum visitor statistics.
    """
    html_content = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HISTAR Admin - Quản lý Tài nguyên Số</title>
    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet">
    <!-- FontAwesome Icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <style>
        :root {
            --bg-primary: #0a0e17;
            --bg-secondary: rgba(18, 26, 44, 0.6);
            --bg-glass: rgba(18, 26, 44, 0.45);
            --border-glass: rgba(255, 255, 255, 0.08);
            
            --color-gold: #ffbd59;
            --color-gold-glow: rgba(255, 189, 89, 0.3);
            --color-crimson: #ff4d4d;
            --color-crimson-glow: rgba(255, 77, 77, 0.3);
            --color-cyan: #00f2fe;
            --color-cyan-glow: rgba(0, 242, 254, 0.3);
            
            --text-main: #f3f4f6;
            --text-muted: #9ca3af;
            --text-dark: #1f2937;
            
            --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Outfit', sans-serif;
        }

        body {
            background-color: var(--bg-primary);
            color: var(--text-main);
            min-height: 100vh;
            overflow-x: hidden;
            background-image: 
                radial-gradient(circle at 10% 20%, rgba(255, 189, 89, 0.05) 0%, transparent 40%),
                radial-gradient(circle at 90% 80%, rgba(0, 242, 254, 0.05) 0%, transparent 40%);
            background-attachment: fixed;
        }

        /* Scrollbar styling */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        ::-webkit-scrollbar-track {
            background: var(--bg-primary);
        }
        ::-webkit-scrollbar-thumb {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: var(--color-gold);
        }

        /* Glassmorphism utility */
        .glass-card {
            background: var(--bg-glass);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid var(--border-glass);
            border-radius: 16px;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        }

        /* LOGIN SCREEN */
        #login-screen {
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            padding: 20px;
        }

        .login-box {
            width: 100%;
            max-width: 450px;
            padding: 40px;
            text-align: center;
            position: relative;
            overflow: hidden;
        }

        .login-box::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 4px;
            background: linear-gradient(90deg, var(--color-gold), var(--color-cyan));
        }

        .logo-title {
            font-family: 'Space Grotesk', sans-serif;
            font-size: 2.2rem;
            font-weight: 700;
            background: linear-gradient(135deg, var(--color-gold) 30%, #ffffff 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 8px;
            letter-spacing: 2px;
        }

        .logo-subtitle {
            color: var(--text-muted);
            font-size: 0.95rem;
            margin-bottom: 35px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .input-group {
            margin-bottom: 24px;
            text-align: left;
            position: relative;
        }

        .input-group label {
            display: block;
            font-size: 0.85rem;
            font-weight: 500;
            color: var(--text-muted);
            margin-bottom: 8px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .input-group i {
            position: absolute;
            bottom: 14px;
            left: 16px;
            color: var(--text-muted);
            font-size: 1.1rem;
        }

        .input-field {
            width: 100%;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid var(--border-glass);
            border-radius: 8px;
            padding: 12px 16px 12px 45px;
            color: #ffffff;
            font-size: 1rem;
            outline: none;
            transition: var(--transition);
        }

        .input-field:focus {
            border-color: var(--color-gold);
            box-shadow: 0 0 10px var(--color-gold-glow);
            background: rgba(255, 255, 255, 0.08);
        }

        .btn {
            width: 100%;
            padding: 14px;
            border: none;
            border-radius: 8px;
            font-weight: 600;
            font-size: 1rem;
            cursor: pointer;
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 10px;
            transition: var(--transition);
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .btn-primary {
            background: linear-gradient(135deg, var(--color-gold), #e09f2d);
            color: var(--text-dark);
            box-shadow: 0 4px 15px var(--color-gold-glow);
        }

        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(255, 189, 89, 0.5);
        }

        .btn-danger {
            background: linear-gradient(135deg, var(--color-crimson), #c0392b);
            color: white;
            box-shadow: 0 4px 15px var(--color-crimson-glow);
        }

        .btn-danger:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(255, 77, 77, 0.5);
        }

        .login-error {
            color: var(--color-crimson);
            font-size: 0.9rem;
            margin-top: 15px;
            display: none;
        }


        /* DASHBOARD LAYOUT */
        #dashboard-screen {
            display: none;
            flex-direction: column;
            min-height: 100vh;
        }

        /* HEADER */
        header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 20px 40px;
            border-bottom: 1px solid var(--border-glass);
            background: rgba(10, 14, 23, 0.8);
            backdrop-filter: blur(10px);
            position: sticky;
            top: 0;
            z-index: 100;
        }

        .header-logo {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .header-logo i {
            font-size: 1.8rem;
            color: var(--color-gold);
            text-shadow: 0 0 10px var(--color-gold-glow);
        }

        .header-logo h1 {
            font-family: 'Space Grotesk', sans-serif;
            font-size: 1.5rem;
            font-weight: 700;
            letter-spacing: 1px;
        }

        .header-user {
            display: flex;
            align-items: center;
            gap: 20px;
        }

        .user-info {
            text-align: right;
        }

        .user-name {
            font-weight: 600;
            font-size: 0.95rem;
        }

        .user-role {
            font-size: 0.8rem;
            color: var(--color-gold);
        }

        .logout-btn {
            background: transparent;
            border: 1px solid var(--border-glass);
            padding: 8px 16px;
            border-radius: 8px;
            color: var(--text-main);
            font-weight: 500;
            cursor: pointer;
            transition: var(--transition);
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .logout-btn:hover {
            background: var(--color-crimson);
            border-color: var(--color-crimson);
            box-shadow: 0 0 10px var(--color-crimson-glow);
            transform: translateY(-1px);
        }

        /* MAIN CONTAINER */
        .dashboard-container {
            display: grid;
            grid-template-columns: 260px 1fr;
            flex-grow: 1;
        }

        /* SIDEBAR */
        aside {
            border-right: 1px solid var(--border-glass);
            padding: 30px 20px;
            background: rgba(10, 14, 23, 0.3);
        }

        .menu-list {
            list-style: none;
            display: flex;
            flex-direction: column;
            gap: 8px;
        }

        .menu-item {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 14px 18px;
            border-radius: 10px;
            color: var(--text-muted);
            cursor: pointer;
            font-weight: 500;
            transition: var(--transition);
        }

        .menu-item:hover, .menu-item.active {
            color: #ffffff;
            background: rgba(255, 255, 255, 0.05);
        }

        .menu-item.active {
            border-left: 4px solid var(--color-gold);
            background: rgba(255, 189, 89, 0.08);
            color: var(--color-gold);
        }

        .menu-item i {
            font-size: 1.15rem;
            width: 20px;
        }

        /* MAIN CONTENT VIEWS */
        main {
            padding: 40px;
            overflow-y: auto;
        }

        .view-section {
            display: none;
            animation: fadeIn 0.4s ease;
        }

        .view-section.active {
            display: block;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .view-header {
            margin-bottom: 35px;
        }

        .view-title {
            font-family: 'Space Grotesk', sans-serif;
            font-size: 1.8rem;
            font-weight: 700;
            margin-bottom: 6px;
        }

        .view-desc {
            color: var(--text-muted);
            font-size: 0.95rem;
        }

        /* ANALYTICS CARDS */
        .analytics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 25px;
            margin-bottom: 40px;
        }

        .stat-card {
            padding: 24px;
            position: relative;
            overflow: hidden;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .stat-card::after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 0;
            width: 100%;
            height: 3px;
            background: var(--card-color, var(--color-gold));
        }

        .stat-info h3 {
            font-size: 0.9rem;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 8px;
        }

        .stat-val {
            font-size: 2.2rem;
            font-weight: 700;
            font-family: 'Space Grotesk', sans-serif;
            color: #ffffff;
        }

        .stat-icon {
            font-size: 2.5rem;
            color: var(--card-color, var(--color-gold));
            opacity: 0.8;
            text-shadow: 0 0 15px var(--card-glow, var(--color-gold-glow));
        }

        /* ANALYTICS SECTION LOWER */
        .analytics-charts {
            display: grid;
            grid-template-columns: 1.5fr 1fr;
            gap: 30px;
        }

        .analytics-box {
            padding: 30px;
            min-height: 400px;
        }

        .box-title {
            font-family: 'Space Grotesk', sans-serif;
            font-size: 1.2rem;
            font-weight: 600;
            margin-bottom: 25px;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .box-title i {
            color: var(--color-gold);
        }

        /* CAMPAIGNS TABLE */
        .table-responsive {
            width: 100%;
            overflow-x: auto;
            border-radius: 12px;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            text-align: left;
        }

        th {
            background: rgba(255, 255, 255, 0.03);
            padding: 16px 20px;
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            color: var(--text-muted);
            border-bottom: 1px solid var(--border-glass);
            font-weight: 600;
        }

        td {
            padding: 18px 20px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.04);
            font-size: 0.95rem;
            vertical-align: middle;
        }

        tr:last-child td {
            border-bottom: none;
        }

        tr:hover td {
            background: rgba(255, 255, 255, 0.01);
        }

        .campaign-meta {
            display: flex;
            align-items: center;
            gap: 15px;
        }

        .campaign-thumb {
            width: 50px;
            height: 50px;
            border-radius: 8px;
            object-fit: cover;
            border: 1px solid var(--border-glass);
            background: #111;
        }

        .campaign-name {
            font-weight: 600;
            color: #ffffff;
            margin-bottom: 4px;
        }

        .campaign-desc {
            font-size: 0.8rem;
            color: var(--text-muted);
            max-width: 250px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        .badge {
            display: inline-block;
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 0.75rem;
            font-weight: 600;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid var(--border-glass);
        }

        .badge-gold {
            background: rgba(255, 189, 89, 0.1);
            color: var(--color-gold);
            border-color: rgba(255, 189, 89, 0.2);
        }

        .badge-cyan {
            background: rgba(0, 242, 254, 0.1);
            color: var(--color-cyan);
            border-color: rgba(0, 242, 254, 0.2);
        }

        .action-btns {
            display: flex;
            gap: 8px;
        }

        .icon-btn {
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid var(--border-glass);
            color: var(--text-main);
            width: 36px;
            height: 36px;
            border-radius: 8px;
            display: flex;
            justify-content: center;
            align-items: center;
            cursor: pointer;
            transition: var(--transition);
        }

        .icon-btn:hover {
            background: rgba(255, 255, 255, 0.1);
        }

        .icon-btn.delete:hover {
            background: var(--color-crimson);
            border-color: var(--color-crimson);
            color: white;
            box-shadow: 0 0 10px var(--color-crimson-glow);
        }

        /* LIVE FEED */
        .live-feed-list {
            list-style: none;
            display: flex;
            flex-direction: column;
            gap: 15px;
            max-height: 450px;
            overflow-y: auto;
            padding-right: 5px;
        }

        .feed-item {
            display: flex;
            align-items: flex-start;
            gap: 12px;
            padding: 12px 15px;
            border-radius: 8px;
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid rgba(255, 255, 255, 0.03);
            animation: slideIn 0.3s ease;
        }

        @keyframes slideIn {
            from { opacity: 0; transform: translateX(10px); }
            to { opacity: 1; transform: translateX(0); }
        }

        .feed-icon {
            background: rgba(0, 242, 254, 0.1);
            color: var(--color-cyan);
            width: 32px;
            height: 32px;
            border-radius: 50%;
            display: flex;
            justify-content: center;
            align-items: center;
            font-size: 0.9rem;
            flex-shrink: 0;
            box-shadow: 0 0 8px var(--color-cyan-glow);
        }

        .feed-content {
            font-size: 0.85rem;
            flex-grow: 1;
        }

        .feed-text {
            color: #ffffff;
            margin-bottom: 4px;
        }

        .feed-text strong {
            color: var(--color-gold);
        }

        .feed-time {
            font-size: 0.75rem;
            color: var(--text-muted);
            display: flex;
            align-items: center;
            gap: 4px;
        }

        /* POPULARITY STATS */
        .popularity-list {
            display: flex;
            flex-direction: column;
            gap: 20px;
        }

        .pop-item {
            display: flex;
            flex-direction: column;
            gap: 8px;
        }

        .pop-meta {
            display: flex;
            justify-content: space-between;
            font-size: 0.9rem;
        }

        .pop-name {
            font-weight: 600;
        }

        .pop-scans {
            color: var(--color-cyan);
            font-weight: bold;
        }

        .pop-bar-bg {
            height: 6px;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 3px;
            overflow: hidden;
            width: 100%;
        }

        .pop-bar-fill {
            height: 100%;
            background: linear-gradient(90deg, var(--color-gold), var(--color-cyan));
            border-radius: 3px;
            width: 0%;
            transition: width 1s cubic-bezier(0.4, 0, 0.2, 1);
        }

        /* UPLOAD WIZARD FORM */
        .form-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
            margin-bottom: 30px;
        }

        .form-column {
            display: flex;
            flex-direction: column;
            gap: 24px;
        }

        .form-group {
            display: flex;
            flex-direction: column;
            gap: 8px;
        }

        .form-group label {
            font-size: 0.85rem;
            font-weight: 600;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .form-group select, .form-group input, .form-group textarea {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid var(--border-glass);
            border-radius: 8px;
            padding: 12px 16px;
            color: #ffffff;
            font-size: 0.95rem;
            outline: none;
            transition: var(--transition);
        }

        .form-group select:focus, .form-group input:focus, .form-group textarea:focus {
            border-color: var(--color-gold);
            box-shadow: 0 0 10px var(--color-gold-glow);
            background: rgba(255, 255, 255, 0.06);
        }

        .color-input-container {
            display: flex;
            align-items: center;
            gap: 15px;
        }

        .color-picker {
            width: 50px;
            height: 46px;
            padding: 0;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            background: transparent;
        }

        .color-hex {
            flex-grow: 1;
        }

        /* UPLOAD BOXES */
        .upload-drag-area {
            border: 2px dashed rgba(255, 255, 255, 0.15);
            border-radius: 12px;
            padding: 35px 20px;
            text-align: center;
            cursor: pointer;
            transition: var(--transition);
            background: rgba(255, 255, 255, 0.01);
            position: relative;
        }

        .upload-drag-area:hover {
            border-color: var(--color-gold);
            background: rgba(255, 189, 89, 0.02);
        }

        .upload-drag-area i {
            font-size: 2.2rem;
            color: var(--text-muted);
            margin-bottom: 12px;
            transition: var(--transition);
        }

        .upload-drag-area:hover i {
            color: var(--color-gold);
            transform: translateY(-3px);
        }

        .upload-text {
            font-size: 0.95rem;
            font-weight: 500;
            margin-bottom: 4px;
        }

        .upload-subtext {
            font-size: 0.75rem;
            color: var(--text-muted);
        }

        .upload-input {
            display: none;
        }

        .file-preview {
            margin-top: 10px;
            font-size: 0.8rem;
            color: var(--color-cyan);
            font-weight: 600;
            display: none;
        }

        /* TOAST ALERT */
        .toast {
            position: fixed;
            bottom: 30px;
            right: -400px;
            padding: 16px 24px;
            display: flex;
            align-items: center;
            gap: 12px;
            z-index: 1000;
            transition: right 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }

        .toast.show {
            right: 30px;
        }

        .toast-success {
            border-left: 4px solid var(--color-cyan);
            box-shadow: 0 5px 15px rgba(0, 242, 254, 0.2);
        }

        .toast-error {
            border-left: 4px solid var(--color-crimson);
            box-shadow: 0 5px 15px rgba(255, 77, 77, 0.2);
        }

        .toast-icon {
            font-size: 1.2rem;
        }

        .toast-success .toast-icon { color: var(--color-cyan); }
        .toast-error .toast-icon { color: var(--color-crimson); }
        
    </style>
</head>
<body>

    <!-- TOAST NOTIFICATION -->
    <div id="toast-notification" class="glass-card toast">
        <i id="toast-icon" class="fa-solid fa-circle-check toast-icon"></i>
        <span id="toast-text">Thông báo mặc định</span>
    </div>

    <!-- 1. LOGIN SCREEN -->
    <div id="login-screen">
        <div class="glass-card login-box">
            <div class="logo-title">HISTAR</div>
            <div class="logo-subtitle">Quản trị Bảo tàng AR</div>
            
            <form id="login-form">
                <div class="input-group">
                    <label for="username">Tài khoản</label>
                    <i class="fa-solid fa-user"></i>
                    <input type="text" id="username" class="input-field" placeholder="Nhập tên đăng nhập" required>
                </div>
                
                <div class="input-group">
                    <label for="password">Mật khẩu</label>
                    <i class="fa-solid fa-lock"></i>
                    <input type="password" id="password" class="input-field" placeholder="Nhập mật khẩu" required>
                </div>
                
                <button type="submit" class="btn btn-primary">
                    <i class="fa-solid fa-right-to-bracket"></i> Đăng nhập hệ thống
                </button>
            </form>
            
            <div id="login-error-msg" class="login-error">Tên đăng nhập hoặc mật khẩu không đúng.</div>
        </div>
    </div>

    <!-- 2. MAIN DASHBOARD SCREEN -->
    <div id="dashboard-screen">
        <header>
            <div class="header-logo">
                <i class="fa-solid fa-clock-rotate-left"></i>
                <div>
                    <h1>HISTAR</h1>
                    <div style="font-size: 0.75rem; color: var(--text-muted); text-transform: uppercase;">Phân hệ kỹ thuật viên</div>
                </div>
            </div>
            
            <div class="header-user">
                <div class="user-info">
                    <div id="display-user-name" class="user-name">Đang tải...</div>
                    <div class="user-role"><i class="fa-solid fa-user-shield"></i> Administrator</div>
                </div>
                <button id="logout-btn" class="logout-btn">
                    <i class="fa-solid fa-power-off"></i> Đăng xuất
                </button>
            </div>
        </header>

        <div class="dashboard-container">
            <!-- SIDEBAR -->
            <aside>
                <ul class="menu-list">
                    <li class="menu-item active" data-view="view-analytics">
                        <i class="fa-solid fa-chart-line"></i> Bảng điều khiển
                    </li>
                    <li class="menu-item" data-view="view-campaigns">
                        <i class="fa-solid fa-map-location-dot"></i> Danh sách chiến dịch
                    </li>
                    <li class="menu-item" data-view="view-wizard">
                        <i class="fa-solid fa-circle-plus"></i> Thêm tài nguyên AR
                    </li>
                </ul>
            </aside>

            <!-- MAIN WORKSPACE -->
            <main>
                
                <!-- VIEW A: ANALYTICS -->
                <section id="view-analytics" class="view-section active">
                    <div class="view-header">
                        <h2 class="view-title">Bảng Điều Khiển Tổng Quan</h2>
                        <p class="view-desc">Giám sát lượng khách tham quan, tiến độ thu thập và các chiến dịch số hóa.</p>
                    </div>

                    <!-- Cards -->
                    <div class="analytics-grid">
                        <div class="glass-card stat-card" style="--card-color: var(--color-gold); --card-glow: var(--color-gold-glow)">
                            <div class="stat-info">
                                <h3>Tổng chiến dịch</h3>
                                <div id="stat-total-campaigns" class="stat-val">0</div>
                            </div>
                            <i class="fa-solid fa-map-location-dot stat-icon"></i>
                        </div>
                        
                        <div class="glass-card stat-card" style="--card-color: var(--color-cyan); --card-glow: var(--color-cyan-glow)">
                            <div class="stat-info">
                                <h3>Lượt quét thành công</h3>
                                <div id="stat-total-scans" class="stat-val">0</div>
                            </div>
                            <i class="fa-solid fa-qrcode stat-icon"></i>
                        </div>
                        
                        <div class="glass-card stat-card" style="--card-color: #a855f7; --card-glow: rgba(168, 85, 247, 0.3)">
                            <div class="stat-info">
                                <h3>Khách tham quan (Unique)</h3>
                                <div id="stat-total-visitors" class="stat-val">0</div>
                            </div>
                            <i class="fa-solid fa-users stat-icon"></i>
                        </div>
                    </div>

                    <!-- Sub Sections -->
                    <div class="analytics-charts">
                        <!-- Activity Feed -->
                        <div class="glass-card analytics-box">
                            <h3 class="box-title"><i class="fa-solid fa-satellite-dish"></i> Hoạt động quét theo thời gian thực</h3>
                            <ul id="live-scanned-feed" class="live-feed-list">
                                <!-- Dynamic dynamic visitor logs -->
                                <li class="feed-item" style="border:none; background:transparent; justify-content:center;">
                                    <span style="color:var(--text-muted);">Đang tải dữ liệu hoạt động...</span>
                                </li>
                            </ul>
                        </div>
                        
                        <!-- Popularity ranking -->
                        <div class="glass-card analytics-box">
                            <h3 class="box-title"><i class="fa-solid fa-fire"></i> Mức độ tương tác của chiến dịch</h3>
                            <div id="campaign-popularity-ranking" class="popularity-list">
                                <!-- Dynamic popularity list -->
                                <span style="color:var(--text-muted); text-align:center; display:block;">Đang phân tích mức độ tương tác...</span>
                            </div>
                        </div>
                    </div>
                </section>


                <!-- VIEW B: CAMPAIGNS LIST -->
                <section id="view-campaigns" class="view-section">
                    <div class="view-header">
                        <h2 class="view-title">Quản Lý Danh Sách Chiến Dịch</h2>
                        <p class="view-desc">Xem, chỉnh sửa hoặc gỡ bỏ các chiến dịch AR và tệp tin hình ảnh/video mô phỏng.</p>
                    </div>

                    <div class="glass-card analytics-box" style="min-height: auto; padding: 20px;">
                        <div class="table-responsive">
                            <table>
                                <thead>
                                    <tr>
                                        <th>Chiến dịch / Bản đồ</th>
                                        <th>Mã TargetIndex</th>
                                        <th>Mã TargetID (Client)</th>
                                        <th>Chroma-Key Color</th>
                                        <th>Ngưỡng Lọc</th>
                                        <th>Hành động</th>
                                    </tr>
                                </thead>
                                <tbody id="campaign-table-body">
                                    <tr>
                                        <td colspan="6" style="text-align:center; color: var(--text-muted); padding: 30px;">
                                            Chưa có chiến dịch nào được tạo.
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </section>


                <!-- VIEW C: WIZARD UPLOAD FORM -->
                <section id="view-wizard" class="view-section">
                    <div class="view-header">
                        <h2 class="view-title">Tải Lên Tài Nguyên Số Hóa</h2>
                        <p class="view-desc">Khởi tạo chiến dịch mới: tải ảnh Marker (MindAR) và Video mô phỏng tương ứng.</p>
                    </div>

                    <div class="glass-card analytics-box" style="min-height: auto;">
                        <form id="wizard-upload-form" enctype="multipart/form-data">
                            <div class="form-grid">
                                
                                <!-- Left Column: Texts -->
                                <div class="form-column">
                                    <div class="form-group">
                                        <label for="campaign-name-input">Tên Chiến Dịch Quân Sự</label>
                                        <input type="text" id="campaign-name-input" placeholder="Ví dụ: Chiến dịch Điện Biên Phủ (1954)" required>
                                    </div>
                                    
                                    <div class="form-grid" style="grid-template-columns:1fr 1fr; margin-bottom:0; gap:15px;">
                                        <div class="form-group">
                                            <label for="target-index-input">Target Index (.mind)</label>
                                            <input type="number" id="target-index-input" min="0" max="99" placeholder="Ví dụ: 0" required>
                                        </div>
                                        <div class="form-group">
                                            <label for="target-id-input">Target ID (A-Frame)</label>
                                            <input type="number" id="target-id-input" min="0" max="99" placeholder="Ví dụ: 0" required>
                                        </div>
                                    </div>
                                    
                                    <div class="form-grid" style="grid-template-columns:1.5fr 1fr; margin-bottom:0; gap:15px;">
                                        <div class="form-group">
                                            <label for="key-color-hex">Chroma-key Color</label>
                                            <div class="color-input-container">
                                                <input type="color" id="key-color-picker" class="color-picker" value="#00ff00">
                                                <input type="text" id="key-color-hex" class="color-hex" value="#00ff00" placeholder="#00ff00" required>
                                            </div>
                                        </div>
                                        <div class="form-group">
                                            <label for="threshold-input">Chroma Threshold</label>
                                            <input type="number" id="threshold-input" step="0.05" min="0.1" max="0.9" value="0.4" required>
                                        </div>
                                    </div>

                                    <div class="form-group">
                                        <label for="description-input">Mô tả lịch sử</label>
                                        <textarea id="description-input" rows="4" placeholder="Nhập tóm tắt lịch sử hào hùng của chiến dịch..."></textarea>
                                    </div>
                                </div>
                                
                                <!-- Right Column: Files upload -->
                                <div class="form-column">
                                    <div class="form-group">
                                        <label>1. Bản đồ Marker (Hình ảnh)</label>
                                        <div class="upload-drag-area" onclick="document.getElementById('marker-file-input').click()">
                                            <i class="fa-solid fa-file-image"></i>
                                            <div class="upload-text">Kéo thả hoặc Nhấp để chọn ảnh bản đồ</div>
                                            <div class="upload-subtext">Hỗ trợ định dạng PNG, JPG, JPEG (Kích thước dưới 5MB)</div>
                                            <input type="file" id="marker-file-input" class="upload-input" accept="image/*" required>
                                            <div id="marker-preview-name" class="file-preview"></div>
                                        </div>
                                    </div>
                                    
                                    <div class="form-group">
                                        <label>2. Video Mô phỏng (Green Screen)</label>
                                        <div class="upload-drag-area" onclick="document.getElementById('video-file-input').click()">
                                            <i class="fa-solid fa-file-video"></i>
                                            <div class="upload-text">Kéo thả hoặc Nhấp để chọn video mô phỏng</div>
                                            <div class="upload-subtext">Hỗ trợ định dạng MP4, WEBM (Chroma-key video nền xanh)</div>
                                            <input type="file" id="video-file-input" class="upload-input" accept="video/*" required>
                                            <div id="video-preview-name" class="file-preview"></div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            
                            <div style="display:flex; justify-content:flex-end;">
                                <button type="submit" class="btn btn-primary" style="width: 250px;">
                                    <i class="fa-solid fa-cloud-arrow-up"></i> Tải Lên Hệ Thống
                                </button>
                            </div>
                        </form>
                    </div>
                </section>

            </main>
        </div>
    </div>

    <!-- JAVASCRIPT FRONT-END CONTROL -->
    <script>
        const API_URL = ""; // Relative path to API endpoints
        let token = localStorage.getItem("histar_admin_token");
        let activeView = "view-analytics";

        // DOM elements
        const loginScreen = document.getElementById("login-screen");
        const dashboardScreen = document.getElementById("dashboard-screen");
        const loginForm = document.getElementById("login-form");
        const loginErrorMsg = document.getElementById("login-error-msg");
        const logoutBtn = document.getElementById("logout-btn");
        const displayName = document.getElementById("display-user-name");
        
        const menuItems = document.querySelectorAll(".menu-item");
        const viewSections = document.querySelectorAll(".view-section");
        
        // File upload visual hooks
        const markerInput = document.getElementById("marker-file-input");
        const videoInput = document.getElementById("video-file-input");
        const markerPreview = document.getElementById("marker-preview-name");
        const videoPreview = document.getElementById("video-preview-name");

        // Sync color picker with hex input
        const colorPicker = document.getElementById("key-color-picker");
        const colorHex = document.getElementById("key-color-hex");
        colorPicker.addEventListener("input", (e) => { colorHex.value = e.target.value; });
        colorHex.addEventListener("input", (e) => { colorPicker.value = e.target.value; });

        // Show toast helper
        const showToast = (message, isSuccess = true) => {
            const toast = document.getElementById("toast-notification");
            const icon = document.getElementById("toast-icon");
            const text = document.getElementById("toast-text");
            
            text.innerText = message;
            if (isSuccess) {
                toast.className = "glass-card toast toast-success show";
                icon.className = "fa-solid fa-circle-check toast-icon";
            } else {
                toast.className = "glass-card toast toast-error show";
                icon.className = "fa-solid fa-circle-exclamation toast-icon";
            }
            
            setTimeout(() => {
                toast.classList.remove("show");
            }, 4000);
        };

        // Switch workspace views
        const switchView = (viewId) => {
            viewSections.forEach(sec => sec.classList.remove("active"));
            menuItems.forEach(item => item.classList.remove("active"));
            
            document.getElementById(viewId).classList.add("active");
            document.querySelector(`[data-view="${viewId}"]`).classList.add("active");
            activeView = viewId;
            
            if (viewId === "view-analytics") {
                fetchAnalytics();
            } else if (viewId === "view-campaigns") {
                fetchCampaigns();
            }
        };

        menuItems.forEach(item => {
            item.addEventListener("click", () => {
                switchView(item.dataset.view);
            });
        });

        // Track file names inside upload wizard
        markerInput.addEventListener("change", (e) => {
            if (e.target.files.length > 0) {
                markerPreview.innerText = `✓ Đã chọn: ${e.target.files[0].name}`;
                markerPreview.style.display = "block";
            }
        });

        videoInput.addEventListener("change", (e) => {
            if (e.target.files.length > 0) {
                videoPreview.innerText = `✓ Đã chọn: ${e.target.files[0].name}`;
                videoPreview.style.display = "block";
            }
        });

        // Check authentication state
        const checkAuth = async () => {
            if (!token) {
                loginScreen.style.display = "flex";
                dashboardScreen.style.display = "none";
                return;
            }
            
            try {
                const response = await fetch(`${API_URL}/api/auth/me`, {
                    headers: { "Authorization": `Bearer ${token}` }
                });
                
                if (response.ok) {
                    const data = await response.json();
                    displayName.innerText = data.full_name || data.username;
                    loginScreen.style.display = "none";
                    dashboardScreen.style.display = "flex";
                    switchView("view-analytics");
                } else {
                    // Invalid token
                    logout();
                }
            } catch (e) {
                showToast("Lỗi máy chủ khi xác thực. Vui lòng thử lại sau.", false);
                logout();
            }
        };

        const logout = () => {
            localStorage.removeItem("histar_admin_token");
            token = null;
            loginScreen.style.display = "flex";
            dashboardScreen.style.display = "none";
        };

        logoutBtn.addEventListener("click", logout);

        // LOGIN SUBMIT
        loginForm.addEventListener("submit", async (e) => {
            e.preventDefault();
            loginErrorMsg.style.display = "none";
            
            const formData = new URLSearchParams();
            formData.append("username", document.getElementById("username").value);
            formData.append("password", document.getElementById("password").value);
            
            try {
                const response = await fetch(`${API_URL}/api/auth/login`, {
                    method: "POST",
                    headers: { "Content-Type": "application/x-www-form-urlencoded" },
                    body: formData
                });
                
                if (response.ok) {
                    const data = await response.json();
                    token = data.access_token;
                    localStorage.setItem("histar_admin_token", token);
                    displayName.innerText = data.full_name || data.username;
                    
                    loginScreen.style.display = "none";
                    dashboardScreen.style.display = "flex";
                    
                    showToast("Đăng nhập thành công! Chào mừng trở lại.");
                    switchView("view-analytics");
                } else {
                    const err = await response.json();
                    loginErrorMsg.innerText = err.detail || "Đăng nhập thất bại.";
                    loginErrorMsg.style.display = "block";
                }
            } catch (err) {
                loginErrorMsg.innerText = "Lỗi kết nối máy chủ backend.";
                loginErrorMsg.style.display = "block";
            }
        });

        // FETCH ANALYTICS SUMMARY
        const fetchAnalytics = async () => {
            try {
                const response = await fetch(`${API_URL}/api/analytics`, {
                    headers: { "Authorization": `Bearer ${token}` }
                });
                
                if (!response.ok) return;
                
                const data = await response.json();
                
                // Set counts
                document.getElementById("stat-total-campaigns").innerText = data.total_campaigns;
                document.getElementById("stat-total-scans").innerText = data.total_scans;
                document.getElementById("stat-total-visitors").innerText = data.total_unique_visitors;
                
                // Popularity bars
                const popContainer = document.getElementById("campaign-popularity-ranking");
                if (data.campaign_popularity.length === 0) {
                    popContainer.innerHTML = '<span style="color:var(--text-muted); text-align:center; display:block;">Chưa có lượt tương tác.</span>';
                } else {
                    const maxScans = Math.max(...data.campaign_popularity.map(p => p.scan_count), 1);
                    popContainer.innerHTML = data.campaign_popularity.map(item => {
                        const percent = (item.scan_count / maxScans) * 100;
                        return `
                            <div class="pop-item">
                                <div class="pop-meta">
                                    <span class="pop-name">${item.campaign_name}</span>
                                    <span class="pop-scans">${item.scan_count} lần quét</span>
                                </div>
                                <div class="pop-bar-bg">
                                    <div class="pop-bar-fill" style="width: ${percent}%"></div>
                                </div>
                            </div>
                        `;
                    }).join("");
                }
                
                // Live Scanned Feed
                const feedContainer = document.getElementById("live-scanned-feed");
                if (data.recent_scans.length === 0) {
                    feedContainer.innerHTML = '<li class="feed-item" style="border:none; background:transparent; justify-content:center;"><span style="color:var(--text-muted);">Chưa có hoạt động quét nào từ khách tham quan.</span></li>';
                } else {
                    // Pre-fetch campaign names map
                    const campaignsResponse = await fetch(`${API_URL}/api/campaigns`);
                    const campaigns = await campaignsResponse.json();
                    const campMap = {};
                    campaigns.forEach(c => campMap[c.id] = c.campaign_name);
                    
                    feedContainer.innerHTML = data.recent_scans.map(log => {
                        const date = new Date(log.scanned_at);
                        const timeStr = date.toLocaleTimeString("vi-VN", { hour: '2-digit', minute: '2-digit', second: '2-digit' }) + ' - ' + date.toLocaleDateString("vi-VN");
                        const name = campMap[log.campaign_id] || `Chiến dịch #${log.campaign_id}`;
                        const visitorName = log.visitor_session_id.substring(0, 8);
                        
                        return `
                            <li class="feed-item">
                                <div class="feed-icon"><i class="fa-solid fa-bolt"></i></div>
                                <div class="feed-content">
                                    <div class="feed-text">Khách tham quan <strong>#${visitorName}</strong> đã quét trúng <strong>${name}</strong></div>
                                    <div class="feed-time"><i class="fa-regular fa-clock"></i> ${timeStr}</div>
                                </div>
                            </li>
                        `;
                    }).join("");
                }
                
            } catch (e) {
                console.error("Error fetching analytics:", e);
            }
        };

        // FETCH CAMPAIGNS FOR THE TABLE
        const fetchCampaigns = async () => {
            const tableBody = document.getElementById("campaign-table-body");
            
            try {
                const response = await fetch(`${API_URL}/api/campaigns`);
                if (!response.ok) return;
                
                const data = await response.json();
                
                if (data.length === 0) {
                    tableBody.innerHTML = `
                        <tr>
                            <td colspan="6" style="text-align:center; color: var(--text-muted); padding: 30px;">
                                Chưa có chiến dịch nào được tạo. Nhấp "Thêm tài nguyên AR" để tạo mới!
                            </td>
                        </tr>
                    `;
                    return;
                }
                
                tableBody.innerHTML = data.map(item => {
                    return `
                        <tr>
                            <td>
                                <div class="campaign-meta">
                                    <img class="campaign-thumb" src="${item.marker_image_url || 'https://images.unsplash.com/photo-1524661135-423995f22d0b?w=100'}" alt="Marker Image">
                                    <div>
                                        <div class="campaign-name">${item.campaign_name}</div>
                                        <div class="campaign-desc" title="${item.description || ''}">${item.description || 'Chưa có mô tả chi tiết...'}</div>
                                    </div>
                                </div>
                            </td>
                            <td><span class="badge badge-gold">${item.target_index}</span></td>
                            <td><span class="badge badge-cyan">${item.target_id}</span></td>
                            <td>
                                <div style="display:flex; align-items:center; gap:8px;">
                                    <span style="display:inline-block; width:14px; height:14px; border-radius:50%; background:${item.key_color}; border: 1px solid rgba(255,255,255,0.2)"></span>
                                    <code>${item.key_color}</code>
                                </div>
                            </td>
                            <td><code>${item.chroma_threshold}</code></td>
                            <td>
                                <div class="action-btns">
                                    <a class="icon-btn" href="${item.video_overlay_url}" target="_blank" title="Xem video mô phỏng">
                                        <i class="fa-solid fa-play"></i>
                                    </a>
                                    <button class="icon-btn delete" onclick="deleteCampaign(${item.id})" title="Xóa tài nguyên">
                                        <i class="fa-solid fa-trash-can"></i>
                                    </button>
                                </div>
                            </td>
                        </tr>
                    `;
                }).join("");
                
            } catch (e) {
                console.error("Error fetching campaigns:", e);
                tableBody.innerHTML = `<tr><td colspan="6" style="text-align:center; color: var(--color-crimson);">Lỗi kết nối dữ liệu máy chủ backend.</td></tr>`;
            }
        };

        // DELETE CAMPAIGN ACTION
        window.deleteCampaign = async (id) => {
            if (!confirm("Bạn có chắc chắn muốn xóa chiến dịch này? Hành động này sẽ xóa vĩnh viễn tệp ảnh và video khỏi máy chủ.")) {
                return;
            }
            
            try {
                const response = await fetch(`${API_URL}/api/campaigns/${id}`, {
                    method: "DELETE",
                    headers: { "Authorization": `Bearer ${token}` }
                });
                
                if (response.ok) {
                    showToast("Đã xóa chiến dịch thành công.");
                    fetchCampaigns();
                } else {
                    const err = await response.json();
                    showToast(err.detail || "Không thể xóa chiến dịch.", false);
                }
            } catch (e) {
                showToast("Lỗi kết nối máy chủ.", false);
            }
        };

        // WIZARD CREATE FORM SUBMIT
        const wizardForm = document.getElementById("wizard-upload-form");
        wizardForm.addEventListener("submit", async (e) => {
            e.preventDefault();
            
            const submitBtn = wizardForm.querySelector("button[type='submit']");
            const originalBtnHtml = submitBtn.innerHTML;
            
            // Set loading state
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<i class="fa-solid fa-circle-notch fa-spin"></i> Đang tải tệp tin lên...';
            
            const formData = new FormData();
            formData.append("target_index", document.getElementById("target-index-input").value);
            formData.append("target_id", document.getElementById("target-id-input").value);
            formData.append("campaign_name", document.getElementById("campaign-name-input").value);
            formData.append("key_color", document.getElementById("key-color-hex").value);
            formData.append("chroma_threshold", document.getElementById("threshold-input").value);
            formData.append("description", document.getElementById("description-input").value);
            
            formData.append("marker_image", markerInput.files[0]);
            formData.append("video", videoInput.files[0]);
            
            try {
                const response = await fetch(`${API_URL}/api/campaigns`, {
                    method: "POST",
                    headers: { "Authorization": `Bearer ${token}` },
                    body: formData
                });
                
                if (response.ok) {
                    showToast("Đã tạo và tải lên chiến dịch AR thành công!");
                    wizardForm.reset();
                    markerPreview.style.display = "none";
                    videoPreview.style.display = "none";
                    colorPicker.value = "#00ff00";
                    colorHex.value = "#00ff00";
                    switchView("view-campaigns");
                } else {
                    const err = await response.json();
                    showToast(err.detail || "Tải lên tài nguyên thất bại.", false);
                }
            } catch (err) {
                showToast("Lỗi kết nối hoặc kích thước tệp tin quá lớn.", false);
            } finally {
                submitBtn.disabled = false;
                submitBtn.innerHTML = originalBtnHtml;
            }
        });

        // Initialize App on load
        checkAuth();
    </script>
</body>
</html>
"""
    return html_content
