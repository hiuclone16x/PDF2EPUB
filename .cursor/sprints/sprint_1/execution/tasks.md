# 📍 Các task kỹ thuật cho Sprint 1

## 🎯 Mục tiêu
Triển khai toàn bộ các story trong Epic 1: Xây dựng Lõi Chuyển đổi PDF sang EPUB.

## 📋 Các task cần làm (Implementation THẬT)

### Story 1.1: Thiết lập môi trường và cấu trúc dự án
- [ ] `task`: Tạo thư mục project `PDF2Epub`.
- [ ] `task`: Chạy `git init` để khởi tạo repository.
- [ ] `task`: Tạo file `.gitignore` chuẩn cho Python.
- [ ] `task`: Chạy `python -m venv venv` để tạo môi trường ảo.
- [ ] `task`: Tạo các thư mục `src`, `output`, `tests`, `docs`.
- [ ] `task`: Tạo file `requirements.txt` và thêm `PyMuPDF`, `EbookLib`, `Pillow`.

### Story 1.2 & 1.3: Đọc PDF và chuyển đổi sang HTML
- [ ] `task`: Tạo file `src/pdf_processor.py`.
- [ ] `task`: Implement lớp `PDFProcessor` với phương thức `__init__(self, pdf_path)`.
- [ ] `task`: Implement phương thức `extract_content_by_page(self)` sử dụng `PyMuPDF` để trích xuất văn bản và hình ảnh cho từng trang. Phương thức này phải trả về một cấu trúc dữ liệu rõ ràng, ví dụ `list[dict]`, mỗi dict chứa `page_number`, `text`, và `images`.
- [ ] `task`: Tạo file `src/html_converter.py`.
- [ ] `task`: Implement lớp `HTMLConverter`.
- [ ] `task`: Implement phương thức `create_html_from_page(self, page_data, output_dir)` để tạo file HTML từ dữ liệu của một trang.
    - [ ] `subtask`: Lưu các file ảnh vào thư mục con (ví dụ `output_dir/images`).
    - [ ] `subtask`: Nhúng văn bản và các thẻ `<img>` với đường dẫn tương đối vào file HTML.

### Story 1.4: Đóng gói thành file EPUB 3.0
- [ ] `task`: Tạo file `src/epub_packager.py`.
- [ ] `task`: Implement lớp `EpubPackager` với phương thức `__init__(self, book_title)`.
- [ ] `task`: Implement phương thức `create_epub(self, html_files, image_dir, output_path)` sử dụng `EbookLib`.
    - [ ] `subtask`: Thiết lập metadata cơ bản cho sách (title, language, identifier).
    - [ ] `subtask`: Tạo các `EpubHtml` item cho mỗi file HTML.
    - [ ] `subtask`: Tạo mục lục (`toc`) và cấu trúc điều hướng (`nav`) từ danh sách các file HTML.
    - [ ] `subtask`: Đóng gói tất cả thành file `.epub`.

### Story 1.5: Tích hợp và xây dựng CLI
- [ ] `task`: Tạo file `src/main.py`.
- [ ] `task`: Sử dụng `argparse` để thiết lập CLI chấp nhận 2 tham số bắt buộc: `input_file` và `output_file`.
- [ ] `task`: Viết hàm `main()` để điều phối toàn bộ quy trình:
    1. Khởi tạo `PDFProcessor`.
    2. Gọi `extract_content_by_page()`.
    3. Khởi tạo `HTMLConverter`.
    4. Lặp qua từng trang, gọi `create_html_from_page()` và lưu vào một thư mục tạm.
    5. Khởi tạo `EpubPackager`.
    6. Gọi `create_epub()` để đóng gói kết quả.
    7. Xóa thư mục tạm sau khi hoàn thành.
- [ ] `task`: Thêm xử lý lỗi cơ bản (ví dụ: `try...except FileNotFoundError`).

## ✅ Tiêu chí hoàn thành (THỰC TẾ)
- [ ] Tất cả các task được đánh dấu hoàn thành.
- [ ] Chạy lệnh `python src/main.py sample.pdf output.epub` thành công.
- [ ] File `output.epub` được tạo ra, có thể mở được trên một trình đọc EPUB (ví dụ Calibre).
- [ ] File `output.epub` vượt qua kiểm tra của `epubcheck` mà không có lỗi nghiêm trọng. 