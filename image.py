import numpy as np
from PIL import Image
import io

from utils import read_binary_file, write_binary_file


class CustomRaw:
    def __init__(self, bytes_per_pixel=3):
        if bytes_per_pixel not in (1, 3):
            raise ValueError("Bytes per pixel must be 1 or 3")
        self.bytes_per_pixel = bytes_per_pixel

    def from_jpg(self, jpg_data):
        img = Image.open(io.BytesIO(jpg_data))

        if self.bytes_per_pixel == 1:
            img = img.convert("L")  # Оттенки серого
        else:
            img = img.convert("RGB")

        arr = np.array(img)

        if self.bytes_per_pixel == 1:
            raw_data = arr.tobytes()
        else:
            raw_data = arr.astype(np.uint8).tobytes()

        return raw_data, img.size

    def to_jpg(self, raw_data, size, quality=85):
        width, height = size
        arr = np.frombuffer(raw_data, dtype=np.uint8)

        if self.bytes_per_pixel == 1:
            arr = arr.reshape((height, width))
            img = Image.fromarray(arr, mode="L")
        else:
            arr = arr.reshape((height, width, 3))
            img = Image.fromarray(arr, mode="RGB")

        jpg_buffer = io.BytesIO()
        img.save(jpg_buffer, format="JPEG", quality=quality)
        return jpg_buffer.getvalue()


if __name__ == "__main__":
    jpg_bytes = read_binary_file("data/pic_original.jpg")

    converter = CustomRaw(bytes_per_pixel=3)

    raw_data, size = converter.from_jpg(jpg_bytes)
    write_binary_file("data/pic_original.raw", raw_data)

    # jpg_bytes = converter.to_jpg(raw_data, size)
    # write_binary_file("data/pic_original_decompressed.jpg", jpg_bytes)
