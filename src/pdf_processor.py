import fitz  # PyMuPDF
import os
from typing import List, Dict, Any
import logging

class PDFProcessor:
    """
    Lớp chịu trách nhiệm xử lý file PDF, bao gồm việc đọc và trích xuất
    nội dung từ file.
    """

    def __init__(self, pdf_path: str):
        """
        Khởi tạo đối tượng PDFProcessor.

        Args:
            pdf_path (str): Đường dẫn đến file PDF cần xử lý.

        Raises:
            FileNotFoundError: Nếu không tìm thấy file PDF tại đường dẫn đã cho.
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"Lỗi: Không tìm thấy file PDF tại '{pdf_path}'")
        
        self.pdf_path = pdf_path
        self.document = fitz.open(pdf_path)
        logging.info(f"Đã mở thành công file PDF: {os.path.basename(pdf_path)}")
        logging.info(f"Tổng số trang: {self.get_total_pages()}")

    def get_total_pages(self) -> int:
        """
        Trả về tổng số trang của tài liệu PDF.

        Returns:
            int: Tổng số trang.
        """
        return len(self.document)

    def extract_content_by_page(self) -> List[Dict[str, Any]]:
        """
        Trích xuất nội dung từ từng trang của file PDF.

        Phương thức này sẽ lặp qua từng trang, lấy ra nội dung văn bản dưới dạng
        HTML để giữ lại cấu trúc cơ bản và danh sách các hình ảnh.

        Returns:
            List[Dict[str, Any]]: Một danh sách các dictionary, mỗi dictionary
            đại diện cho một trang và chứa:
            - 'page_number': số thứ tự trang (bắt đầu từ 1)
            - 'text': nội dung văn bản của trang dưới dạng HTML
            - 'images': danh sách các hình ảnh, mỗi hình ảnh là một dictionary
                        chứa 'xref', 'data', và 'ext' (phần mở rộng file).
        """
        content_list = []
        total_pages = self.get_total_pages()

        for page_num in range(total_pages):
            page = self.document.load_page(page_num)
            logging.info(f"Đang xử lý trang {page_num + 1}/{total_pages}...")

            # Trích xuất văn bản dưới dạng HTML để bảo toàn cấu trúc cơ bản
            # Đây là một phương pháp nâng cao hơn get_text("text")
            text_content = page.get_text("html")

            # Trích xuất hình ảnh
            image_list = []
            images = page.get_images(full=True)
            for img_index, img in enumerate(images):
                xref = img[0]
                base_image = self.document.extract_image(xref)
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]
                image_list.append({
                    "xref": xref,
                    "data": image_bytes,
                    "ext": image_ext
                })

            content_list.append({
                "page_number": page_num + 1,
                "text": text_content,
                "images": image_list
            })
        
        logging.info("Hoàn tất trích xuất nội dung từ file PDF.")
        return content_list

    def close(self):
        """
        Đóng tài liệu PDF để giải phóng tài nguyên.
        """
        self.document.close()
        logging.info("Đã đóng file PDF.") 