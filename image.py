import numpy as np
from PIL import Image
import io
from utils import read_binary_file, write_binary_file


class CustomRaw:
    def __init__(self, bytes_per_pixel=3):
        if bytes_per_pixel not in (1, 2, 3):
            raise ValueError("Bytes per pixel must be 1, 2, or 3")
        self.bytes_per_pixel = bytes_per_pixel

    def from_jpg(self, jpg_data):
        img = Image.open(io.BytesIO(jpg_data))

        if self.bytes_per_pixel == 1:
            img = img.convert("L")  # Grayscale
            arr = np.array(img, dtype=np.uint8)
        elif self.bytes_per_pixel == 2:
            img = img.convert("RGB")
            arr = np.array(img, dtype=np.uint8)
            r = (arr[:, :, 0] >> 3).astype(np.uint16)
            g = (arr[:, :, 1] >> 2).astype(np.uint16)
            b = (arr[:, :, 2] >> 3).astype(np.uint16)
            arr = (r << 11) | (g << 5) | b
            arr = arr.astype(np.uint16).tobytes()
            return arr, img.size
        else:
            img = img.convert("RGB")
            arr = np.array(img, dtype=np.uint8).tobytes()

        return arr, img.size

    def to_jpg(self, raw_data, size, quality=85):
        width, height = size

        if self.bytes_per_pixel == 1:
            arr = np.frombuffer(raw_data, dtype=np.uint8).reshape((height, width))
            img = Image.fromarray(arr, mode="L")
        elif self.bytes_per_pixel == 2:
            arr = np.frombuffer(raw_data, dtype=np.uint16).reshape((height, width))
            r = ((arr >> 11) & 0x1F) << 3
            g = ((arr >> 5) & 0x3F) << 2
            b = (arr & 0x1F) << 3
            arr = np.stack([r, g, b], axis=-1).astype(np.uint8)
            img = Image.fromarray(arr, mode="RGB")
        else:
            arr = np.frombuffer(raw_data, dtype=np.uint8).reshape((height, width, 3))
            img = Image.fromarray(arr, mode="RGB")

        jpg_buffer = io.BytesIO()
        img.save(jpg_buffer, format="JPEG", quality=quality)
        return jpg_buffer.getvalue()


if __name__ == "__main__":
    jpg_bytes = read_binary_file("data/pic_original.jpg")

    for bpp in [1, 2]:
        converter = CustomRaw(bytes_per_pixel=bpp)
        raw_data, size = converter.from_jpg(jpg_bytes)
        write_binary_file(f"data/pic_{bpp}_bytes.raw", raw_data)

        # jpg_bytes = converter.to_jpg(raw_data, size)
        # write_binary_file(f"data/pic_{bpp}bpp_decompressed.jpg", jpg_bytes)
