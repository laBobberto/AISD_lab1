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


def byte_calculating(number: int) -> int:
    if number == 0:
        return 1
    bits = 1
    while number >= 2 ** bits:
        bits += 1
    return ceil(bits / 8)
