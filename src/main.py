import argparse
import os
import shutil
import tempfile
import sys
import logging

from pdf_processor import PDFProcessor
from html_converter import HTMLConverter
from epub_packager import EpubPackager
from image_optimizer import ImageOptimizer
from utils import parse_page_ranges
from layout_analyzer import LayoutAnalyzer
from toc_generator import TOCGenerator

def setup_logging():
    """Cấu hình hệ thống logging để ghi ra file và console."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("conversion.log"),
            logging.StreamHandler(sys.stdout)
        ]
    )

def main():
    """
    Hàm chính điều phối toàn bộ quá trình chuyển đổi từ PDF sang EPUB.
    """
    setup_logging()
    
    # 1. Thiết lập và phân tích các tham số dòng lệnh
    parser = argparse.ArgumentParser(
        description="Công cụ dòng lệnh để chuyển đổi file PDF sang định dạng EPUB 3.0.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    # Chuyển các tham số bắt buộc thành tùy chọn để có thể nhập sau
    parser.add_argument(
        "input_file",
        nargs='?',  # Đánh dấu là có thể có hoặc không
        default=None,
        help="Đường dẫn đến file PDF đầu vào (có thể bỏ trống để nhập sau)."
    )
    parser.add_argument(
        "output_file",
        nargs='?',  # Đánh dấu là có thể có hoặc không
        default=None,
        help="Đường dẫn để lưu file EPUB đầu ra (có thể bỏ trống để nhập sau)."
    )
    
    args = parser.parse_args()

    # --- Bắt đầu luồng thực thi ---

    # ===== PHẦN 1: LẤY THÔNG TIN TƯƠNG TÁC =====
    
    # Lấy và xác thực đường dẫn file input
    input_path = args.input_file
    while not input_path or not os.path.isfile(input_path):
        if input_path:  # Trường hợp người dùng cung cấp đường dẫn nhưng không hợp lệ
            logging.error(f"Lỗi: Không tìm thấy file tại '{input_path}'. Vui lòng thử lại.")
        
        try:
            input_path = input("➡️  Vui lòng nhập đường dẫn đến file PDF: ").strip().replace('"', '')
        except KeyboardInterrupt:
            logging.info("\nĐã hủy bởi người dùng. Tạm biệt!")
            sys.exit(0)
            
        if not input_path:
            logging.warning("Đường dẫn không được để trống.")

    # Lấy và xác thực đường dẫn file output
    output_path = args.output_file
    if not output_path:
        default_output = os.path.splitext(os.path.basename(input_path))[0] + '.epub'
        try:
            user_output = input(f"➡️  Vui lòng nhập tên file EPUB output [Mặc định: {default_output}]: ").strip()
            if not user_output:
                user_output = default_output
        except KeyboardInterrupt:
            logging.info("\nĐã hủy bởi người dùng. Tạm biệt!")
            sys.exit(0)
            
        output_path = user_output
    
    # Lấy các tùy chọn nâng cao một cách tương tác
    try:
        logging.info("-" * 20)
        logging.info("Cấu hình tùy chọn nâng cao:")
        
        skip_pages_str = input("➡️  Nhập các trang cần bỏ qua (vd: 1,3,5-7) [Bỏ trống nếu không có]: ").strip()
        
        remove_keywords_str = input("➡️  Nhập các từ khóa cần xóa, cách nhau bởi dấu phẩy (,) [Bỏ trống nếu không có]: ").strip()
        remove_keywords = [k.strip() for k in remove_keywords_str.split(',') if k.strip()]

        # Cấu hình phân tích bố cục
        layout_analyzer = None
        user_wants_layout_analysis = input("➡️  Bạn có muốn phân tích bố cục (cột)? (y/n) [Mặc định: y]: ").strip().lower()
        if user_wants_layout_analysis in ('', 'y', 'yes'):
            logging.info("Phân tích bố cục được BẬT.")
            layout_analyzer = LayoutAnalyzer()
        else:
            logging.info("Phân tích bố cục đã được TẮT.")

        # Cấu hình tạo mục lục tự động
        toc_generator = None
        user_wants_toc_generation = input("➡️  Bạn có muốn tạo mục lục tự động? (y/n) [Mặc định: y]: ").strip().lower()
        if user_wants_toc_generation in ('', 'y', 'yes'):
            logging.info("Tạo mục lục tự động được BẬT.")
            toc_generator = TOCGenerator()
        else:
            logging.info("Tạo mục lục tự động đã được TẮT.")

        # Cấu hình tối ưu hóa ảnh
        optimizer = None
        user_wants_optimization = input("➡️  Bạn có muốn tối ưu hóa hình ảnh không? (y/n) [Mặc định: y]: ").strip().lower()
        if user_wants_optimization in ('', 'y', 'yes'):
            logging.info("Tối ưu hóa hình ảnh được BẬT.")
            try:
                quality_str = input("    - Chất lượng ảnh (1-100) [Mặc định: 85]: ").strip()
                quality = int(quality_str) if quality_str else 85
            except ValueError:
                logging.warning("Giá trị không hợp lệ, sử dụng chất lượng mặc định là 85.")
                quality = 85

            try:
                width_str = input("    - Chiều rộng tối đa (pixels) [Mặc định: 1024]: ").strip()
                max_width = int(width_str) if width_str else 1024
            except ValueError:
                logging.warning("Giá trị không hợp lệ, sử dụng chiều rộng mặc định là 1024.")
                max_width = 1024
            
            optimizer = ImageOptimizer(quality=quality, max_width=max_width)
        else:
            logging.info("Tối ưu hóa hình ảnh đã được TẮT.")

    except KeyboardInterrupt:
        logging.info("\nĐã hủy bởi người dùng. Tạm biệt!")
        sys.exit(0)

    # Đảm bảo file output có phần mở rộng .epub
    if not output_path.lower().endswith('.epub'):
        output_path += '.epub'

    temp_dir = tempfile.mkdtemp(prefix="pdf2epub_")
    logging.info(f"Thư mục làm việc tạm thời: {temp_dir}")

    try:
        # 2. Xử lý PDF
        logging.info("-" * 20)
        processor = PDFProcessor(pdf_path=input_path)
        all_pages_data = processor.extract_structured_content()

        # Lọc các trang cần bỏ qua
        pages_to_skip = parse_page_ranges(skip_pages_str)
        pages_to_process = [page for page in all_pages_data if page['page_number'] not in pages_to_skip]
        if pages_to_skip:
            logging.info(f"Đã bỏ qua các trang: {sorted(list(pages_to_skip))}")

        # Phát hiện mục lục nếu người dùng yêu cầu
        headings = []
        if toc_generator:
            logging.info("-" * 20)
            logging.info("Bắt đầu quá trình phát hiện tiêu đề để tạo mục lục...")
            headings = toc_generator.detect_headings(pages_to_process)
            logging.info(f"Đã phát hiện được {len(headings)} tiêu đề.")

        # 3. Chuyển đổi sang HTML
        logging.info("-" * 20)
        book_title = os.path.splitext(os.path.basename(input_path))[0]
        
        converter = HTMLConverter(
            book_title=book_title, 
            output_dir=temp_dir, 
            image_optimizer=optimizer,
            layout_analyzer=layout_analyzer
        )
        converter.create_stylesheet()
        
        html_files = []
        for page_data in pages_to_process:
            html_path = converter.create_html_from_page(
                page_data, 
                keywords_to_remove=remove_keywords
            )
            html_files.append(html_path)
        
        if remove_keywords:
            logging.info(f"Đã thực hiện loại bỏ các từ khóa: {remove_keywords}")

        # 4. Đóng gói thành EPUB
        logging.info("-" * 20)
        packager = EpubPackager(book_title=book_title)
        packager.create_epub(
            html_files=html_files,
            resource_dir=temp_dir,
            output_path=output_path,
            dynamic_toc=headings
        )

        processor.close()
        logging.info("-" * 20)
        logging.info("🎉 Quá trình chuyển đổi đã hoàn tất thành công! 🎉")

    except FileNotFoundError as e:
        logging.error(f"Lỗi: {e}")
        sys.exit(1)
    except Exception as e:
        logging.error(f"Đã xảy ra một lỗi không mong muốn: {e}", exc_info=True)
        logging.error("Vui lòng kiểm tra lại file PDF đầu vào hoặc báo cáo lỗi.")
        sys.exit(1)
    finally:
        # 5. Dọn dẹp thư mục tạm
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
            logging.info(f"Đã dọn dẹp thư mục tạm thời: {temp_dir}")


if __name__ == "__main__":
    main() 