# HISTAR - Hệ thống Web-AR tương tác lịch sử quân sự trên nền tảng bảo tàng số

Báo cáo Bài tập lớn
Học phần: INT3121 - Các chuyên đề trong KHMT (Nhóm 15)
Giảng viên hướng dẫn: TS. Ngô Thị Duyên

## Đóng góp của các thành viên

| MSSV | Họ và tên | Công việc | Đóng góp |
| :---: | ----- | ----- | :---: |
| 23021466 | Nguyễn Hồng Anh | Thiết kế, triển khai CSDL. Cấu hình môi trường Docker và thiết kế Backend. Tiến hành khảo sát người dùng. | 20% |
| 23021506 | Trần Ánh Duy | Nghiên cứu, tích hợp thư viện MindAR để trích xuất điểm đặc trưng và nhận diện Marker bản đồ và thiết kế Backend. Tiến hành khảo sát người dùng. | 20% |
| 23021546 | Đậu Đức Hiếu | Xây dựng giao diện Client Web-AR trên trình duyệt di động và giao diện Admin Dashboard, tích hợp thư viện MindAR. Tiến hành kiểm thử chức năng. | 20% |
| 23021494 | Nguyễn Đức Dũng | Thiết kế và phát triển Admin Dashboard, xây dựng logic xử lý khi đăng tải hình ảnh sơ đồ trận đánh và video mô phỏng. Tiến hành kiểm thử hiệu năng FPS/Độ trễ. | 20% |
| 23021498 | Nguyễn Tiến Dũng | Xây dựng logic quản lý trạng thái trải nghiệm và cơ chế lưu trữ tiến độ phía Client, phát triển tính năng tích hợp Gamification. Thiết lập các kịch bản kiểm thử chức năng và phi chức năng. | 20% |

---

## 1. Giới thiệu

### 1.1. Đặt vấn đề và bối cảnh thực tế
Trong kỷ nguyên số hóa và cuộc cách mạng công nghiệp 4.0, việc ứng dụng công nghệ thông tin vào bảo tồn, phát huy giá trị di sản văn hóa và lịch sử đang trở thành một xu thế tất yếu. Xu hướng "Bảo tàng số" và du lịch thông minh đang mở ra những phương thức tiếp cận mới, xóa nhòa khoảng cách giữa hiện vật tĩnh và người xem.

Tại Bảo tàng Lịch sử Quân sự Việt Nam, nơi lưu trữ những trang sử hào hùng của dân tộc, thực trạng tham quan hiện nay cho thấy một nghịch lý đáng suy ngẫm. Khách tham quan, đặc biệt là thế hệ trẻ, thường dễ bị thu hút bởi các hiện vật khối lớn, trực quan như vũ khí, máy bay, xe tăng. Ngược lại, các bản đồ trận đánh, sa bàn chiến dịch nơi chứa đựng tư duy chiến thuật, diễn biến cốt lõi và tinh hoa quân sự của cha ông lại thường bị ngó lơ hoặc khó tiếp thu. Nguyên nhân chính xuất phát từ tính chất khô khan, phức tạp và trừu tượng của các sơ đồ giấy truyền thống. Người xem rất khó hình dung được hướng tiến quân, các mũi đột kích hay diễn biến thay đổi theo thời gian chỉ qua các mũi tên và ký hiệu tĩnh trên mặt phẳng.

### 1.2. Bài toán kỹ thuật Web-AR và Quản lý trạng thái
*   **Định nghĩa bài toán kỹ thuật Web-AR:** Bài toán cốt lõi của dự án là nghiên cứu và xây dựng hệ thống "HISTAR" - một ứng dụng Web-AR chạy trực tiếp trên các trình duyệt thiết bị di động phổ biến thông qua giao thức bảo mật HTTPS. Hệ thống giải quyết hai thách thức kỹ thuật lớn:
    1.  Nhận diện và theo dõi hình ảnh mục tiêu (Marker bản đồ chiến thuật quân sự phẳng) trong môi trường thực tế bảo tàng với điều kiện ánh sáng phức tạp, đổ bóng hoặc thay đổi góc nhìn.
    2.  Đảm bảo khả năng hiển thị nội dung mượt mà trên thiết bị di động bằng cách tận dụng GPU để khử dải màu xanh (Chroma key) của video mô phỏng trận đánh trực tiếp trên bản đồ mà không làm giảm hiệu năng hệ thống.
