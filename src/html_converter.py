import os
from typing import Dict, Any, List, Optional
import re
from bs4 import BeautifulSoup
from bs4.element import NavigableString
import logging

# Giả định image_optimizer.py nằm cùng cấp và có thể import
from image_optimizer import ImageOptimizer

class HTMLConverter:
    """
    Lớp chịu trách nhiệm chuyển đổi dữ liệu trang (đã được trích xuất)
    thành các file HTML, đồng thời xử lý từ khóa và tối ưu hóa ảnh.
    """

    def __init__(self, book_title: str, output_dir: str, image_optimizer: Optional[ImageOptimizer] = None):
        """
        Khởi tạo HTMLConverter.

        Args:
            book_title (str): Tiêu đề của sách.
            output_dir (str): Thư mục để lưu các file HTML và hình ảnh.
            image_optimizer (Optional[ImageOptimizer]): Đối tượng để tối ưu hóa ảnh.
        """
        self.book_title = book_title
        self.output_dir = output_dir
        self.image_dir = os.path.join(self.output_dir, "images")
        self.image_optimizer = image_optimizer
        
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.image_dir, exist_ok=True)
        logging.info(f"Thư mục output đã sẵn sàng tại: '{self.output_dir}'")

    def _remove_keywords_from_html(self, html_content: str, keywords: List[str]) -> str:
        """Sử dụng BeautifulSoup để xóa từ khóa một cách an toàn."""
        soup = BeautifulSoup(html_content, 'html.parser')
        # Tìm tất cả các chuỗi văn bản trong cây HTML
        for text_node in soup.find_all(string=True):
            if isinstance(text_node, NavigableString):
                new_text = text_node
                for keyword in keywords:
                    # re.IGNORECASE để không phân biệt hoa thường
                    new_text = re.sub(r'\b' + re.escape(keyword) + r'\b', '', new_text, flags=re.IGNORECASE)
                text_node.replace_with(new_text) # type: ignore
        return str(soup)

    def create_html_from_page(
        self, 
        page_data: Dict[str, Any],
        keywords_to_remove: Optional[List[str]] = None
    ) -> str:
        """
        Tạo một file HTML từ dữ liệu của một trang.
        """
        page_number = page_data["page_number"]
        html_content = page_data["text"]

        # 1. Loại bỏ từ khóa nếu có
        if keywords_to_remove and html_content:
            html_content = self._remove_keywords_from_html(html_content, keywords_to_remove)

        # 2. Lưu và tối ưu hóa hình ảnh
        soup = BeautifulSoup(html_content, 'html.parser')
        img_tags = soup.find_all('img')

        for i, image_info in enumerate(page_data["images"]):
            image_data = image_info["data"]
            
            # Tối ưu hóa ảnh nếu có optimizer
            if self.image_optimizer:
                optimized_data = self.image_optimizer.optimize_image(image_data)
                image_ext = "jpeg" # Optimizer chuyển ảnh sang JPEG
            else:
                optimized_data = image_data
                image_ext = image_info["ext"]

            image_filename = f"p{page_number}_img{i}.{image_ext}"
            image_path = os.path.join(self.image_dir, image_filename)

            with open(image_path, "wb") as f:
                f.write(optimized_data)
            
            # Cập nhật src trong tag <img> tương ứng
            if i < len(img_tags):
                relative_image_path = os.path.join("images", image_filename).replace("\\", "/")
                img_tags[i]['src'] = relative_image_path # type: ignore
                img_tags[i]['alt'] = f"Hình ảnh từ trang {page_number}" # type: ignore
        
        html_content = str(soup)

        # 3. Tạo nội dung HTML hoàn chỉnh
        final_html = f"""
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
  <title>{self.book_title} - Trang {page_number}</title>
  <meta charset="utf-8" />
  <link rel="stylesheet" type="text/css" href="style.css" />
</head>
<body>
  {html_content}
</body>
</html>
"""
        # Lưu file HTML
        html_filename = f"page_{page_number:04d}.xhtml"
        html_path = os.path.join(self.output_dir, html_filename)
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(final_html)
            
        logging.info(f"Đã tạo file HTML: '{html_filename}'")
        return html_path

    def create_stylesheet(self):
        """
        Tạo một file CSS đơn giản để định dạng cơ bản cho EPUB.
        """
        css_content = """
body {
    font-family: sans-serif;
    line-height: 1.6;
    margin: 2em;
}

img {
    max-width: 100%;
    height: auto;
    display: block;
    margin: 1em 0;
}

p {
    text-align: justify;
    margin: 0.5em 0;
}
"""
        css_path = os.path.join(self.output_dir, "style.css")
        with open(css_path, "w", encoding="utf-8") as f:
            f.write(css_content)
        logging.info("Đã tạo file CSS 'style.css'.")
        return "style.css" 