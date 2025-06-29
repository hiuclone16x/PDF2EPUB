# PDF2Epub Converter

Một công cụ dòng lệnh mạnh mẽ, được xây dựng bằng Python, để chuyển đổi các tài liệu PDF sang định dạng EPUB 3.0. Công cụ này không chỉ thực hiện chuyển đổi cơ bản mà còn cung cấp nhiều tùy chọn nâng cao để tùy chỉnh file EPUB đầu ra theo ý muốn của bạn.

## 🌟 Tính năng chính

- **Chuyển đổi PDF sang EPUB 3.0:** Chuyển đổi mỗi trang PDF thành một file XHTML, bảo toàn văn bản và hình ảnh.
- **Bỏ qua trang:** Dễ dàng loại bỏ các trang không mong muốn (ví dụ: trang bìa, quảng cáo, trang trắng) khỏi file EPUB cuối cùng.
- **Loại bỏ từ khóa:** Tự động tìm và xóa các từ hoặc cụm từ không cần thiết (ví dụ: "Bản quyền", "Bản nháp") khỏi nội dung sách.
- **Tối ưu hóa hình ảnh:** Tự động thay đổi kích thước và nén hình ảnh để giảm đáng kể dung lượng file EPUB, giúp tải nhanh hơn và tiết kiệm không gian lưu trữ trên các thiết bị đọc sách.
- **Giao diện dòng lệnh (CLI):** Cung cấp một giao diện trực quan và dễ sử dụng qua terminal.

## 🚀 Cài đặt

Dự án này sử dụng Python 3.8+ và được quản lý bằng môi trường ảo.

**Bước 1: Clone repository (nếu có)**
```bash
git clone https://github.com/user/repo.git # Thay thế bằng URL repo thực tế
cd PDF2Epub
```

**Bước 2: Tạo và kích hoạt môi trường ảo**
```bash
# Tạo môi trường ảo
python -m venv venv

# Kích hoạt trên Windows
venv\Scripts\activate

# Kích hoạt trên macOS/Linux
source venv/bin/activate
```

**Bước 3: Cài đặt các gói cần thiết**
Cách 1: Cài đặt các thư viện trực tiếp để phát triển.
```bash
pip install -r requirements.txt
```
Cách 2: Build và cài đặt công cụ như một package hoàn chỉnh.
```bash
# Cài đặt build tool
pip install build

# Build package
python -m build

# Cài đặt file .whl vừa được tạo trong thư mục dist/
pip install dist/*.whl
```

##  kullanım

Sau khi cài đặt, bạn có thể sử dụng công cụ thông qua lệnh `pdf2epub` (nếu cài đặt như package) hoặc `python src/main.py` (nếu chạy từ mã nguồn).

### Cú pháp cơ bản

```bash
pdf2epub [input_file.pdf] [output_file.epub] [OPTIONS]
```

### Ví dụ

**1. Chuyển đổi cơ bản:**
```bash
pdf2epub "tai-lieu-cua-toi.pdf" "sach-cua-toi.epub"
```

**2. Chuyển đổi với các tùy chọn nâng cao:**
```bash
pdf2epub "report.pdf" "optimized-report.epub" \
--skip-pages "1,10-12" \
--remove-keywords "Confidential" "Draft" "Internal" \
--image-quality 75 \
--image-max-width 800
```

### 📖 Tất cả các tùy chọn

| Tùy chọn                  | Viết tắt | Mô tả                                                                                                        | Mặc định     |
| -------------------------- | -------- | ------------------------------------------------------------------------------------------------------------ | ------------ |
| `input_file`               |          | **(Bắt buộc)** Đường dẫn đến file PDF đầu vào.                                                              | -            |
| `output_file`              |          | **(Bắt buộc)** Đường dẫn để lưu file EPUB đầu ra.                                                             | -            |
| `--skip-pages "..."`       |          | Chuỗi các trang hoặc khoảng trang cần bỏ qua (ví dụ: `"1,5,8-12"`).                                          | ""           |
| `--remove-keywords "..."`  |          | Danh sách các từ khóa cần xóa, đặt trong dấu ngoặc kép và cách nhau bởi dấu cách.                             | []           |
| `--image-quality N`        |          | Chất lượng ảnh JPEG sau khi nén (1-100).                                                                     | 85           |
| `--image-max-width N`      |          | Chiều rộng tối đa của ảnh (tính bằng pixel).                                                                  | 1024         |
| `--no-image-optimization`  |          | Tắt hoàn toàn tính năng tối ưu hóa hình ảnh.                                                                 | Tắt (False)  |
| `--help`                   | `-h`     | Hiển thị màn hình trợ giúp này.                                                                              | -            |

## 📝 TODOs cho tương lai

- [ ] Cải thiện việc nhận dạng và giữ lại cấu trúc cột, bảng biểu.
- [ ] Tự động nhận dạng tiêu đề để tạo mục lục (TOC) thông minh hơn.
- [ ] Hỗ trợ các định dạng input khác (ví dụ: DOCX, TXT).
- [ ] Tạo giao diện đồ họa (GUI) đơn giản. 