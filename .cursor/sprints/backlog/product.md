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

# Epic 4: Phân tích và Tái tạo Bố cục Nâng cao

## Giá trị kinh doanh THỰC TẾ
- **Vấn đề giải quyết:** Các tài liệu PDF học thuật, báo cáo, tạp chí thường có bố cục nhiều cột và bảng biểu. Việc chuyển đổi thông thường sẽ làm xáo trộn hoàn toàn thứ tự đọc, khiến nội dung trở nên vô nghĩa.
- **Tác động tới user:** Cho phép người dùng đọc các tài liệu có bố cục phức tạp một cách tự nhiên và đúng trình tự trên thiết bị đọc sách.
- **Chỉ số thành công:** Chuyển đổi thành công và giữ đúng thứ tự đọc cho ít nhất 80% các tài liệu có bố cục 2 cột. Chuyển đổi đúng cấu trúc cho 70% các bảng biểu đơn giản.

## Phạm vi kỹ thuật (KHÔNG MOCK)
- **Components thật cần xây dựng:**
    - Module `LayoutAnalyzer`: Phân tích các khối văn bản (`blocks`) từ `PyMuPDF` dựa trên tọa độ (x, y) để xác định các cột và bảng.
    - Logic tái cấu trúc HTML: Sắp xếp lại các khối văn bản theo đúng thứ tự đọc và bọc chúng trong các thẻ `<div>` hoặc `<table>` thích hợp.
- **Integration points thực tế:** `LayoutAnalyzer` sẽ được tích hợp vào giữa `PDFProcessor` và `HTMLConverter`. `PDFProcessor` cần được nâng cấp để trích xuất dữ liệu có kèm tọa độ (`get_text("dict")`).
- **Performance requirements cụ thể:** Quá trình phân tích không làm tăng thời gian chuyển đổi tổng thể quá 50% đối với các file có cấu trúc phức tạp.

## Stories breakdown (MỖI STORY PHẢI THẬT)
1. **Story 4.1:** Nâng cấp bộ trích xuất PDF để lấy dữ liệu có metadata về vị trí.
2. **Story 4.2:** Implement thuật toán nhận dạng và sắp xếp lại nội dung theo cột.
3. **Story 4.3:** Implement thuật toán nhận dạng và chuyển đổi bảng biểu đơn giản sang thẻ `<table>` HTML.

# Epic 5: Tự động Tạo Mục lục (TOC) từ Nội dung

## Giá trị kinh doanh THỰC TẾ
- **Vấn đề giải quyết:** Các file PDF dài nhưng không có mục lục (bookmark) sẵn khiến việc điều hướng vô cùng khó khăn.
- **Tác động tới user:** Cung cấp một mục lục (TOC) có thể điều hướng được trong file EPUB, giúp người dùng dễ dàng chuyển đến các chương, mục mà họ quan tâm.
- **Chỉ số thành công:** Tự động tạo ra mục lục hợp lệ cho >90% các tài liệu có cấu trúc tiêu đề rõ ràng (ví dụ: "Chương 1", "1.1 Giới thiệu").

## Phạm vi kỹ thuật (KHÔNG MOCK)
- **Components thật cần xây dựng:**
    - Module `TOCGenerator`: Phân tích các thuộc tính của văn bản (kích thước font, độ đậm, kiểu chữ) và nội dung (các mẫu regex như "Chương X", "Phần Y") để xác định các tiêu đề.
    - Logic tạo cấu trúc TOC phân cấp: Xây dựng một cây mục lục dựa trên các cấp độ tiêu đề đã nhận dạng.
- **Integration points thực tế:** `PDFProcessor` cần trích xuất thêm thông tin về font. `TOCGenerator` sẽ được gọi trong `main.py` và kết quả của nó sẽ được truyền vào `EpubPackager`.
- **Performance requirements cụ thể:** Tốc độ quét tiêu đề không ảnh hưởng đáng kể đến thời gian xử lý chung.

## Stories breakdown (MỖI STORY PHẢI THẬT)
1. **Story 5.1:** Nâng cấp bộ trích xuất PDF để lấy metadata về font chữ.
2. **Story 5.2:** Implement bộ quy tắc (heuristic-based engine) để nhận dạng tiêu đề.
3. **Story 5.3:** Tích hợp cấu trúc TOC đã nhận dạng vào file EPUB. 