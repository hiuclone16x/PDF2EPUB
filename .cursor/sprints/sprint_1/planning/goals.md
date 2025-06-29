# 🎯 Sprint 1: Nền tảng Chuyển đổi Cốt lõi

## 📅 Thời gian
- Bắt đầu: [dd/mm/yyyy]
- Kết thúc dự kiến: [dd/mm/yyyy]

## 🎯 Mục tiêu Sprint
1. **Thiết lập nền tảng vững chắc:** Xây dựng cấu trúc project Python chuyên nghiệp, sẵn sàng cho việc mở rộng và bảo trì trong tương lai.
2. **Implement chức năng chuyển đổi cốt lõi:** Chuyển đổi thành công một file PDF đơn giản thành một file EPUB 3.0 hợp lệ về mặt kỹ thuật.
3. **Đảm bảo tính toàn vẹn của EPUB:** File EPUB được tạo ra phải có cấu trúc đúng chuẩn, bao gồm nội dung HTML cho mỗi trang, file mục lục (`toc.ncx`) và file điều hướng (`nav.xhtml`).

## 📊 Phân chia công việc
| Epic | Story | Độ ưu tiên | Ước tính (SP) |
|------|-------|------------|----------|
| Lõi Chuyển đổi | Thiết lập Project & Môi trường | 🔴 Cao | 2 |
| Lõi Chuyển đổi | Đọc và Phân tích PDF | 🔴 Cao | 5 |
| Lõi Chuyển đổi | Chuyển đổi trang PDF sang HTML | 🔴 Cao | 5 |
| Lõi Chuyển đổi | Đóng gói thành file EPUB 3.0 | 🔴 Cao | 8 |
| Lõi Chuyển đổi | Xây dựng CLI cơ bản | 🟡 TB | 3 |

## ⚠️ Nguyên tắc implementation
- ✅ **PHẢI** dùng các thư viện thực tế (`PyMuPDF`, `EbookLib`).
- ✅ **PHẢI** có xử lý lỗi cơ bản cho luồng chính.
- ✅ **PHẢI** tạo ra file EPUB có thể được xác thực bằng `epubcheck`.
- ❌ **KHÔNG** dùng mock data, không giả lập bất kỳ tiến trình nào.
- ❌ **KHÔNG** làm simplified version, logic trích xuất phải xử lý cả text và ảnh.

## 🚨 Rủi ro và giải pháp
| Rủi ro | Mức độ | Giải pháp thực tế |
|--------|--------|-------------------|
| Bố cục PDF phức tạp gây sai lệch nội dung | Cao | Sử dụng `PyMuPDF` với `get_text("blocks")` để giữ lại ngữ cảnh vị trí. Chấp nhận rằng bố cục hoàn hảo 100% là mục tiêu cho các sprint sau. |
| File EPUB không hợp lệ (invalid) | Trung bình | Dùng `epubcheck` (công cụ chuẩn) để kiểm tra thủ công trong sprint này nhằm đảm bảo tuân thủ chuẩn. | 