# 🎯 Sprint 4: Phân tích Bố cục và Mục lục Thông minh

## 📅 Thời gian
- Bắt đầu: [dd/mm/yyyy]
- Kết thúc dự kiến: [dd/mm/yyyy]

## 🎯 Mục tiêu Sprint
1.  **Nâng cấp Nền tảng Trích xuất Dữ liệu:** Refactor module `PDFProcessor` để trích xuất dữ liệu văn bản kèm theo metadata chi tiết về vị trí (tọa độ khối) và định dạng (font, size, weight). Đây là nền tảng bắt buộc cho cả hai tính năng lớn.
2.  **Triển khai Phiên bản Đầu tiên của Nhận dạng Cột:** Xây dựng và tích hợp một thuật toán có khả năng nhận diện và sắp xếp lại chính xác nội dung cho các tài liệu có bố cục 2 cột đơn giản.
3.  **Triển khai Hệ thống Nhận dạng Tiêu đề dựa trên Heuristic:** Xây dựng một bộ quy tắc (rule-based engine) để tự động phát hiện các tiêu đề chương, mục dựa trên các thuộc tính của font và các mẫu văn bản phổ biến.
4.  **Tạo Mục lục Động:** Tích hợp các tiêu đề đã được nhận dạng vào `EpubPackager` để tạo ra một mục lục (Table of Contents) phân cấp, có thể điều hướng được.

## 📊 Phân chia công việc
| Epic | Story | Độ ưu tiên | Ước tính (SP) |
|------|-------|------------|----------|
| Bố cục Nâng cao | Nâng cấp bộ trích xuất (vị trí & font) | 🔴 Cao | 8 |
| Bố cục Nâng cao | Implement nhận dạng cột | 🔴 Cao | 8 |
| Bố cục Nâng cao | Implement nhận dạng bảng (cơ bản) | 🟡 TB | 5 |
| Mục lục Thông minh | Implement nhận dạng tiêu đề | 🔴 Cao | 8 |
| Mục lục Thông minh | Tích hợp TOC vào EPUB | 🟡 TB | 5 |

## ⚠️ Nguyên tắc implementation
- ✅ **PHẢI** sử dụng phương thức `get_text("dict")` của `PyMuPDF` làm nền tảng.
- ✅ **PHẢI** xây dựng các module `LayoutAnalyzer` và `TOCGenerator` riêng biệt, dễ dàng kiểm thử và thay thế.
- ✅ **PHẢI** ghi log chi tiết quá trình phân tích (ví dụ: "Phát hiện 2 cột ở trang 5", "Dòng 'ABC' được xác định là tiêu đề cấp 1").
- ❌ **KHÔNG** cố gắng giải quyết mọi trường hợp bố cục phức tạp. Tập trung vào các trường hợp phổ biến trước.
- ❌ **KHÔNG** sử dụng các giải pháp OCR bên ngoài. Tận dụng tối đa khả năng của `PyMuPDF`.

## 🚨 Rủi ro và giải pháp
| Rủi ro | Mức độ | Giải pháp thực tế |
|--------|--------|-------------------|
| **Sự đa dạng của bố cục PDF là vô hạn:** Thuật toán nhận dạng cột và bảng có thể thất bại trên nhiều tài liệu không theo chuẩn. | Cao | - **Giải pháp:** Chấp nhận đây là một bài toán heuristic. Tập trung vào các bố cục phổ biến (báo cáo 2 cột, bảng dữ liệu đơn giản). Cung cấp một tùy chọn trong `main.py` để bật/tắt tính năng phân tích bố cục (`--analyze-layout`), mặc định có thể tắt để đảm bảo sự ổn định. |
| **Nhận dạng tiêu đề không chính xác:** Heuristics có thể nhận dạng sai (false positive) hoặc bỏ sót (false negative) các tiêu đề. | Cao | - **Giải pháp:** Xây dựng một hệ thống heuristic linh hoạt. Cho phép người dùng tinh chỉnh các ngưỡng (ví dụ: tỉ lệ kích thước font, các từ khóa trong tiêu đề) trong tương lai. Ở sprint này, ghi log rõ ràng các tiêu đề đã nhận dạng và thuộc tính của chúng để dễ dàng gỡ lỗi và cải tiến. |
| **Tái cấu trúc (Refactoring) lớn:** Việc thay đổi cách `PDFProcessor` trả về dữ liệu sẽ ảnh hưởng đến toàn bộ luồng xử lý. | Trung bình | - **Giải pháp:** Lập kế hoạch refactor cẩn thận. Viết lại các unit test cho các module bị ảnh hưởng để đảm bảo không có lỗi hồi quy (regression bug). Quá trình này đã được tính đến trong ước tính Story Point. | 