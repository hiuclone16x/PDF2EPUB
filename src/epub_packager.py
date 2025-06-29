import os
from ebooklib import epub
from typing import List, Optional
import uuid
import logging

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

    def create_epub(self, html_files: List[str], resource_dir: str, output_path: str, dynamic_toc: Optional[List[tuple]] = None):
        """
        Tạo file EPUB từ các tài nguyên đã cho.

        Args:
            html_files (List[str]): Danh sách các đường dẫn đến file HTML (đã được sắp xếp).
            resource_dir (str): Thư mục chứa các tài nguyên (CSS, images).
            output_path (str): Đường dẫn để lưu file EPUB cuối cùng.
            dynamic_toc (Optional[List[tuple]], optional): Danh sách các tiêu đề để tạo mục lục động.
        """
        logging.info("Bắt đầu quá trình đóng gói EPUB...")
        
        items = []
        chapters = []
        
        # 1. Thêm Stylesheet
        style_path = os.path.join(resource_dir, 'style.css')
        if os.path.exists(style_path):
            with open(style_path, 'r', encoding='utf-8') as f:
                css_content = f.read()
            stylesheet = epub.EpubItem(uid="style_main", file_name="style/main.css", media_type="text/css", content=css_content.encode('utf-8'))
            self.book.add_item(stylesheet)
            items.append(stylesheet)
        else:
            stylesheet = None # Không có stylesheet
            logging.warning("Cảnh báo: Không tìm thấy file style.css.")

        # 2. Thêm các trang HTML (dưới dạng chapters)
        for i, html_path in enumerate(html_files):
            page_number = i + 1
            file_name = os.path.basename(html_path)
            
            with open(html_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            chapter = epub.EpubHtml(title=f'Trang {page_number}', file_name=file_name, lang='vi')
            chapter.content = html_content
            # Gán một ID duy nhất cho mỗi chapter để TOC có thể tham chiếu
            chapter.id = f"page_{page_number}"
            
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
             logging.warning("Cảnh báo: Không tìm thấy thư mục 'images'.")


        # 4. Định nghĩa cấu trúc sách (spine và table of contents)
        self.book.spine = ['nav'] + chapters  # 'nav' là trang mục lục sẽ được tạo tự động

        # Tạo mục lục (Table of Contents)
        if dynamic_toc:
            logging.info(f"Đang tạo mục lục động từ {len(dynamic_toc)} tiêu đề đã phát hiện...")
            # Tạo mục lục từ danh sách tiêu đề đã phát hiện
            toc_items = []
            for level, title, page_num in dynamic_toc:
                # Tìm chapter tương ứng với số trang
                target_chapter = next((c for c in chapters if c.id == f"page_{page_num}"), None)
                if target_chapter:
                    if level == 1:
                        section = epub.Section(title)
                        link = epub.Link(target_chapter.file_name, title, f"toc_{len(toc_items)}")
                        toc_items.append((section, link))
                    elif level > 1 and toc_items:
                        # Thêm như một mục con của mục cấp 1 gần nhất
                        parent_section, _ = toc_items[-1]
                        link = epub.Link(target_chapter.file_name, title, f"toc_{len(toc_items)}_{level}")
                        # EbookLib cấu trúc TOC dạng tuple(Section, (Link, Link, ...))
                        # Cần refactor lại cách thêm mục con
                        # Logic hiện tại chỉ hỗ trợ 2 cấp độ đơn giản
                        if isinstance(parent_section, epub.Section):
                            # Nếu mục cuối là Section, tạo tuple mới
                            if len(toc_items[-1]) == 2:
                                toc_items[-1] = (parent_section, (toc_items[-1][1], link))
                            else: # Nếu đã là tuple, nối thêm link
                                toc_items[-1] = (parent_section, toc_items[-1][1] + (link,))
            self.book.toc = toc_items
        else:
            # Mục lục mặc định: mỗi trang là một mục
            self.book.toc = chapters

        # Thêm mục lục NCX và Nav Point (cần thiết cho EPUB 3)
        self.book.add_item(epub.EpubNcx())
        self.book.add_item(epub.EpubNav())

        # 5. Viết ra file .epub
        epub.write_epub(output_path, self.book, {})
        logging.info(f"Đã tạo thành công file EPUB tại: '{output_path}'") 