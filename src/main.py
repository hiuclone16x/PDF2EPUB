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
    # Tham số bắt buộc
    parser.add_argument("input_file", help="Đường dẫn đến file PDF đầu vào.")
    parser.add_argument("output_file", help="Đường dẫn để lưu file EPUB đầu ra. Phần mở rộng .epub sẽ được tự động thêm vào nếu thiếu.")
    
    # Tham số tùy chọn Sprint 2
    parser.add_argument(
        "--skip-pages",
        type=str,
        default="",
        help='Chuỗi các trang cần bỏ qua. \nVí dụ: "1,3,5-7" sẽ bỏ qua trang 1, 3, 5, 6, 7.'
    )
    parser.add_argument(
        "--remove-keywords",
        nargs='*',
        default=[],
        help='Danh sách các từ khóa cần loại bỏ khỏi văn bản, phân tách bởi dấu cách. \nVí dụ: --remove-keywords "Bản quyền" "Draft"'
    )
    parser.add_argument(
        "--image-quality",
        type=int,
        default=85,
        help="Chất lượng hình ảnh sau khi nén (1-100). Mặc định: 85."
    )
    parser.add_argument(
        "--image-max-width",
        type=int,
        default=1024,
        help="Chiều rộng tối đa cho hình ảnh (pixels). Mặc định: 1024."
    )
    parser.add_argument(
        "--no-image-optimization",
        action="store_true",
        help="Tắt hoàn toàn tính năng tối ưu hóa hình ảnh."
    )
    
    args = parser.parse_args()

    # --- Bắt đầu luồng thực thi ---
    if not args.output_file.lower().endswith('.epub'):
        args.output_file += '.epub'

    temp_dir = tempfile.mkdtemp(prefix="pdf2epub_")
    logging.info(f"Thư mục làm việc tạm thời: {temp_dir}")

    try:
        # 2. Xử lý PDF
        logging.info("-" * 20)
        processor = PDFProcessor(pdf_path=args.input_file)
        all_pages_data = processor.extract_content_by_page()

        # Lọc các trang cần bỏ qua
        pages_to_skip = parse_page_ranges(args.skip_pages)
        pages_to_process = [page for page in all_pages_data if page['page_number'] not in pages_to_skip]
        if pages_to_skip:
            logging.info(f"Đã bỏ qua các trang: {sorted(list(pages_to_skip))}")

        # 3. Chuyển đổi sang HTML
        logging.info("-" * 20)
        book_title = os.path.splitext(os.path.basename(args.input_file))[0]
        
        # Khởi tạo optimizer nếu được bật
        optimizer = None
        if not args.no_image_optimization:
            optimizer = ImageOptimizer(quality=args.image_quality, max_width=args.image_max_width)
            logging.info(f"Tối ưu hóa hình ảnh được BẬT (chất lượng: {args.image_quality}, rộng tối đa: {args.image_max_width}px).")
        else:
            logging.info("Tối ưu hóa hình ảnh đã được TẮT.")

        converter = HTMLConverter(book_title=book_title, output_dir=temp_dir, image_optimizer=optimizer)
        converter.create_stylesheet()
        
        html_files = []
        for page_data in pages_to_process:
            html_path = converter.create_html_from_page(
                page_data, 
                keywords_to_remove=args.remove_keywords
            )
            html_files.append(html_path)
        
        if args.remove_keywords:
            logging.info(f"Đã thực hiện loại bỏ các từ khóa: {args.remove_keywords}")

        # 4. Đóng gói thành EPUB
        logging.info("-" * 20)
        packager = EpubPackager(book_title=book_title)
        packager.create_epub(
            html_files=html_files,
            resource_dir=temp_dir,
            output_path=args.output_file
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