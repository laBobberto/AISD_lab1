import os

from Lz77 import run_lz77
from Lz78 import run_lz78
from utils import read_binary_file

input_files = ["registry.x86_64.bin", "книга.txt", "enwik7.txt", "pic_bg.jpg", "pic_bw.jpg", "pic_original.jpg"]
compressed_file = "compressed.bin"
decompressed_file = "decompressed.txt"

for input_file in input_files:
    window_size = 4096
    block_size = 255
    # Сжатие
    run_lz77("compress", "data/" + input_file, "compressed/" + input_file[:-4] + ".bin", window_size, block_size)

    # Распаковка
    run_lz77("decompress", "compressed/" + input_file[:-4] + ".bin", "decompressed/" + input_file, window_size, block_size)


    print("Тестовый файл: " + input_file)
    print("Коэффициент сжатия: ", os.path.getsize("data/" + input_file)/os.path.getsize("compressed/" + input_file[:-4] + ".bin"))
    print(f"Размер оригинального файла: {os.path.getsize('data/' + input_file)} байт")
    print(f"Размер сжатого файла: {os.path.getsize("compressed/" + input_file[:-4] + ".bin")} байт")
    print("Корректность восстановленных данных:", read_binary_file("data/" + input_file) == read_binary_file("decompressed/" + input_file), end="\n\n")