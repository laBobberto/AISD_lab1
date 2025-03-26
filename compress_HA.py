import utils
from HA import ha_encoder, ha_decoder
from utils import read_binary_file, write_binary_file, write_table, collect_information

# input_files = ["pic_original.raw", "книга.txt", "enwik7.txt", "pic_bg.jpg", "pic_bw.jpg", "pic_original.jpg", "registry.x86_64.bin"]
# input_files = ["enwik7.txt"]
# buffer_sizes = [128, 512, 1024, 2048, 4096, 8192, 16384, 32768]
input_files = ["pic_1_bytes.raw", "pic_2_bytes.raw"]

for input_file in input_files:

    path_to_input_file = "data/" + input_file
    path_to_compressed_file = "compressed/" + input_file
    path_to_output_file = "decompressed/" + input_file

    print(input_file)
    write_binary_file(path_to_compressed_file, ha_encoder(read_binary_file(path_to_input_file)))

    write_binary_file(path_to_output_file, ha_decoder(read_binary_file(path_to_compressed_file)))
    write_table("combined.csv", collect_information("НА", input_file, path_to_input_file, path_to_compressed_file, path_to_output_file))
    # write_table("tables/ha.csv", collect_information("НА", input_file, path_to_input_file, path_to_compressed_file, path_to_output_file))
    print("-----------")