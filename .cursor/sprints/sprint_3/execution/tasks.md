# 📍 Các task kỹ thuật cho Sprint 3

## 🎯 Mục tiêu
Triển khai toàn bộ các story trong Epic 3: Hoàn thiện, Đóng gói và Tài liệu hóa.

## 📋 Các task cần làm (Implementation THẬT)

### Story 3.1: Xây dựng hệ thống test tự động
- [ ] `task`: Cài đặt `pytest` và `pytest-cov`.
- [ ] `task`: Viết unit test cho `pdf_processor.py`, `html_converter.py`, `image_optimizer.py`. Sử dụng file PDF mẫu nhỏ và mock các dependency nếu cần.
- [ ] `task`: Viết unit test cho các hàm tiện ích (ví dụ: hàm parse chuỗi `skip-pages`).
- [ ] `task`: Viết integration test cho luồng `main.py`, kiểm tra xem việc chạy lệnh với các tham số khác nhau có tạo ra file output đúng như mong đợi không.
- [ ] `task`: Cấu hình `pytest.ini` để tự động chạy test và tạo báo cáo độ bao phủ (coverage report).
- [ ] `task`: (Bonus) Thiết lập GitHub Actions workflow để tự động chạy test mỗi khi có push lên repository.

### Story 3.2: Hoàn thiện xử lý lỗi và logging
- [ ] `task`: Cài đặt thư viện `logging` của Python.
- [ ] `task`: Cấu hình logging trong `main.py` để ghi lại các thông tin quan trọng (ví dụ: file đang xử lý, các tham số) và các lỗi chi tiết vào một file log (ví dụ: `conversion.log`).
- [ ] `task`: Rà soát lại toàn bộ code, bọc các đoạn code có nguy cơ lỗi (I/O, xử lý file) trong các khối `try...except` cụ thể.
- [ ] `task`: Thay thế các lệnh `print` thông báo lỗi bằng các lời gọi `logging.error()` và hiển thị thông báo thân thiện cho người dùng. Ví dụ: thay vì traceback, hiển thị "Lỗi: File PDF 'abc.pdf' không tồn tại hoặc không thể đọc."

### Story 3.3: Đóng gói ứng dụng
- [ ] `task`: Tạo file `pyproject.toml` để định nghĩa thông tin project và các build dependency.
- [ ] `task`: Tạo file `setup.cfg` để chứa các metadata của package (tên, phiên bản, tác giả, mô tả, dependencies).
- [ ] `task`: Cấu hình `entry_points` trong `setup.cfg` để tạo ra một command-line script (ví dụ: `pdf2epub`) khi package được cài đặt.
- [ ] `task`: Build package bằng lệnh `python -m build`.
- [ ] `task`: Test cài đặt package cục bộ bằng lệnh `pip install dist/your-package-name.whl` và chạy thử lệnh `pdf2epub`.

### Story 3.4: Viết tài liệu hướng dẫn
- [ ] `task`: Tạo file `README.md` ở thư mục gốc.
- [ ] `task`: Viết phần giới thiệu về công cụ trong `README.md`.
- [ ] `task`: Viết hướng dẫn cài đặt chi tiết (cách tạo môi trường ảo, cài đặt bằng pip).
- [ ] `task`: Viết hướng dẫn sử dụng chi tiết, bao gồm tất cả các tham số dòng lệnh và các ví dụ cụ thể.
- [ ] `task`: Cập nhật `argparse` trong `main.py` để thêm các thông điệp trợ giúp (`help=...`) rõ ràng cho từng tham số.

## ✅ Tiêu chí hoàn thành (THỰC TẾ)
- [ ] Độ bao phủ của test đạt > 80%.
- [ ] Công cụ không bị crash khi gặp các lỗi phổ biến (file không tồn tại, file sai định dạng) và hiển thị thông báo lỗi rõ ràng.
- [ ] Có thể cài đặt công cụ qua `pip` và chạy bằng lệnh `pdf2epub` từ bất kỳ đâu trên terminal.
- [ ] File `README.md` đầy đủ, rõ ràng, giúp người dùng mới có thể tự cài đặt và sử dụng. 