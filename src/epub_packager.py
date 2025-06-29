import os
from ebooklib import epub
from typing import List
import uuid

class EpubPackager:
    """
    Lớp chịu trách nhiệm đóng gói các file HTML, hình ảnh và CSS
    thành một file EPUB 3.0 hoàn chỉnh.
    """

    def __init__(self, book_title: str, author: str = "PDF2Epub Tool"):
        """
        Khởi tạo EpubPackager.

        Args:
            book_title (str): Tiêu đề của sách.
            author (str, optional): Tên tác giả. Mặc định là "PDF2Epub Tool".
        """
        self.book = epub.EpubBook()
        self.book.set_title(book_title)
        self.book.set_language("vi")  # Mặc định ngôn ngữ tiếng Việt
        self.book.add_author(author)
        # Tạo một identifier duy nhất cho sách
        self.book.set_identifier(str(uuid.uuid4()))

    def create_epub(self, html_files: List[str], resource_dir: str, output_path: str):
        """
        Tạo file EPUB từ các tài nguyên đã cho.

        Args:
            html_files (List[str]): Danh sách các đường dẫn đến file HTML (đã được sắp xếp).
            resource_dir (str): Thư mục chứa các tài nguyên (CSS, images).
            output_path (str): Đường dẫn để lưu file EPUB cuối cùng.
        """
        print("Bắt đầu quá trình đóng gói EPUB...")
        
        items = []
        chapters = []
        
        # 1. Thêm Stylesheet
        style_path = os.path.join(resource_dir, 'style.css')
        if os.path.exists(style_path):
            with open(style_path, 'r', encoding='utf-8') as f:
                css_content = f.read()
            stylesheet = epub.EpubItem(uid="style_main", file_name="style/main.css", media_type="text/css", content=css_content)
            self.book.add_item(stylesheet)
            items.append(stylesheet)
        else:
            stylesheet = None # Không có stylesheet
            print("Cảnh báo: Không tìm thấy file style.css.")

        # 2. Thêm các trang HTML (dưới dạng chapters)
        for i, html_path in enumerate(html_files):
            page_number = i + 1
            file_name = os.path.basename(html_path)
            
            with open(html_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            chapter = epub.EpubHtml(title=f'Trang {page_number}', file_name=file_name, lang='vi')
            chapter.content = html_content
            if stylesheet:
                chapter.add_item(stylesheet) # Liên kết stylesheet với chapter
            
            self.book.add_item(chapter)
            chapters.append(chapter)

        # 3. Thêm hình ảnh
        image_dir = os.path.join(resource_dir, 'images')
        if os.path.isdir(image_dir):
            for img_filename in sorted(os.listdir(image_dir)):
                img_path = os.path.join(image_dir, img_filename)
                with open(img_path, 'rb') as f:
                    img_content = f.read()
                
                # Xác định media type dựa trên phần mở rộng file
                ext = os.path.splitext(img_filename)[1].lower()
                media_type = f'image/{ext[1:]}' # ví dụ: image/jpeg, image/png
                
                image_item = epub.EpubImage(
                    uid=f'img_{img_filename}',
                    file_name=os.path.join('images', img_filename).replace("\\", "/"),
                    media_type=media_type,
                    content=img_content
                )
                self.book.add_item(image_item)
        else:
             print("Cảnh báo: Không tìm thấy thư mục 'images'.")


        # 4. Định nghĩa cấu trúc sách (spine và table of contents)
        self.book.spine = ['nav'] + chapters  # 'nav' là trang mục lục sẽ được tạo tự động

        # Tạo mục lục (Table of Contents)
        self.book.toc = chapters

        # Thêm mục lục NCX và Nav Point (cần thiết cho EPUB 3)
        self.book.add_item(epub.EpubNcx())
        self.book.add_item(epub.EpubNav())

        # 5. Viết ra file .epub
        epub.write_epub(output_path, self.book, {})
        print(f"Đã tạo thành công file EPUB tại: '{output_path}'") 