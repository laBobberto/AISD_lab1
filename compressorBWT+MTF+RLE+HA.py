from BWT import run_bwt
from HA import ha_encoder, ha_decoder
from MTF import mtf_encoder, mtf_decoder
from RLE import rle_encode, rle_decode
from utils import read_binary_file, write_binary_file, write_table, collect_information

# input_files = ["pic_original.raw", "книга.txt", "enwik7.txt", "pic_bg.jpg", "pic_bw.jpg", "pic_original.jpg", "registry.x86_64.bin"]
input_files = ["pic_1_bytes.raw", "pic_2_bytes.raw"]
for input_file in input_files:

    path_to_input_file = "data/" + input_file
    path_to_semicompressed_file = "semicompressed/" + input_file
    path_to_compressed_file = "compressed/" + input_file

    path_to_semidecompressed_file = "semidecompressed/" + input_file
    path_to_output_file = "decompressed/" + input_file

    print(input_file)
    run_bwt("compress", path_to_input_file, path_to_semicompressed_file, 100000000)
    write_binary_file(path_to_compressed_file, ha_encoder(rle_encode(mtf_encoder(read_binary_file(path_to_semicompressed_file)))))

    write_binary_file(path_to_semidecompressed_file, mtf_decoder(rle_decode(ha_decoder(read_binary_file(path_to_compressed_file)))))
    run_bwt("decompress", path_to_semicompressed_file, path_to_output_file, 100000000)

    write_table("combined.csv", collect_information("BWT + MTF + RLE + HA", input_file, path_to_input_file, path_to_compressed_file,
                                                       path_to_output_file))