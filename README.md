# HISTAR - Bảo tàng Lịch sử Quân Sự Việt Nam AR

## Thành viên và đóng góp

Mỗi thành viên đóng góp 20% vào dự án.

| STT | MSV - Họ và tên | Tỷ lệ đóng góp |
| --- | --- | --- |
| 1 | MSV1 - Họ và tên thành viên 1 | 20% |
| 2 | MSV2 - Họ và tên thành viên 2 | 20% |
| 3 | MSV3 - Họ và tên thành viên 3 | 20% |
| 4 | MSV4 - Họ và tên thành viên 4 | 20% | 
| 5 | MSV5 - Họ và tên thành viên 5 | 20% |

## Giới thiệu dự án

HISTAR là một trải nghiệm web AR dùng A-Frame và MindAR để quét bản đồ/marker lịch sử, hiển thị video mô phỏng bằng chroma key và theo dõi tiến độ thu thập chiến dịch của người dùng.

Dự án hướng tới việc tạo ra một hình thức tham quan tương tác cho nội dung lịch sử quân sự Việt Nam. Người dùng mở website trên trình duyệt, cấp quyền camera, quét marker đã được huấn luyện trong file `assets/target.mind`, sau đó xem lớp video AR được đặt trực tiếp lên marker.

## Mục tiêu dự án

- Xây dựng trải nghiệm thực tế tăng cường chạy trực tiếp trên trình duyệt.
- Quét marker từ file `assets/target.mind` bằng MindAR.
- Hiển thị video mô phỏng tương ứng với từng marker.
- Lưu tiến độ người dùng bằng `localStorage`.
- Cung cấp giao diện nhiệm vụ, thông báo khi tìm thấy chiến dịch mới và màn hình hoàn thành.

## Công nghệ sử dụng

- HTML5: xây dựng cấu trúc giao diện và scene AR.
- CSS3: thiết kế màn hình bắt đầu, HUD, toast và màn hình hoàn thành.
- JavaScript: xử lý logic tiến độ, video, component A-Frame và chroma key.
- A-Frame `1.3.0`: dựng scene WebXR/WebAR.
- MindAR `1.2.2`: nhận diện image target.
- Three.js: được A-Frame sử dụng bên dưới, dùng trực tiếp cho `VideoTexture` và `ShaderMaterial`.

## Cấu trúc thư mục

```text
HISTAR/
├── assets/
│   ├── target.mind     # File dữ liệu marker cho MindAR
│   ├── video1.mp4      # Video hiển thị cho targetIndex 0
│   └── video2.mp4      # Video hiển thị cho targetIndex 1
├── index.html          # Cấu trúc HTML và scene AR
├── styles.css          # Toàn bộ CSS của giao diện
├── script.js           # Toàn bộ JavaScript xử lý AR, video và tiến độ
└── README.md           # Tài liệu dự án
```

## Chức năng chính

### 1. Màn hình bắt đầu

Người dùng nhấn nút bắt đầu để kích hoạt trải nghiệm AR. Trước khi vào AR, hệ thống gọi phát/tạm dừng video một lần để hỗ trợ chính sách autoplay trên trình duyệt di động.

### 2. Quét marker AR

Scene AR sử dụng:

```html
<a-scene mindar-image="imageTargetSrc: ./assets/target.mind; autoStart: true;">
```

Khi camera nhận diện được marker, entity tương ứng sẽ kích hoạt các component:

- `map-tracker`: ghi nhận chiến dịch đã tìm thấy.
- `video-handler`: phát video khi marker xuất hiện và tạm dừng khi marker mất.
- `chromakey-video`: loại nền xanh của video bằng shader.

### 3. Lưu tiến độ

Tiến độ được lưu trong `localStorage` với key:

```text
ar_museum_progress
```

Người dùng có thể xóa dữ liệu để chơi lại từ đầu bằng nút `Xóa Dữ Liệu (Chơi Lại)`.

### 4. HUD nhiệm vụ

HUD hiển thị số lượng chiến dịch đã thu thập theo định dạng:

```text
[ số_đã_tìm / 10 ]
```

Khi người dùng tìm đủ 10 chiến dịch, màn hình hoàn thành sẽ xuất hiện.

## Cách chạy dự án

Do trình duyệt cần quyền camera và tải file asset cục bộ, nên chạy dự án qua một local server thay vì mở trực tiếp file HTML.

Nếu có Python:

```bash
python -m http.server 8000
```

Sau đó mở:

```text
http://localhost:8000
```

Trên điện thoại, cần đảm bảo thiết bị cùng mạng với máy chạy server và truy cập qua địa chỉ IP nội bộ của máy tính.

## Cách thêm marker/video mới

1. Thêm video mới vào thư mục `assets`, ví dụ `assets/video3.mp4`.
2. Khai báo video trong `<a-assets>`:

```html
<video id="vid2" src="./assets/video3.mp4" loop playsinline preload="auto"></video>
```

3. Thêm entity mới với `targetIndex` tương ứng trong file `assets/target.mind`:

```html
<a-entity mindar-image-target="targetIndex: 2"
          map-tracker="targetId: 2; targetName: Tên chiến dịch"
          video-handler="video: #vid2">
    <a-plane chromakey-video="src: #vid2; threshold: 0.4" position="0 0 0" height="1" width="1"></a-plane>
</a-entity>
```

4. Nếu tổng số marker thay đổi, cập nhật hằng số trong `script.js`:

```js
const TOTAL_MAPS = 10;
```

## Ghi chú triển khai

- File `.mind` và các video `.mp4` được đặt trong thư mục `assets` để quản lý tài nguyên tập trung.
- `script.js` được load trong `<head>` sau A-Frame và MindAR để component được đăng ký trước khi scene AR được parse.
- Toàn bộ CSS inline đã được chuyển sang `styles.css`.
- Toàn bộ JavaScript inline đã được chuyển sang `script.js`.
- Các style inline của màn hình hoàn thành cũng đã được đưa vào CSS riêng.

## Tác giả

Nhóm phát triển HISTAR.
