import pytest
from src.utils import parse_page_ranges

# Các bộ dữ liệu để kiểm thử (test cases)
@pytest.mark.parametrize("input_string, expected_set", [
    ("1,3,5", {1, 3, 5}),
    ("1-5", {1, 2, 3, 4, 5}),
    ("1,3,5-7", {1, 3, 5, 6, 7}),
    (" 2 , 4-6 , 9 ", {2, 4, 5, 6, 9}),
    ("7-5,1", {1, 5, 6, 7}),  # Kiểm tra trường hợp nhập ngược
    ("1-1", {1}),
    ("", set()),  # Chuỗi rỗng
    ("3, 3, 3", {3}),  # Trùng lặp
    ("abc,1,2", {1, 2}),  # Dữ liệu không hợp lệ
    ("1-c,5", {5}),  # Khoảng không hợp lệ
    ("5,", {5}),  # Dấu phẩy cuối chuỗi
])
def test_parse_page_ranges(input_string, expected_set):
    """
    Kiểm tra chức năng của hàm parse_page_ranges với nhiều loại input khác nhau.
    """
    assert parse_page_ranges(input_string) == expected_set 