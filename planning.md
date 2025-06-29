# 🎯 Sprint 1: Xây dựng nền tảng và chức năng chuyển đổi cốt lõi

## 📅 Thời gian
- Bắt đầu: Ngay sau khi kế hoạch được duyệt
- Ước tính hoàn thành: 5 ngày làm việc

## 🎯 Mục tiêu Sprint
1.  Thiết lập cấu trúc project Python hoàn chỉnh, sẵn sàng cho việc phát triển và mở rộng.
2.  Implement chức năng cốt lõi: chuyển đổi một file PDF đầu vào thành một file EPUB 3.0 hợp lệ.
3.  Đảm bảo file EPUB 3.0 tạo ra có cấu trúc đúng chuẩn, bao gồm nội dung (HTML cho mỗi trang), mục lục (TOC), và file điều hướng (navigation).
4.  Xây dựng giao diện dòng lệnh (CLI) cơ bản để thực thi việc chuyển đổi.

## 📊 Phân chia công việc
| Bước | Mô tả chi tiết (Implementation THẬT) | Độ ưu tiên | Ước tính (giờ) | Trạng thái |
| :--- | :--- | :--- | :--- | :--- |
| 1 | **Thiết lập môi trường và cấu trúc project** <br/>- Tạo virtual environment (`venv`) <br/>- Cấu trúc thư mục `src`, `tests`, `output` <br/>- Khởi tạo `git` và file `.gitignore` <br/>- Tạo file `requirements.txt` | 🔴 Cao | 2 | ⬜ |
| 2 | **Implement Module đọc và phân tích PDF** <br/>- Sử dụng `PyMuPDF` <br/>- Tạo lớp `PDFProcessor` <br/>- Implement phương thức đọc file PDF, trích xuất văn bản và hình ảnh từ từng trang. | 🔴 Cao | 8 | ⬜ |
| 3 | **Implement Module chuyển đổi sang HTML** <br/>- Tạo lớp `HTMLConverter` <br/>- Implement phương thức nhận dữ liệu (văn bản, ảnh) của một trang và tạo ra một file HTML tương ứng. <br/>- Lưu ảnh vào thư mục riêng và nhúng vào HTML. | 🔴 Cao | 8 | ⬜ |
| 4 | **Implement Module đóng gói EPUB 3.0** <br/>- Sử dụng `EbookLib` <br/>- Tạo lớp `EpubPackager` <br/>- Implement phương thức nhận các file HTML đã tạo, tạo file `content.opf`, `toc.ncx`, và `nav.xhtml` (chuẩn EPUB 3). <br/>- Đóng gói tất cả thành một file `.epub` duy nhất. | 🔴 Cao | 10 | ⬜ |
| 5 | **Xây dựng giao diện dòng lệnh (CLI) cơ bản** <br/>- Sử dụng `argparse` <br/>- Tạo file `main.py` <br/>- CLI chấp nhận 2 tham số: `input_file` (đường dẫn PDF) và `output_file` (đường dẫn EPUB). | 🟡 Trung bình | 4 | ⬜ |
| 6 | **Tích hợp và kiểm thử End-to-End** <br/>- Viết script để kiểm tra luồng hoạt động từ PDF -> EPUB với một file PDF mẫu. <br/>- Xác thực file EPUB output bằng công cụ `epubcheck`. | 🟡 Trung bình | 4 | ⬜ |


## 📦 Dependencies cần cài đặt
- `PyMuPDF` - Để đọc và trích xuất nội dung từ file PDF một cách hiệu quả và chính xác.
- `EbookLib` - Để tạo và quản lý cấu trúc file EPUB 3.0 theo đúng tiêu chuẩn.
- `Pillow` - Để xử lý và tối ưu hóa hình ảnh được trích xuất từ PDF.

## 🔧 Lệnh cần chạy
```bash
# 1. Thiết lập môi trường ảo
python -m venv venv
source venv/bin/activate  # Trên Linux/macOS
# venv\Scripts\activate  # Trên Windows

# 2. Cài đặt các thư viện cần thiết từ file requirements.txt
pip install -r requirements.txt

# 3. Chạy công cụ (sau khi hoàn thành)
python src/main.py path/to/your/document.pdf path/to/your/output.epub
```

## ⚠️ Nguyên tắc implementation
- ✅ **PHẢI** xây dựng logic xử lý thật, không hardcode hay giả lập cho bất kỳ định dạng PDF nào.
- ✅ **PHẢI** xử lý lỗi (ví dụ: file không tồn tại, file không phải PDF) một cách tường minh.
- ✅ **PHẢI** tạo ra file EPUB 3.0 hợp lệ, có thể được xác thực bằng các công cụ chuẩn.
- ❌ **KHÔNG** dùng mock data hay các thư viện giả lập.
- ❌ **KHÔNG** làm phiên bản đơn giản hóa (simplified version) cho việc trích xuất nội dung. Phải xử lý cả văn bản và hình ảnh.

## 🚨 Rủi ro và giải pháp
| Rủi ro | Mức độ | Giải pháp thực tế |
| :--- | :--- | :--- |
| **Bố cục PDF phức tạp** (nhiều cột, bảng biểu) làm cho việc trích xuất văn bản bị sai thứ tự. | Cao | - **Giải pháp:** Sử dụng các phương thức trích xuất nâng cao của `PyMuPDF` (ví dụ: `get_text("blocks")` thay vì `get_text()`) để giữ lại thông tin về vị trí các khối văn bản. <br/>- Chấp nhận rằng việc giữ lại 100% bố cục gốc là một bài toán cực kỳ phức tạp và sẽ được cải tiến trong các Sprint sau. Sprint 1 tập trung vào việc lấy đúng nội dung. |
| **File EPUB không hợp lệ (invalid)** do cấu trúc sai hoặc thiếu metadata. | Trung bình | - **Giải pháp:** Tuân thủ chặt chẽ tài liệu của `EbookLib` cho việc tạo EPUB 3. <br/>- Tự động chạy công cụ `epubcheck.jar` (một công cụ tiêu chuẩn của ngành) trong quy trình kiểm thử để đảm bảo tính hợp lệ của file đầu ra. |
| **Hiệu năng kém** với các file PDF lớn (>500 trang). | Thấp | - **Giải pháp:** Trong Sprint 1, tập trung vào tính đúng đắn. Các vấn đề về hiệu năng sẽ được đo lường và tối ưu hóa trong một Sprint riêng nếu cần. Thiết kế code theo module (Processor, Converter, Packager) sẽ giúp dễ dàng tối ưu từng phần sau này. |

## 📝 Ghi chú
- Kế hoạch cho các tính năng nâng cao (bỏ qua trang, xóa từ khóa, tối ưu hóa) sẽ được xây dựng trong **planning_sprint_2.md**.
- Cần chuẩn bị một bộ các file PDF mẫu (từ đơn giản đến phức tạp) để phục vụ cho việc phát triển và kiểm thử. 