def rle_encode(data: bytes) -> bytes:
    result = bytearray()
    i = 0
    n = len(data)
    while i < n:
        if i + 1 < n and data[i] == data[i + 1]:
            byte = data[i]
            max_length = min(127, n - i)
            length = 1
            while (i + length < n and
                   length < max_length and
                   data[i + length] == byte):
                length += 1

            result.append(0x80 | length)
            result.append(byte)
            i += length
        else:
            start = i
            max_length = min(127, n - start)
            end = start
            prev_byte = None

            while end < n and (end - start) < max_length:
                current_byte = data[end]
                if prev_byte == current_byte:
                    break
                prev_byte = current_byte
                end += 1

            unique_length = end - start
            if unique_length == 0:
                unique_length = 1
                end = start + 1

            result.append(unique_length)
            result.extend(data[start:end])
            i = end
    return bytes(result)


def rle_decode(encoded_data: bytes) -> bytes:
    result = bytearray()
    i = 0
    n = len(encoded_data)

    while i < n:
        if i >= n:
            break

        control_byte = encoded_data[i]
        i += 1
        is_repeated = (control_byte & 0x80) != 0
        length = control_byte & 0x7F

        if is_repeated:
            if i >= n:
                break
            byte = encoded_data[i]
            i += 1
            result.extend([byte] * length)
        else:
            end = i + length
            if end > n:
                end = n
            result.extend(encoded_data[i:end])
            i = end

    return bytes(result)
