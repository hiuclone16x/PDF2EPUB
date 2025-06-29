import logging
import re
from typing import List, Dict, Any, Tuple
from collections import Counter

class TOCGenerator:
    """
    Lớp chịu trách nhiệm phân tích nội dung văn bản để tự động
    nhận dạng các tiêu đề và tạo ra một cấu trúc mục lục (TOC).
    """

    def __init__(self, min_level: int = 1, max_level: int = 3):
        """Khởi tạo TOCGenerator."""
        self.min_level = min_level
        self.max_level = max_level
        # Các mẫu regex để nhận dạng tiêu đề, từ cấp cao đến thấp
        self.HEADING_PATTERNS = [
            re.compile(r'^\s*(chương|phần|part|chapter)\s+\d+', re.IGNORECASE),  # Cấp 1
            re.compile(r'^\s*\d+\.\s+.*'),                                    # Cấp 2
            re.compile(r'^\s*\d+\.\d+\.\s+.*'),                                # Cấp 3
            re.compile(r'^\s*[A-Z]\.\s+.*'),                                  # Cấp 2 (A, B, C)
        ]
        logging.info("Khởi tạo TOCGenerator.")

    def _get_most_common_font_style(self, all_pages_data: List[Dict[str, Any]]) -> Tuple[float, str]:
        """Phân tích tất cả các trang để tìm ra size và font phổ biến nhất."""
        font_sizes = []
        font_names = []
        for page_data in all_pages_data:
            content_dict = page_data.get("content_dict", {})
            for block in content_dict.get("blocks", []):
                if block.get("type") == 0: # Text block
                    for line in block.get("lines", []):
                        for span in line.get("spans", []):
                            font_sizes.append(round(span.get("size", 0)))
                            font_names.append(span.get("font", ""))
        
        if not font_sizes:
            return 12.0, "Unknown"

        most_common_size = Counter(font_sizes).most_common(1)[0][0]
        most_common_font = Counter(font_names).most_common(1)[0][0]
        
        logging.info(f"Font chữ phổ biến nhất: {most_common_font}, size: {most_common_size}pt")
        return float(most_common_size), most_common_font

    def detect_headings(self, all_pages_data: List[Dict[str, Any]]) -> List[Tuple[int, str, int]]:
        """
        Quét qua tất cả các trang để phát hiện tiêu đề.

        Returns:
            List[Tuple[int, str, int]]: Danh sách các tiêu đề, mỗi item là một tuple
            chứa (cấp độ, nội dung tiêu đề, số trang).
        """
        headings = []
        common_size, _ = self._get_most_common_font_style(all_pages_data)
        size_threshold = common_size * 1.15  # Tiêu đề phải lớn hơn 15%

        for page_data in all_pages_data:
            page_num = page_data['page_number']
            content_dict = page_data.get("content_dict", {})
            for block in content_dict.get("blocks", []):
                if block.get("type") == 0: # Text block
                    for line in block.get("lines", []):
                        # Giả định một dòng là một ứng viên tiêu đề tiềm năng
                        line_text = "".join(span.get("text", "") for span in line.get("spans", [])).strip()
                        if not line_text or len(line_text.split()) > 15: # Bỏ qua dòng quá dài
                            continue

                        # Heuristic 1: Dựa vào kích thước font và độ đậm
                        first_span = line.get("spans", [{}])[0]
                        span_size = first_span.get("size", 0)
                        is_bold = "bold" in first_span.get("font", "").lower()

                        if span_size > size_threshold or is_bold:
                            # Heuristic 2: Dựa vào mẫu Regex
                            for i, pattern in enumerate(self.HEADING_PATTERNS):
                                if pattern.match(line_text):
                                    level = i + 1
                                    headings.append((level, line_text, page_num))
                                    logging.info(f"Phát hiện tiêu đề cấp {level} (Regex) ở trang {page_num}: '{line_text}'")
                                    break # Đã khớp, không cần check các mẫu khác
                            else: # Nếu không khớp regex nào, chỉ dựa vào font
                                if span_size > size_threshold * 1.2: # Ngưỡng cao hơn cho non-regex
                                    level = 1
                                    headings.append((level, line_text, page_num))
                                    logging.info(f"Phát hiện tiêu đề cấp {level} (Font) ở trang {page_num}: '{line_text}'")

        return headings 