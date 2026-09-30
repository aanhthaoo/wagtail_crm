# HƯỚNG DẪN CÀI ĐẶT VÀ SỬ DỤNG HỆ THỐNG
## WAGTAIL AI CRM & BUSINESS INTELLIGENCE DASHBOARD

Tài liệu này hướng dẫn chi tiết từng bước từ lúc tải mã nguồn từ GitHub về máy mới cho đến khi vận hành và trải nghiệm đầy đủ các tính năng thông minh của hệ thống.

---

## 1. YÊU CẦU MÔI TRƯỜNG (PREREQUISITES)

- **Hệ điều hành**: Windows 10/11, macOS, hoặc Linux / Ubuntu.
- **Python**: Phiên bản `3.11` hoặc `3.12` (Khuyến nghị Python 3.12).
- **Git**: Đã cài đặt Git trên máy.
- **Gemini API Key**: Miễn phí từ [Google AI Studio](https://aistudio.google.com/).

---

## 2. QUY TRÌNH CÀI ĐẶT 6 BƯỚC CHO MÁY MỚI (SETUP GUIDE)

### Bước 1: Clone mã nguồn từ GitHub
Mở terminal (PowerShell trên Windows hoặc Terminal trên macOS/Linux) và chạy:
```powershell
git clone https://github.com/aanhthaoo/wagtail_crm.git
cd wagtail_crm
```

---

### Bước 2: Tạo và kích hoạt môi trường ảo (Virtual Environment)
```powershell
# Tạo môi trường ảo tên 'venv'
python -m venv venv

# Kích hoạt môi trường ảo trên Windows (PowerShell):
.\venv\Scripts\activate

# (Nếu dùng Command Prompt cmd.exe: venv\Scripts\activate.bat)
# (Nếu dùng macOS/Linux: source venv/bin/activate)
```

---

### Bước 3: Cài đặt các thư viện phụ thuộc
```powershell
pip install -r requirements.txt
```

---

### Bước 4: Thiết lập cấu hình biến môi trường (`.env`)
Tạo file `.env` tại thư mục gốc của dự án bằng cách copy từ file mẫu:

```powershell
# Trên Windows PowerShell:
Copy-Item .env.example .env

# Hoặc trên Linux/macOS:
cp .env.example .env
```

Mở file `.env` vừa tạo và cập nhật các thông số:
```env
# Cấu hình Django
DEBUG=True
DJANGO_SECRET_KEY=django-insecure-any-secret-key-for-local-dev-12345

# Khóa API Google Gemini (Bắt buộc để chạy tính năng AI)
GEMINI_API_KEY=AIzaSyYourActualGeminiAPIKeyHere
```

> [!TIP]
> **Cách lấy Gemini API Key miễn phí trong 1 phút:**
> 1. Truy cập [https://aistudio.google.com/](https://aistudio.google.com/) và đăng nhập bằng tài khoản Google.
> 2. Chọn **"Get API key"** -> **"Create API key"**.
> 3. Copy chuỗi khóa và dán vào dòng `GEMINI_API_KEY=...` trong file `.env`.

---

### Bước 5: Khởi tạo Cơ sở dữ liệu & Nạp dữ liệu mẫu
```powershell
# 1. Chạy migrations để khởi tạo cấu trúc bảng SQLite
python manage.py migrate

# 2. Tạo tài khoản quản trị viên (Superuser)
python manage.py createsuperuser
# -> Nhập username (ví dụ: admin), email, mật khẩu

# 3. Nạp bộ dữ liệu mẫu (8 khách hàng, 43 tương tác, 12 đơn hàng)
python manage.py seed_crm_data
```

---

### Bước 6: Khởi chạy Server
```powershell
python manage.py runserver
```

Khi khởi động, terminal sẽ hiển thị bảng điều hướng các URL:
- **CRM Executive Dashboard**: [http://127.0.0.1:8000/crm/dashboard/](http://127.0.0.1:8000/crm/dashboard/)
- **Wagtail CMS Admin**: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
- **Django Native Admin**: [http://127.0.0.1:8000/django-admin/](http://127.0.0.1:8000/django-admin/)

---

## 3. HƯỚNG DẪN SỬ DỤNG CÁC TÍNH NĂNG CHÍNH

### 3.1. Trải nghiệm Executive Dashboard & Kích hoạt AI Phân Tích

1. Truy cập [http://127.0.0.1:8000/crm/dashboard/](http://127.0.0.1:8000/crm/dashboard/).
2. **Quan sát 4 thẻ KPI thống kê**:
   - *Tổng khách hàng*: Số lượng bản ghi hiện có trong hệ thống.
   - *Điểm tiềm năng TB (Lead Score)*: Tính toán trung bình động thời gian thực.
   - *Khách nguy cơ cao (High Churn Risk)*: Cảnh báo những khách hàng cần chăm sóc khẩn cấp.
   - *Doanh số dự kiến (Forecast Revenue)*: Tổng giá trị đơn hàng đang đàm phán hoặc đã chốt.
3. **Kích hoạt Phân tích AI theo thời gian thực (Real-time Async Analysis)**:
   - Trên bảng khách hàng, tìm những khách hàng có trạng thái `Điểm AI: --` (ví dụ: *Nguyen Hoang Nam*, *Vo Minh Tri*, *Dang Thu Thao*).
   - Nhấn nút **[⚡ Phân tích AI]** ở cột Thao tác.
   - Nút sẽ hiển thị spinner tải dữ liệu và tự động cập nhật ngay trên giao diện kết quả:
     - Điểm tiềm năng (**Lead Score 1-100**)
     - Sắc thái cảm xúc (**Sentiment: Positive / Neutral / Negative**)
     - Mức độ rủi ro rời bỏ (**Churn Risk: Low / Medium / High**)
     - Tóm tắt tình trạng & Đề xuất hành động tiếp theo (**Next Action**)
4. **Xem Báo cáo Chi tiết 4 Trụ Cột (Interactive Modal)**:
   - **Click chuột vào bất kỳ hàng nào** trên bảng khách hàng.
   - Modal chi tiết sẽ mở ra với 4 thẻ màu phân tích chuyên sâu:
     - 🟣 **Thuộc tính định danh & ICP Fit**: Phân tích quy mô, ngành nghề, vai trò người ra quyết định.
     - 🔵 **Hành vi giao dịch (Mô hình RFM)**: Đánh giá Recency, Frequency, Monetary và phân hạng khách hàng.
     - 🟡 **Mức độ tương tác & Sắc thái**: Đánh giá phản hồi qua Email, Cuộc gọi, Support Ticket và chỉ số hài lòng NPS.
     - 🟢 **Chỉ số dự đoán & Vòng đời**: Ước tính CLV (Customer Lifetime Value), vị trí phễu bán hàng và thời điểm tối ưu để chốt hợp đồng.

---

### 3.2. Quản trị Dữ liệu trên Wagtail Admin Panel

1. Truy cập [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) và đăng nhập bằng tài khoản superuser đã tạo ở Bước 5.
2. Trên menu bên trái, tìm nhóm **"Quản lý CRM"**:
   - **Khách hàng**: Xem, thêm mới, lọc theo trạng thái (`Lead`, `Customer`, `Churned`) hoặc nguy cơ rời bỏ (`Churn Risk`). Khi bấm vào từng khách hàng, Wagtail hiển thị giao diện phân vùng chuyên nghiệp (`MultiFieldPanel`).
   - **Lịch sử tương tác**: Theo dõi toàn bộ lịch sử trao đổi đa kênh kèm nội dung tóm tắt (`content_preview`).
   - **Đơn hàng / Deal**: Quản lý mã đơn hàng, giá trị hợp đồng và các giai đoạn đàm phán (`Negotiation`, `Won`, `Lost`).

---

## 4. CHẠY KIỂM THỬ TỰ ĐỘNG (AUTOMATED TESTING)

Hệ thống đi kèm bộ kiểm thử tự động gồm **6 bài test** toàn diện sử dụng Mock Gemini API để kiểm tra độ tin cậy của mã nguồn:

```powershell
python manage.py test crm_core -v 2
```

Kết quả mong đợi:
```text
Ran 6 tests in 0.045s - OK
```

---

## 5. XỬ LÝ SỰ CỐ THƯỜNG GẶP (TROUBLESHOOTING)

| Vấn đề gặp phải | Nguyên nhân | Cách khắc phục |
| :--- | :--- | :--- |
| **Bấm Phân tích AI báo lỗi API kết nối** | Chưa cấu hình hoặc sai `GEMINI_API_KEY` trong file `.env`. | Mở file `.env`, kiểm tra lại key và đảm bảo không có dấu cách thừa. |
| **Port 8000 bị chiếm dụng** | Một ứng dụng khác đang chạy trên cổng 8000. | Chạy lệnh `python manage.py runserver 8080` để đổi sang cổng 8080. |
| **Lỗi `ModuleNotFoundError`** | Chưa kích hoạt môi trường ảo `venv` trước khi chạy. | Chạy lệnh `.\venv\Scripts\activate` rồi thử lại. |
