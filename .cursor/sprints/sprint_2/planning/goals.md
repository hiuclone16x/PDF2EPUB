# 🎯 Sprint 2: Tùy chọn Nâng cao và Tối ưu hóa

## 📅 Thời gian
- Bắt đầu: [dd/mm/yyyy]
- Kết thúc dự kiến: [dd/mm/yyyy]

## 🎯 Mục tiêu Sprint
1. **Nâng cao khả năng tùy chỉnh:** Cung cấp cho người dùng khả năng loại bỏ các trang không mong muốn và các từ khóa cụ thể khỏi nội dung sách.
2. **Tối ưu hóa tài nguyên:** Implement chức năng tối ưu hóa hình ảnh (nén và thay đổi kích thước) để giảm đáng kể dung lượng file EPUB cuối cùng.
3. **Mở rộng giao diện CLI:** Cập nhật giao diện dòng lệnh để hỗ trợ các tùy chọn cấu hình mới một cách linh hoạt.

## 📊 Phân chia công việc
| Epic | Story | Độ ưu tiên | Ước tính (SP) |
|------|-------|------------|----------|
| Nâng cao & Tùy chỉnh | Bỏ qua các trang được chỉ định | 🔴 Cao | 5 |
| Nâng cao & Tùy chỉnh | Tìm và loại bỏ từ khóa | 🟡 TB | 5 |
| Nâng cao & Tùy chỉnh | Tối ưu hóa hình ảnh | 🔴 Cao | 8 |

## ⚠️ Nguyên tắc implementation
- ✅ **PHẢI** tích hợp thư viện `Pillow` để xử lý ảnh một cách thực tế.
- ✅ **PHẢI** viết logic tìm kiếm và thay thế từ khóa hiệu quả, không ảnh hưởng nhiều đến hiệu năng.
- ✅ **PHẢI** giữ cho các tùy chọn mới dễ sử dụng thông qua CLI.
- ❌ **KHÔNG** làm ảnh hưởng đến các chức năng cốt lõi đã xây dựng ở Sprint 1.

## 🚨 Rủi ro và giải pháp
| Rủi ro | Mức độ | Giải pháp thực tế |
|--------|--------|-------------------|
| Việc xử lý ảnh làm tăng đáng kể thời gian chuyển đổi. | Cao | - **Giải pháp:** Cung cấp các tùy chọn tối ưu hóa (ví dụ: `--optimization-level high/medium/low`). <br/> - Chạy xử lý song song (nếu có thể) cho các tác vụ xử lý ảnh. Đo lường và benchmark cụ thể để tìm ra điểm nghẽn. |
| Việc xóa từ khóa có thể phá vỡ cấu trúc HTML (nếu từ khóa nằm trong tag HTML). | Trung bình | - **Giải pháp:** Chỉ thực hiện việc tìm và thay thế trên nội dung văn bản (text content) của các thẻ HTML, không phải trên toàn bộ chuỗi HTML thô. Sử dụng một thư viện phân tích HTML (như `BeautifulSoup` nếu cần) để đảm bảo an toàn. | 