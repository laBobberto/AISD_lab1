from Lz77 import run_lz77
from utils import read_binary_file, write_binary_file, write_table, collect_information

# input_files = ["pic_original.raw", "книга.txt", "enwik7.txt", "pic_bg.jpg", "pic_bw.jpg", "pic_original.jpg", "registry.x86_64.bin"]
input_files = ["pic_1_bytes.raw", "pic_2_bytes.raw"]
for input_file in input_files:

    path_to_input_file = "data/" + input_file
    path_to_compressed_file = "compressed/" + input_file
    path_to_output_file = "decompressed/" + input_file

    print(input_file)
    run_lz77("compress", path_to_input_file, path_to_compressed_file, 16384, 128)

    run_lz77("decompress", path_to_compressed_file, path_to_output_file, 16384, 128)
    write_table("combined.csv", collect_information("LZ77", input_file, path_to_input_file, path_to_compressed_file, path_to_output_file))
    print("-----------")