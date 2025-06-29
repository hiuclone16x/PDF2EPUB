# Epic 1: Xây dựng Lõi Chuyển đổi PDF sang EPUB

## Giá trị kinh doanh THỰC TẾ
- **Vấn đề giải quyết:** Người dùng cần một công cụ đáng tin cậy để chuyển đổi tài liệu PDF sang định dạng EPUB 3.0 có thể đọc được trên nhiều thiết bị e-reader.
- **Tác động tới user:** Cho phép người dùng đọc tài liệu PDF trên các thiết bị chuyên dụng, cải thiện trải nghiệm đọc (tùy chỉnh font, kích thước chữ).
- **Chỉ số thành công:** Công cụ có khả năng chuyển đổi thành công 95% các file PDF có cấu trúc đơn giản đến trung bình thành file EPUB 3.0 hợp lệ.

## Phạm vi kỹ thuật (KHÔNG MOCK)
- **Components thật cần xây dựng:**
    - `PDFProcessor`: Module đọc và trích xuất dữ liệu từ PDF.
    - `HTMLConverter`: Module chuyển đổi dữ liệu trang thành file HTML.
    - `EpubPackager`: Module đóng gói các tài nguyên thành file EPUB 3.0.
    - `CLI`: Giao diện dòng lệnh để người dùng tương tác.
- **Integration points thực tế:** Tích hợp giữa các module nội bộ.
- **Performance requirements cụ thể:** Xử lý file PDF 100 trang trong dưới 60 giây.
- **Security considerations đầy đủ:** Đảm bảo không có lỗ hổng thực thi mã từ xa khi xử lý file PDF (sử dụng thư viện uy tín).

## Stories breakdown (MỖI STORY PHẢI THẬT)
1. **Story 1.1:** Thiết lập môi trường và cấu trúc dự án.
2. **Story 1.2:** Implement chức năng đọc PDF và trích xuất nội dung.
3. **Story 1.3:** Implement chức năng chuyển đổi nội dung trang sang HTML.
4. **Story 1.4:** Implement chức năng đóng gói thành file EPUB 3.0 hoàn chỉnh.
5. **Story 1.5:** Tích hợp thành một luồng hoàn chỉnh qua giao diện CLI.

# Epic 2: Nâng cao Trải nghiệm và Tùy chỉnh

## Giá trị kinh doanh THỰC TẾ
- **Vấn đề giải quyết:** Người dùng muốn có quyền kiểm soát nhiều hơn đối với nội dung của file EPUB cuối cùng, loại bỏ những phần không mong muốn và tối ưu hóa kích thước file.
- **Tác động tới user:** Tạo ra các file EPUB gọn nhẹ hơn, sạch sẽ hơn và phù hợp hơn với nhu cầu cá nhân.
- **Chỉ số thành công:** Giảm ít nhất 20% kích thước file EPUB đối với các tài liệu có nhiều hình ảnh. Cho phép người dùng tùy chỉnh thành công 100% các yêu cầu về bỏ trang và xóa từ khóa.

## Phạm vi kỹ thuật (KHÔNG MOCK)
- **Components thật cần xây dựng:**
    - Mở rộng `CLI` để chấp nhận các tham số `--skip-pages` và `--remove-keywords`.
    - Thêm logic vào `PDFProcessor` để lọc các trang không cần thiết.
    - Thêm logic vào `HTMLConverter` để tìm và thay thế từ khóa.
    - Tích hợp thư viện `Pillow` vào luồng xử lý ảnh để nén và thay đổi kích thước.
- **Integration points thực tế:** Tích hợp `Pillow` vào `PDFProcessor` hoặc `HTMLConverter`.
- **Performance requirements cụ thể:** Các tùy chọn tùy chỉnh không làm tăng thời gian xử lý quá 20%.

## Stories breakdown (MỖI STORY PHẢI THẬT)
1. **Story 2.1:** Bỏ qua các trang được chỉ định trong quá trình chuyển đổi.
2. **Story 2.2:** Tìm và loại bỏ các từ khóa được chỉ định khỏi nội dung văn bản.
3. **Story 2.3:** Tối ưu hóa hình ảnh để giảm kích thước file EPUB.

# Epic 3: Hoàn thiện, Đóng gói và Tài liệu hóa

## Giá trị kinh doanh THỰC TẾ
- **Vấn đề giải quyết:** Cung cấp một công cụ mạnh mẽ, ổn định, dễ cài đặt và dễ sử dụng cho người dùng cuối.
- **Tác động tới user:** Tăng sự tin tưởng vào công cụ, giảm thiểu các lỗi gặp phải và cung cấp hướng dẫn rõ ràng khi có sự cố.
- **Chỉ số thành công:** Tỷ lệ lỗi dưới 1% khi chạy trên bộ test case. Độ bao phủ của test đạt trên 80%. Người dùng có thể cài đặt công cụ bằng một lệnh duy nhất.

## Phạm vi kỹ thuật (KHÔNG MOCK)
- **Components thật cần xây dựng:**
    - Bộ test cases hoàn chỉnh (`unittest`/`pytest`).
    - Hệ thống xử lý lỗi và logging chi tiết.
    - File `setup.py` hoặc `pyproject.toml` để đóng gói thành một package có thể cài đặt qua `pip`.
    - Tài liệu hướng dẫn sử dụng (`README.md`) và trợ giúp dòng lệnh (`--help`).
- **Integration points thực tế:** CI pipeline (e.g., GitHub Actions) để tự động chạy test và `epubcheck`.
- **Performance requirements cụ thể:** Tối ưu hóa các điểm nghẽn cổ chai đã xác định.
- **Security considerations đầy đủ:** Quét các lỗ hổng bảo mật trong các thư viện phụ thuộc.

## Stories breakdown (MỖI STORY PHẢI THẬT)
1. **Story 3.1:** Xây dựng hệ thống test tự động (unit & integration).
2. **Story 3.2:** Hoàn thiện hệ thống xử lý lỗi và logging.
3. **Story 3.3:** Đóng gói ứng dụng để có thể cài đặt dễ dàng.
4. **Story 3.4:** Viết tài liệu hướng dẫn đầy đủ cho người dùng. 