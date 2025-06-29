from PIL import Image
import io

class ImageOptimizer:
    """
    Lớp chịu trách nhiệm tối ưu hóa hình ảnh (thay đổi kích thước và nén).
    """

    def __init__(self, quality: int = 85, max_width: int | None = 1024):
        """
        Khởi tạo ImageOptimizer.

        Args:
            quality (int): Chất lượng của ảnh sau khi nén (từ 1 đến 100).
                           Mặc định là 85.
            max_width (int | None): Chiều rộng tối đa của ảnh. Nếu ảnh gốc
                                  rộng hơn, nó sẽ được thu nhỏ lại.
                                  Mặc định là 1024px.
        """
        self.quality = quality
        self.max_width = max_width

    def optimize_image(self, image_bytes: bytes) -> bytes:
        """
        Tối ưu hóa một hình ảnh từ dữ liệu bytes.

        Args:
            image_bytes (bytes): Dữ liệu byte của hình ảnh gốc.

        Returns:
            bytes: Dữ liệu byte của hình ảnh đã được tối ưu hóa.
        """
        try:
            with Image.open(io.BytesIO(image_bytes)) as img:
                original_format = img.format
                
                # Chỉ thay đổi kích thước nếu có max_width và ảnh rộng hơn max_width
                if self.max_width and img.width > self.max_width:
                    ratio = self.max_width / img.width
                    new_height = int(img.height * ratio)
                    img = img.resize((self.max_width, new_height), Image.Resampling.LANCZOS)

                output_buffer = io.BytesIO()
                # Chuyển đổi sang RGB nếu là RGBA (loại bỏ kênh alpha) để lưu JPEG
                if img.mode in ("RGBA", "P"):
                    img = img.convert("RGB")
                    
                img.save(output_buffer, format='JPEG', quality=self.quality, optimize=True)
                return output_buffer.getvalue()
        except Exception as e:
            print(f"Cảnh báo: Không thể tối ưu hóa hình ảnh. Sử dụng ảnh gốc. Lỗi: {e}")
            return image_bytes 