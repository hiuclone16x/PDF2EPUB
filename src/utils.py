from typing import Set

def parse_page_ranges(page_string: str) -> Set[int]:
    """
    Phân tích một chuỗi đại diện cho các trang và khoảng trang thành một tập hợp các số nguyên.

    Ví dụ:
        "1,3,5-7" -> {1, 3, 5, 6, 7}
        "1-3,8" -> {1, 2, 3, 8}

    Args:
        page_string (str): Chuỗi chứa các trang cần phân tích.

    Returns:
        Set[int]: Một tập hợp các số trang duy nhất.
    """
    if not page_string:
        return set()

    result_pages: Set[int] = set()
    parts = page_string.split(',')

    for part in parts:
        part = part.strip()
        if not part:
            continue
        
        if '-' in part:
            try:
                start, end = map(int, part.split('-'))
                if start > end:
                    # Hoán đổi nếu người dùng nhập ngược, ví dụ 7-5
                    start, end = end, start
                result_pages.update(range(start, end + 1))
            except ValueError:
                print(f"Cảnh báo: Bỏ qua khoảng trang không hợp lệ '{part}'")
                continue
        else:
            try:
                result_pages.add(int(part))
            except ValueError:
                print(f"Cảnh báo: Bỏ qua số trang không hợp lệ '{part}'")
                continue

    return result_pages 