*   **Giải pháp Web-AR:** Khách tham quan không cần tải ứng dụng nặng từ App Store hoặc Google Play, loại bỏ rào cản thời gian và dung lượng mạng. Chỉ cần thực hiện thao tác quét mã QR đơn giản bằng trình duyệt sẵn có trên điện thoại để trải nghiệm trực quan hóa sinh động.
*   **Quản lý trạng thái và Gamification:** Duy trì và lưu trữ tiến trình khám phá của khách tham quan dưới dạng một chuỗi nhiệm vụ tương tác thu thập tư liệu lịch sử. Trạng thái này được lưu trữ an toàn ngay tại localStorage phía Client và cập nhật động trong suốt quá trình trải nghiệm.

### 1.3. Mục tiêu và Phạm vi nghiên cứu
*   **Mục tiêu:** Phát triển ứng dụng Web-AR ổn định trên trình duyệt di động, độ trễ thấp, khử nền video chính xác bằng Shader Custom trên GPU, lưu trữ tiến trình an toàn không bị mất khi tải lại trang, nâng cao tính khám phá chủ động của người học.
*   **Phạm vi nghiên cứu:** Tập trung xây dựng giải pháp trình diễn các chiến dịch lịch sử quân sự Việt Nam. Hệ thống hỗ trợ cấu hình nội dung động, mở rộng nhiều kịch bản khác nhau. Phạm vi thử nghiệm thực hiện trên 10 chiến dịch quân sự tiêu biểu, trong đó giai đoạn ban đầu đã hoàn thiện dữ liệu mẫu cho 2 chiến dịch:
    1.  Chiến thắng Bạch Đằng của Ngô Quyền trước quân Nam Hán (năm 938).
    2.  Chiến dịch Lý Thường Kiệt tiến công phủ đầu nhà Tống (1075 - 1076).

---

## 2. Kiến trúc và Luồng hoạt động của hệ thống

Hệ thống được thiết kế theo mô hình kiến trúc Client-Server tách biệt, giao tiếp qua giao thức bảo mật HTTPS và chuẩn RESTful API.

### 2.1. Các thành phần chính
1.  **Client-AR (Mobile Web Application):** Giao diện tương tác trực tiếp của khách tham quan chạy trên trình duyệt di động (Safari, Chrome, ...). Chịu trách nhiệm khởi tạo camera, thu nhận luồng hình ảnh thời gian thực, thực hiện thuật toán thị giác máy tính nhận diện bản đồ chiến thuật (Marker) và hiển thị các video mô phỏng tách nền.
2.  **Backend API & Admin Dashboard (Server-Side):** Hệ thống quản trị trung tâm dành cho kỹ thuật viên và ban quản lý bảo tàng. Admin Panel hỗ trợ đăng tải, sửa đổi hoặc xóa bỏ các tài nguyên lịch sử số hóa (ảnh sơ đồ, video mô phỏng, tham số lọc màu). Máy chủ cung cấp RESTful API phân phối cấu hình dữ liệu động (JSON Payload) cho Client.

### 2.2. Quy trình nghiệp vụ cốt lõi
*   **Quy trình quản trị số hóa (Dành cho Kỹ thuật viên):**
    1.  Kỹ thuật viên đăng nhập Admin Dashboard với tài khoản định danh hợp lệ.
    2.  Chọn chức năng "Thêm mới chiến dịch lịch sử".
    3.  Tải lên tệp ảnh sơ đồ bản đồ (.png/.jpg), video mô phỏng trận đánh (.mp4 đã tách nền xanh) và cấu hình hệ số threshold (ngưỡng lọc màu xanh) cho Shader.
    4.  Hệ thống tiếp nhận luồng dữ liệu, lưu trữ file vật lý tĩnh và ghi nhận Metadata vào CSDL PostgreSQL.
