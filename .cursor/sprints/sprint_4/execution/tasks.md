# 📍 Các Task Kỹ Thuật cho Sprint 4

---

## Story 4.1 & 5.1: Nâng cấp Bộ trích xuất PDF (Nền tảng)

**🎯 Mục tiêu:** Thay đổi `PDFProcessor` để trích xuất dữ liệu có cấu trúc (`dict`) thay vì HTML thô, bao gồm tọa độ, thông tin font chữ cho từng dòng, từng chữ.

-   [ ] **Refactor `pdf_processor.py`:**
    -   [ ] Thay đổi phương thức `extract_page_content` để sử dụng `page.get_text("dict")`.
    -   [ ] Phương thức mới sẽ trả về một cấu trúc dữ liệu phức tạp chứa các "blocks", "lines", và "spans" của văn bản.
    -   [ ] Đảm bảo việc trích xuất hình ảnh vẫn hoạt động như cũ.
-   [ ] **Cập nhật `html_converter.py`:**
    -   [ ] Tạm thời sửa `HTMLConverter` để có thể xử lý cấu trúc dữ liệu mới này theo cách đơn giản nhất (chỉ nối các chuỗi văn bản lại) để đảm bảo các tính năng hiện có không bị vỡ ngay lập tức. Đây là bước đệm trước khi tích hợp logic phân tích bố cục.

---

## Story 4.2 & 4.3: Implement Module Phân tích Bố cục (`LayoutAnalyzer`)

**🎯 Mục tiêu:** Xây dựng logic để nhận dạng cột và bảng từ dữ liệu có cấu trúc đã trích xuất.

-   [ ] **Tạo file `src/layout_analyzer.py`:**
    -   [ ] Tạo class `LayoutAnalyzer`.
-   [ ] **Implement thuật toán nhận dạng cột:**
    -   [ ] Viết phương thức `analyze_columns(page_blocks, page_width)`.
    -   [ ] Logic:
        1.  Phân loại các khối văn bản vào các "vùng" theo chiều ngang (ví dụ: nửa trái, nửa phải).
        2.  Sắp xếp lại các khối trong mỗi vùng theo chiều dọc (tọa độ `y`).
        3.  Nối các khối đã sắp xếp lại thành một luồng văn bản duy nhất.
-   [ ] **Implement thuật toán nhận dạng bảng (cơ bản):**
    -   [ ] Viết phương thức `analyze_tables(page_blocks)`.
    -   [ ] Logic sơ bộ: Tìm các khối văn bản được sắp xếp theo dạng lưới (cùng tọa độ `y` nhưng khác `x`, hoặc ngược lại). Đây là một heuristic đơn giản.
-   [ ] **Tích hợp vào `html_converter.py`:**
    -   [ ] Gọi `LayoutAnalyzer` trong `HTMLConverter`.
    -   [ ] Dựa vào kết quả phân tích, tái cấu trúc các khối văn bản thành HTML. Các khối được xác định là cột sẽ được sắp xếp lại. Các khối được xác định là bảng sẽ được bọc trong thẻ `<table>`.

---

## Story 5.2: Implement Module Nhận dạng Tiêu đề (`TOCGenerator`)

**🎯 Mục tiêu:** Xây dựng logic để tìm ra các tiêu đề trong văn bản dựa trên các quy tắc.

-   [ ] **Tạo file `src/toc_generator.py`:**
    -   [ ] Tạo class `TOCGenerator`.
-   [ ] **Implement Heuristics Engine:**
    -   [ ] Viết phương thức `detect_headings(page_blocks)`.
    -   [ ] Logic:
        1.  Tính toán kích thước font trung bình và phổ biến nhất trên trang.
        2.  Duyệt qua các `span` văn bản:
            -   Nếu `span` có kích thước font lớn hơn đáng kể so với trung bình (ví dụ: > 1.2x).
            -   Nếu `span` có font weight là `bold`.
            -   Nếu `span` khớp với các mẫu regex (ví dụ: `^Chương \d+`, `^\d+\.\d+ .*`, `^Phần [A-Z]`).
        3.  Gán cấp độ cho tiêu đề (ví dụ: font-size 24px là cấp 1, 18px là cấp 2).
    -   [ ] Phương thức sẽ trả về một danh sách các tiêu đề đã phát hiện, ví dụ: `[(level, title, page_number), ...]`.

---

## Story 5.3: Tích hợp TOC vào `EpubPackager`

**🎯 Mục tiêu:** Sử dụng danh sách tiêu đề đã nhận dạng để tạo mục lục cho file EPUB.

-   [ ] **Refactor `epub_packager.py`:**
    -   [ ] Sửa đổi phương thức `create_epub` để chấp nhận một tham số mới: `dynamic_toc`.
    -   [ ] Nếu `dynamic_toc` được cung cấp, xây dựng `book.toc` từ danh sách này.
    -   [ ] Logic này cần xử lý việc tạo ra các mục lục lồng nhau (nested) dựa trên `level` của tiêu đề.

---

## Tích hợp cuối cùng và Cập nhật `main.py`

**🎯 Mục tiêu:** Kết nối tất cả các thành phần mới và cung cấp tùy chọn cho người dùng.

-   [ ] **Cập nhật `main.py`:**
    -   [ ] Thêm các câu hỏi tương tác mới:
        -   `Bạn có muốn kích hoạt tính năng phân tích bố cục (cột, bảng)? (y/n):`
        -   `Bạn có muốn tự động tạo mục lục từ nội dung? (y/n):`
    -   [ ] Trong luồng xử lý chính, gọi `LayoutAnalyzer` và `TOCGenerator` nếu người dùng đã chọn.
    -   [ ] Truyền kết quả vào các module tiếp theo (`HTMLConverter`, `EpubPackager`).
-   [ ] **Kiểm thử tích hợp:**
    -   [ ] Chạy toàn bộ quy trình với một file PDF 2 cột.
    -   [ ] Chạy toàn bộ quy trình với một file PDF có tiêu đề rõ ràng.
    -   [ ] Kiểm tra file EPUB đầu ra để xác nhận thứ tự nội dung và mục lục được tạo ra là chính xác. 