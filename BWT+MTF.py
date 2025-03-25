from BWT import run_bwt
from MTF import mtf_encoder, mtf_decoder
from utils import read_binary_file, write_binary_file, print_information

# input_files = ["pic_original.raw", "книга.txt", "enwik7.txt", "pic_bg.jpg", "pic_bw.jpg", "pic_original.jpg", "registry.x86_64.bin"]
input_files = ["enwik7.txt"]
sizes = [5000, 10000, 100000, 1000000, 10000000, 100000000, 200000000, 500000000, 1000000000, 2000000000]
# слишком много промежуточных файлов
for input_file in input_files:
    for size in sizes:
        path_to_input_file = "data/" + input_file

        path_to_semicompressed_file = "semicompressed/" + input_file
        path_to_compressed_file = "compressed/" + input_file

        path_to_semidecompressed_file = "semidecompressed/" + input_file
        path_to_output_file = "decompressed/" + input_file

        print(input_file)
        print(f"Размер блока: {size}")
        run_bwt("compress", path_to_input_file, path_to_semicompressed_file, size)

        mtf_encode_data = mtf_encoder(read_binary_file(path_to_semicompressed_file))
        write_binary_file(path_to_compressed_file, mtf_encode_data)

        mtf_decode_data = mtf_decoder(read_binary_file(path_to_compressed_file))
        write_binary_file(path_to_semidecompressed_file, mtf_decode_data)

        run_bwt("decompress", path_to_semidecompressed_file, path_to_output_file, size)

        print_information(path_to_input_file, path_to_compressed_file, path_to_output_file)
        print("-----------")