*   **Quy trình trải nghiệm tương tác AR (Dành cho Khách tham quan):**
    1.  Người dùng quét mã QR để truy cập ứng dụng Web-AR trên trình duyệt di động qua giao thức HTTPS.
    2.  Ứng dụng tự động gửi request bất đồng bộ `fetch()` để tải danh sách cấu hình, Marker và Video từ Backend.
    3.  Người dùng hướng camera về phía bản đồ chiến thuật trưng bày tại bảo tàng.
    4.  Thư viện MindAR phát hiện điểm đặc trưng trùng khớp với Marker (sự kiện `targetFound`). Thực thể VideoTexture tương ứng được phủ lên mặt phẳng bản đồ. GPU chạy Shader khử màu xanh nền để hiển thị hành quân trực quan thời gian thực.
    5.  Hệ thống gửi thông báo Toast dạng UI chúc mừng, ghi nhận mã chiến dịch vào `localStorage` của trình duyệt. Thanh hiển thị tiến độ (HUD Mission Tracker) cập nhật tiến độ tương ứng.
    6.  Khi quét đủ số lượng bản đồ chiến dịch yêu cầu, ứng dụng hiển thị màn hình chúc mừng Hoàn thành toàn diện (Completion UI) và dừng tương tác để giải phóng tài nguyên.

---

## 3. Phân tích và Thiết kế hệ thống

### 3.1. Thiết kế phân tầng
Hệ thống gồm 4 tầng chức năng chính:
1.  **Tầng giao diện người dùng (Presentation Layer):**
    *   Client di động: HTML5 và CSS3 DOM, thiết kế Responsive tối ưu cho màn hình cảm ứng di động.
    *   Admin Panel: Bảng điều khiển quản trị bằng biểu mẫu và kéo thả tài nguyên.
2.  **Tầng điều khiển và Đồ họa (Application/AR Engine Layer):**
    *   A-Frame: Framework quản lý thực thể đồ họa 3D theo mô hình ECS.
    *   MindAR: Thư viện xử lý thị giác máy tính nhận diện và theo dõi hình ảnh tham chiếu (Image Tracking).
    *   Three.js: Lớp lõi quản lý WebGL Scene, nạp luồng pixel video vào GPU làm VideoTexture để chạy bộ lọc khử nền.
3.  **Tầng dịch vụ máy chủ (Backend API Layer):**
    *   FastAPI (Python): Xây dựng RESTful API dạng Stateless, cung cấp Endpoint để phân phối cấu hình JSON và tiếp nhận dữ liệu tải lên bất đồng bộ với tốc độ cao.
4.  **Tầng lưu trữ dữ liệu (Data Layer):**
    *   PostgreSQL: Lưu trữ thông tin tài khoản, metadata chiến dịch quân sự, cấu hình marker và đường dẫn tĩnh.
    *   localStorage: Cơ chế lưu trữ cục bộ trên trình duyệt để quản lý tiến độ Gamification của người dùng.

### 3.2. Thiết kế Cơ sở dữ liệu (Bảng Campaigns)

| Trường dữ liệu | Kiểu dữ liệu | Mô tả |
| :---: | :---: | ----- |
| id (PK) | Integer | Mã định danh duy nhất tăng tự động của chiến dịch lịch sử quân sự. |
| target\_index | Integer | Chỉ số liên kết ánh xạ với thứ tự chỉ mục tập tin chứa tệp biên dịch nhận diện .mind |
| campaign\_name | Varchar(255) | Tên chiến dịch lịch sử hiển thị trên thông báo HUD hoặc Toast chúc mừng. |
| marker\_image\_url | Varchar(512) | Đường dẫn lưu trữ hình ảnh bản đồ làm Marker để hiển thị xem trước. |
| video\_overlay\_url | Varchar(512) | Đường dẫn lưu trữ tệp tin video mô phỏng trận đánh (.mp4, codec H.264). |
| chroma\_threshold | Float | Hệ số lọc nhiễu nền xanh (Similarity Threshold) tùy biến cho Shader. |

---

## 4. Triển khai và Kiểm thử hệ thống

### 4.1. Công nghệ sử dụng
*   **Client:** HTML5, CSS3, JavaScript, A-Frame, MindAR, Three.js, WebGL/GLSL.
*   **Backend:** Python, FastAPI.
*   **Database & Storage:** PostgreSQL, Local Directory/Cloud Storage S3.
*   **Môi trường & Quy trình xuất bản:**
    *   Client được triển khai tĩnh trên nền tảng Vercel.
    *   Backend và Database được đóng gói bằng Docker và triển khai trên máy chủ ảo VPS độc lập.
    *   Cấu hình môi trường phát triển cục bộ hỗ trợ chuyển tiếp kết nối HTTPS qua Ngrok để kiểm thử trực tiếp trên điện thoại.

### 4.2. Kiểm thử yêu cầu chức năng (Black-box Testing)

