from pathlib import Path
import csv
import math
import os
from math import ceil


def read_binary_file(file_path: str):
    try:
        with open(file_path, 'rb') as file:
            return file.read()
    except Exception as e:
        print(f"Error: {e}")
        return b''

def write_binary_file(file_path: str, data: bytes):
    try:
        with open(file_path, 'wb') as file:
            file.write(data)
    except Exception as e:
        print(f"Error: {e}")

def count_bytes(data: bytes):
    result = [0] * 256

    for byte in data:
        result[byte] += 1

    return result

def search_two_min(arr):
    min_1, min_2 = arr[0], None
    min_1_index, min_2_index = 0, None
    for i in range(1, len(arr[1:])+1):
        if arr[i] < min_1:
            min_1, min_2 = arr[i], min_1
            min_1_index, min_2_index = i, min_1_index
        elif min_2 is None or arr[i] < min_2:
            min_2 = arr[i]
            min_2_index = i
    return min_1, min_2, min_1_index, min_2_index

# Ну тут можно было и логарифмом обойтись
def byte_calculating(number: int) -> int:
    if number == 0:
        return 1
    bits = 1
    while number >= 2 ** bits:
        bits += 1
    return ceil(bits / 8)

def entropy_count(data: bytes) -> int:
    bytes_frequency = count_bytes(data)
    entropy = 0

    for i in range(len(bytes_frequency)):
        frequency = bytes_frequency[i]/ len(data)
        if frequency != 0:
            entropy += frequency * math.log(frequency, 2)

    return entropy * -1

def print_information(input_file: str, compressed_file: str, output_file: str):
    print(f"Энтропия исходного файла: {entropy_count(read_binary_file(input_file))}")
    print(f"Энтропия сжатого файла: {entropy_count(read_binary_file(compressed_file))}")

    print(f"Размер исходного файла: {os.path.getsize(input_file)}")
    print(f"Размер сжатого файла: {os.path.getsize(compressed_file)}")
    print(f"Коэффициент сжатия: {os.path.getsize(input_file)/os.path.getsize(compressed_file):.3f}")

    print(f"Корректность декомпрессии: {read_binary_file(input_file) == read_binary_file(output_file)}")

def collect_information(alg, filename, input_file: str, compressed_file: str, output_file: str):
    row = [alg,
           filename,
           os.path.getsize(input_file),
           os.path.getsize(compressed_file),
           os.path.getsize(output_file),
           round(os.path.getsize(input_file)/os.path.getsize(compressed_file), 3),
           (read_binary_file(input_file) == read_binary_file(output_file))
           ]
    return row


def write_table(filename, new_data):
    file_exists = Path(filename).exists()

    with open(filename, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Метод сжатия", "Тестовый файл", "Размер до компрессии", "Размер после компрессии", "Размер после декомпрессии", "Коэффициент сжатия", "Корректность декомпресии"])
        writer.writerow(new_data)

