import os
from typing import Dict, Any, List
import re

class HTMLConverter:
    """
    Lớp chịu trách nhiệm chuyển đổi dữ liệu trang (đã được trích xuất)
    thành các file HTML.
    """

    def __init__(self, book_title: str, output_dir: str):
        """
        Khởi tạo HTMLConverter.

        Args:
            book_title (str): Tiêu đề của sách, dùng để tạo tiêu đề cho file HTML.
            output_dir (str): Thư mục để lưu các file HTML và hình ảnh.
        """
        self.book_title = book_title
        self.output_dir = output_dir
        self.image_dir = os.path.join(self.output_dir, "images")
        
        # Tạo các thư mục output nếu chúng chưa tồn tại
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.image_dir, exist_ok=True)
        print(f"Thư mục output đã sẵn sàng tại: '{self.output_dir}'")

    def create_html_from_page(self, page_data: Dict[str, Any]) -> str:
        """
        Tạo một file HTML từ dữ liệu của một trang.

        Lưu hình ảnh vào thư mục 'images' và thay thế các tham chiếu hình ảnh
        trong nội dung HTML.

        Args:
            page_data (Dict[str, Any]): Dictionary chứa dữ liệu của trang,
                                        bao gồm 'page_number', 'text', 'images'.

        Returns:
            str: Đường dẫn đến file HTML đã được tạo.
        """
        page_number = page_data["page_number"]
        html_content = page_data["text"]

        # Lưu hình ảnh và cập nhật đường dẫn trong HTML
        for i, image_info in enumerate(page_data["images"]):
            image_ext = image_info["ext"]
            image_data = image_info["data"]
            # Đặt tên file ảnh duy nhất cho mỗi trang để tránh trùng lặp
            image_filename = f"p{page_number}_img{i}.{image_ext}"
            image_path = os.path.join(self.image_dir, image_filename)

            with open(image_path, "wb") as f:
                f.write(image_data)
            
            # Tìm kiếm các thẻ <img> trong HTML trích xuất từ PyMuPDF và thay thế
            # src của chúng. PyMuPDF thường tạo ra các src trống hoặc không hợp lệ.
            # Chúng ta sẽ tìm thẻ img thứ i và thay thế src của nó.
            # Đây là một cách tiếp cận đơn giản, có thể cần cải tiến nếu PDF phức tạp.
            img_tag_pattern = re.compile(r"<img[^>]*>")
            img_tags = img_tag_pattern.findall(html_content)

            if i < len(img_tags):
                original_tag = img_tags[i]
                # Đường dẫn tương đối từ file HTML đến file ảnh
                relative_image_path = os.path.join("images", image_filename).replace("\\", "/")
                new_tag = f'<img src="{relative_image_path}" alt="Hình ảnh từ trang {page_number}" />'
                html_content = html_content.replace(original_tag, new_tag, 1)

        # Tạo nội dung HTML hoàn chỉnh
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
            
        print(f"Đã tạo file HTML: '{html_filename}'")
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
        print("Đã tạo file CSS 'style.css'.")
        return "style.css" 