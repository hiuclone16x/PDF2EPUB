import pytest
from unittest.mock import MagicMock, patch, mock_open
from src.epub_packager import EpubPackager

@pytest.fixture
def packager():
    """Tạo một instance của EpubPackager cho mỗi test."""
    return EpubPackager(book_title="Sách Thử Nghiệm")

def test_initialization(packager):
    """Kiểm tra xem các metadata cơ bản có được thiết lập đúng khi khởi tạo không."""
    assert packager.book.get_title() == "Sách Thử Nghiệm"
    assert packager.book.get_language() == "vi"
    assert packager.book.get_metadata('DC', 'creator')[0][0] == "PDF2Epub Tool"
    assert packager.book.get_identifier() is not None

@patch('builtins.open', new_callable=mock_open, read_data="body {color: black;}")
@patch('os.path.exists', return_value=True)
def test_add_stylesheet(mock_exists, mock_file, packager):
    """Kiểm tra việc thêm stylesheet."""
    html_file = "page_0001.xhtml"
    resource_dir = "/fake/dir"
    
    # Giả lập epub.EpubItem và book.add_item
    with patch('src.epub_packager.epub.EpubItem') as mock_epub_item, \
         patch.object(packager.book, 'add_item') as mock_add_item:
        
        packager.create_epub(html_files=[], resource_dir=resource_dir, output_path="/fake/output.epub")
        
        # Kiểm tra stylesheet được thêm vào sách
        mock_add_item.assert_any_call(mock_epub_item.return_value)
        # Kiểm tra file CSS được tạo với đúng nội dung và metadata
        mock_epub_item.assert_any_call(
            uid="style_main",
            file_name="style/main.css",
            media_type="text/css",
            content="body {color: black;}"
        )


@patch('builtins.open', new_callable=mock_open, read_data="<html></html>")
@patch('os.path.exists', return_value=False) # Giả lập không có stylesheet
def test_add_html_chapters(mock_exists, mock_file, packager):
    """Kiểm tra việc thêm các chapter HTML."""
    html_paths = ["/fake/dir/page_0001.xhtml", "/fake/dir/page_0002.xhtml"]
    
    with patch('src.epub_packager.epub.EpubHtml') as mock_epub_html, \
         patch.object(packager.book, 'add_item') as mock_add_item:
        
        # Giả lập mock_epub_html trả về một đối tượng có phương thức add_item
        mock_chapter = MagicMock()
        mock_epub_html.return_value = mock_chapter

        packager.create_epub(html_files=html_paths, resource_dir="/fake/dir", output_path="/fake/output.epub")
        
        # Phải được gọi 2 lần cho 2 chapter
        assert mock_epub_html.call_count == 2
        # Kiểm tra sách có thêm 2 chapter
        assert len(packager.book.items) == (2 + 2) # 2 chapter + NCX + NAV


@patch('builtins.open', new_callable=mock_open, read_data=b'imagedata')
@patch('os.path.isdir', return_value=True)
@patch('os.listdir', return_value=['test.jpg', 'test.png'])
def test_add_images(mock_listdir, mock_isdir, mock_file, packager):
    """Kiểm tra việc thêm hình ảnh."""
    with patch('src.epub_packager.epub.EpubImage') as mock_epub_image, \
         patch.object(packager.book, 'add_item') as mock_add_item:

        packager.create_epub(html_files=[], resource_dir="/fake/dir", output_path="/fake/output.epub")
        
        # Phải được gọi 2 lần cho 2 ảnh
        assert mock_epub_image.call_count == 2
        # Kiểm tra media type được xác định đúng
        mock_epub_image.assert_any_call(
            uid='img_test.jpg',
            file_name='images/test.jpg',
            media_type='image/jpeg',
            content=b'imagedata'
        )
        mock_epub_image.assert_any_call(
            uid='img_test.png',
            file_name='images/test.png',
            media_type='image/png',
            content=b'imagedata'
        ) 