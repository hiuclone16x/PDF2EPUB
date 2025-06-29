# 📍 Các task kỹ thuật cho Sprint 2

## 🎯 Mục tiêu
Triển khai toàn bộ các story trong Epic 2: Nâng cao Trải nghiệm và Tùy chỉnh.

## 📋 Các task cần làm (Implementation THẬT)

### Story 2.1: Bỏ qua các trang được chỉ định
- [ ] `task`: Cập nhật `src/main.py` để thêm tham số tùy chọn `--skip-pages` vào `argparse`. Tham số này nhận một chuỗi các số trang được phân tách bằng dấu phẩy (ví dụ: "1,2,5-7").
- [ ] `task`: Viết một hàm tiện ích để phân tích chuỗi `skip-pages` thành một tập hợp (set) các số trang cần bỏ qua.
- [ ] `task`: Cập nhật logic trong `main.py` để lọc danh sách các trang được xử lý, loại bỏ những trang có trong tập hợp `skip-pages` trước khi truyền vào `HTMLConverter`.
- [ ] `task`: Thêm unit test để xác minh hàm phân tích chuỗi và logic lọc trang hoạt động chính xác.

### Story 2.2: Tìm và loại bỏ từ khóa
- [ ] `task`: Cập nhật `src/main.py` để thêm tham số tùy chọn `--remove-keywords`. Tham số này nhận một danh sách các từ khóa.
- [ ] `task`: Cập nhật phương thức `create_html_from_page` trong `src/html_converter.py` để nhận thêm tham số `keywords_to_remove`.
- [ ] `task`: Implement logic bên trong `create_html_from_page` để lặp qua danh sách từ khóa và thực hiện thay thế chúng bằng một chuỗi rỗng (`''`) trong nội dung văn bản của trang. Đảm bảo việc thay thế không phân biệt chữ hoa/thường.
- [ ] `task`: Thêm unit test để kiểm tra logic thay thế từ khóa.

### Story 2.3: Tối ưu hóa hình ảnh
- [ ] `task`: Cập nhật `src/main.py` để thêm các tham số tùy chọn cho việc tối ưu hóa ảnh, ví dụ: `--image-quality` (1-100), `--image-max-width` (pixels).
- [ ] `task`: Tạo một module mới `src/image_optimizer.py` và lớp `ImageOptimizer`.
- [ ] `task`: Implement phương thức `optimize_image(self, image_path, quality, max_width)` trong `ImageOptimizer` sử dụng thư viện `Pillow`.
    - [ ] `subtask`: Mở ảnh.
    - [ ] `subtask`: Thay đổi kích thước (resize) nếu chiều rộng của ảnh lớn hơn `max_width`, giữ nguyên tỷ lệ.
    - [ ] `subtask`: Lưu lại ảnh với chất lượng (quality) được chỉ định, ghi đè lên file gốc.
- [ ] `task`: Tích hợp `ImageOptimizer` vào luồng làm việc trong `main.py`, gọi nó sau khi ảnh được trích xuất bởi `PDFProcessor` và trước khi `EpubPackager` được gọi.
- [ ] `task`: Thêm test để xác minh rằng kích thước ảnh và dung lượng file giảm sau khi tối ưu hóa.

## ✅ Tiêu chí hoàn thành (THỰC TẾ)
- [ ] Tất cả các task được đánh dấu hoàn thành.
- [ ] Chạy lệnh `python src/main.py sample.pdf output.epub --skip-pages "1,3" --remove-keywords "Copyright" --image-quality 80` thành công.
- [ ] Trang 1 và 3 không xuất hiện trong file `output.epub`.
- [ ] Từ "Copyright" (không phân biệt hoa thường) bị xóa khỏi nội dung.
- [ ] Kích thước file của hình ảnh trong EPUB nhỏ hơn so với bản gốc. 