| Mã kịch bản | Giao diện | Kịch bản kiểm thử | Mô tả chi tiết | Kết quả mong đợi | Trạng thái |
| ----- | ----- | ----- | ----- | ----- | ----- |
| KT-CN-01 | Admin Dashboard | Xác thực và phân quyền tài khoản | Kiểm tra tính năng đăng nhập của kỹ thuật viên. | Từ chối tài khoản sai mật khẩu; Điều hướng tài khoản đúng vào trang quản trị. | ĐẠT |
| KT-CN-02 | Admin Dashboard | Đăng tải nội dung số hóa chiến dịch mới | Kỹ thuật viên tải Video mô phỏng nền xanh, nhập thông tin chiến dịch và cấu hình giá trị Chroma Key. | Tiếp nhận luồng file, ghi nhận metadata vào PostgreSQL và hiển thị thông báo thành công. | ĐẠT |
| KT-CN-03 | Client AR | Đồng bộ dữ liệu động (Fetch Dynamic Content) | Người dùng truy cập ứng dụng Web-AR thông qua trình duyệt di động. | Ứng dụng tự động gửi request API lên server và nhận thành công cấu hình JSON. | ĐẠT |
| KT-CN-04 | Client AR | Nhận diện thị giác máy tính và Lọc nền video | Người dùng hướng camera vào bản đồ giấy chiến dịch. | Thư viện MindAR nhận diện trong vòng dưới 1.5 giây, video tự động phủ (overlay) chính xác lên bản đồ. | ĐẠT |
| KT-CN-05 | Client AR | Lưu trữ tiến độ nhiệm vụ (Gamification) | Kiểm tra luồng ghi nhận khi người dùng quét thành công bản đồ mới. | Hiển thị Toast chúc mừng, HUD tăng tiến độ, dữ liệu lưu xuống localStorage không bị mất khi reload. | ĐẠT |
| KT-CN-06 | Client AR | Hoàn thành toàn bộ chuỗi nhiệm vụ | Người dùng hoàn thành quét đầy đủ số lượng bản đồ theo cấu hình. | Dừng tương tác đồ họa để giải phóng tài nguyên CPU/GPU và hiển thị Completion UI chúc mừng. | ĐẠT |

### 4.3. Kiểm thử hiệu năng (Phi chức năng)
*   **Tốc độ khung hình (FPS):**
    *   Thiết bị cấu hình cao (iOS - iPhone XS trở lên / Android - Snapdragon 8 Gen 1 trở lên): Đạt ổn định ở mức 55 - 60 FPS trong suốt chu trình nhận diện và phát video.
    *   Thiết bị cấu hình trung bình - thấp: Khi chạy Shader khử nền xanh, FPS duy trì ở mức 35 - 45 FPS, đảm bảo độ mượt mà cần thiết.
*   **Độ trễ nhận diện (Tracking Latency):** Trung bình đạt 800ms - 1200ms từ lúc camera tiếp cận trọn vẹn marker đến khi hiển thị video trong điều kiện ánh sáng phòng bảo tàng.
*   **Tiêu thụ tài nguyên:** RAM chiếm dụng tối đa của tab trình duyệt dao động từ 180MB đến 250MB.

---

## 5. Kết quả thực nghiệm và khảo sát ý kiến người dùng

Quy trình thử nghiệm được tiến hành thực tế tại Bảo tàng Lịch sử Quân sự Việt Nam trên hai nhóm đối tượng: Nhóm quản trị nội dung (03 cán bộ kỹ thuật) và Nhóm khách tham quan (10 người độ tuổi từ 10 đến 60 tuổi).

### 5.1. Khảo sát định lượng đối với Khách tham quan
Khảo sát sử dụng thang đo Likert 5 mức độ (1: Rất không hài lòng/Khó sử dụng, 5: Rất hài lòng/Dễ sử dụng).

| STT | Tiêu chí đánh giá | Điểm trung bình | Độ lệch chuẩn |
| :---: | ----- | :---: | :---: |
| 1 | Mức độ thuận tiện khi truy cập ứng dụng bằng mã QR | 4.6 | 0.49 |
| 2 | Khả năng nhận diện và hiển thị nội dung AR trên bản đồ lịch sử | 4.4 | 0.52 |
| 3 | Mức độ dễ dàng khi sử dụng các chức năng của ứng dụng | 4.5 | 0.50 |
| 4 | Khả năng hỗ trợ hiểu diễn biến chiến dịch lịch sử | 4.8 | 0.40 |
| 5 | Mức độ ghi nhớ thông tin lịch sử sau khi trải nghiệm | 4.6 | 0.52 |
| 6 | Mức độ hứng thú trong quá trình khám phá các chiến dịch | 4.5 | 0.53 |
| 7 | Tốc độ phản hồi và độ mượt của ứng dụng | 4.2 | 0.63 |
| 8 | Mức độ hài lòng chung đối với hệ thống | 4.7 | 0.46 |

