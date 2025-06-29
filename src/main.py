import argparse
import os
import shutil
import tempfile
import sys

from pdf_processor import PDFProcessor
from html_converter import HTMLConverter
from epub_packager import EpubPackager

def main():
    """
    Hàm chính điều phối toàn bộ quá trình chuyển đổi từ PDF sang EPUB.
    """
    # 1. Thiết lập và phân tích các tham số dòng lệnh
    parser = argparse.ArgumentParser(
        description="Một công cụ dòng lệnh để chuyển đổi file PDF sang định dạng EPUB 3.0."
    )
    parser.add_argument(
        "input_file", 
        help="Đường dẫn đến file PDF đầu vào."
    )
    parser.add_argument(
        "output_file", 
        help="Đường dẫn để lưu file EPUB đầu ra. Nếu không có phần mở rộng .epub, nó sẽ được tự động thêm vào."
    )
    args = parser.parse_args()

    input_path = args.input_file
    output_path = args.output_file

    # Đảm bảo file output có phần mở rộng .epub
    if not output_path.lower().endswith('.epub'):
        output_path += '.epub'

    # Tạo một thư mục tạm thời để chứa các file trung gian (HTML, CSS, images)
    temp_dir = tempfile.mkdtemp(prefix="pdf2epub_")
    print(f"Thư mục làm việc tạm thời: {temp_dir}")

    try:
        # 2. Xử lý PDF
        print("-" * 20)
        processor = PDFProcessor(pdf_path=input_path)
        pages_data = processor.extract_content_by_page()

        # 3. Chuyển đổi sang HTML
        print("-" * 20)
        # Lấy tên file không có phần mở rộng để làm tiêu đề sách
        book_title = os.path.splitext(os.path.basename(input_path))[0]
        converter = HTMLConverter(book_title=book_title, output_dir=temp_dir)
        converter.create_stylesheet()
        
        html_files = []
        for page_data in pages_data:
            html_path = converter.create_html_from_page(page_data)
            html_files.append(html_path)

        # 4. Đóng gói thành EPUB
        print("-" * 20)
        packager = EpubPackager(book_title=book_title)
        packager.create_epub(
            html_files=html_files,
            resource_dir=temp_dir,
            output_path=output_path
        )

        # Đóng file PDF sau khi đã xử lý xong
        processor.close()
        print("-" * 20)
        print("🎉 Quá trình chuyển đổi đã hoàn tất thành công! 🎉")

    except FileNotFoundError as e:
        print(f"Lỗi: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Đã xảy ra một lỗi không mong muốn: {e}", file=sys.stderr)
        print("Vui lòng kiểm tra lại file PDF đầu vào hoặc báo cáo lỗi.", file=sys.stderr)
        sys.exit(1)
    finally:
        # 5. Dọn dẹp thư mục tạm
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
            print(f"Đã dọn dẹp thư mục tạm thời: {temp_dir}")


if __name__ == "__main__":
    main() 