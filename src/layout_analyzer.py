import logging
from typing import List, Dict, Any

class LayoutAnalyzer:
    """
    Lớp chịu trách nhiệm phân tích bố cục của một trang PDF,
    bao gồm nhận dạng cột và bảng biểu (trong tương lai).
    """

    def __init__(self, column_threshold: float = 0.5):
        """
        Khởi tạo LayoutAnalyzer.

        Args:
            column_threshold (float): Ngưỡng để xác định điểm chia cột,
                                      tính theo tỷ lệ trên chiều rộng trang.
                                      Mặc định là 0.5 (ở giữa).
        """
        self.column_threshold = column_threshold
        logging.info("Khởi tạo LayoutAnalyzer.")

    def _sort_blocks_by_y_coordinate(self, blocks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Sắp xếp các khối văn bản theo thứ tự từ trên xuống dưới (tọa độ y)."""
        # bbox[1] là tọa độ y1 (top) của khối
        return sorted(blocks, key=lambda b: b['bbox'][1])

    def analyze_columns(self, page_blocks: List[Dict[str, Any]], page_width: float) -> List[Dict[str, Any]]:
        """
        Phân tích và sắp xếp lại các khối văn bản từ bố cục nhiều cột.
        Thuật toán này được thiết kế cho trường hợp 2 cột phổ biến.
        """
        left_column = []
        right_column = []
        other_blocks = []  # Dành cho các khối chiếm cả trang (tiêu đề, chân trang)
        
        center_line = page_width * self.column_threshold

        # Chỉ xem xét chia cột nếu có nhiều hơn 2 khối văn bản
        text_blocks = [b for b in page_blocks if b.get('type') == 0]
        if len(text_blocks) <= 2:
            return self._sort_blocks_by_y_coordinate(page_blocks)

        for block in page_blocks:
            # Bỏ qua các khối không phải văn bản (ví dụ: hình ảnh)
            if block.get('type') != 0:
                other_blocks.append(block)
                continue

            x0, _, x1, _ = block['bbox']
            
            # Khối nằm hoàn toàn bên trái đường chia
            if x1 < center_line - 5: # Thêm một khoảng đệm nhỏ
                left_column.append(block)
            # Khối nằm hoàn toàn bên phải đường chia
            elif x0 > center_line + 5: # Thêm một khoảng đệm nhỏ
                right_column.append(block)
            # Khối giao với đường trung tâm (có thể là tiêu đề/chân trang)
            else:
                other_blocks.append(block)

        # Nếu một trong hai cột quá ít nội dung, giả định đây không phải bố cục cột
        if len(left_column) < 1 or len(right_column) < 1:
            return self._sort_blocks_by_y_coordinate(page_blocks)

        logging.info("Phát hiện có khả năng là bố cục 2 cột. Đang sắp xếp lại nội dung.")
        
        # Sắp xếp các khối trong mỗi cột và các khối khác
        sorted_left = self._sort_blocks_by_y_coordinate(left_column)
        sorted_right = self._sort_blocks_by_y_coordinate(right_column)
        sorted_other = self._sort_blocks_by_y_coordinate(other_blocks)

        # Kết hợp lại theo thứ tự: các khối khác (tiêu đề/chân trang),
        # sau đó là toàn bộ cột trái, rồi đến toàn bộ cột phải.
        # Đây là một heuristic cơ bản nhưng hiệu quả cho nhiều trường hợp.
        reordered_blocks = sorted_other + sorted_left + sorted_right
        
        return reordered_blocks 