*   **Điểm hài lòng trung bình chung:** 4.54/5.00

### 5.2. Khảo sát định lượng đối với Nhóm quản trị

| STT | Tiêu chí đánh giá | Điểm trung bình | Nhận xét |
| :---: | ----- | :---: | :---: |
| 1 | Giao diện quản trị rõ ràng và dễ sử dụng | 4.33 | Tốt |
| 2 | Thuận tiện khi thêm mới hoặc cập nhật dữ liệu chiến dịch | 4.67 | Rất tốt |
| 3 | Dễ dàng tải lên hình ảnh và video minh họa | 4.67 | Rất tốt |
| 4 | Khả năng tự quản lý nội dung mà không cần chỉnh sửa mã nguồn | 4.67 | Rất tốt |
| 5 | Mức độ hài lòng chung đối với hệ thống quản trị | 4.33 | Tốt |

*   **Điểm hài lòng trung bình chung:** 4.53/5.00

### 5.3. Đánh giá chung từ thực nghiệm
*   **Kết quả đạt được:** Hệ thống chạy ổn định trên cả iOS và Android, khả năng nhận diện hình ảnh chính xác dưới ánh sáng bảo tàng. Tốc độ tải và hiển thị video tốt. Khách tham quan đánh giá cao tính trực quan của Web-AR so với sơ đồ tĩnh truyền thống. Giao diện quản trị giúp ban quản lý cập nhật kịch bản dễ dàng, nhanh chóng mà không cần lập trình lại.
*   **Hạn chế còn tồn tại:** Dưới điều kiện ánh sáng yếu hoặc bị lóa kính bảo vệ, thời gian nhận diện marker có thể kéo dài. Video mô phỏng dung lượng lớn đòi hỏi kết nối mạng 4G/5G/Wifi ổn định ở lần tải trang đầu tiên.
*   **Đóng góp ý kiến cải tiến:** Người dùng đề xuất bổ sung thêm nút điều khiển video (tạm dừng, tua lại) để dễ quan sát chiến dịch.

---

## 6. Kết luận và Hướng phát triển tương lai

### 6.1. Các kết quả đã đạt được
*   **Về mặt công nghệ:** Xây dựng thành công Client Web-AR chạy trực tiếp trên các trình duyệt tiêu chuẩn không cần ứng dụng cài đặt trung gian. Tích hợp MindAR cho tốc độ nhận dạng tốt (< 1.5 giây), hiệu năng đồ họa từ 35 - 60 FPS. Cài đặt thành công Shader Custom (Chroma Key) trên GPU để khử nền xanh video tư liệu trực quan.
*   **Về mặt quản trị:** Thiết kế hoàn chỉnh kiến trúc Client-Server tách biệt, phân phối dữ liệu qua RESTful API động từ Backend FastAPI tới Client. Xây dựng Admin Panel dễ sử dụng cho kỹ thuật viên.
*   **Về mặt trải nghiệm:** Tích hợp thành công cơ chế lưu trữ tiến độ chơi (Gamification) trên thiết bị người dùng qua localStorage và hiển thị sinh động qua thanh HUD Mission Tracker.

### 6.2. Hướng phát triển tương lai
*   **Mở rộng phân quyền (RBAC):** Bổ sung cơ chế quản lý phân quyền nâng cao trên Admin Dashboard, bao gồm các vai trò: Quản trị viên tối cao (Hạ tầng), Biên tập viên nội dung (Duyệt kịch bản lịch sử) và Kỹ thuật viên (Đăng tải tài nguyên số).
*   **Công nghệ AR dựa trên vị trí (Location-based AR):** Nghiên cứu tích hợp định vị không gian, tọa độ GPS kết hợp la bàn thiết bị để dẫn đường và gợi ý lộ trình tham quan cho du khách khi di chuyển giữa các phân khu trưng bày trong khuôn viên rộng lớn của bảo tàng.
