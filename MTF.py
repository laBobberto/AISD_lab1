def mtf_encoder(data: bytes) -> bytes:
    symbol_list = list(range(256))
    encoded = []
    for byte in data:
        idx = symbol_list.index(byte)
        encoded.append(idx)
        symbol_list.pop(idx)
        symbol_list.insert(0, byte)
    return bytes(encoded)


def mtf_decoder(data: bytes) -> bytes:
    symbol_list = list(range(256))
    decoded = []
    for idx in data:
        symbol = symbol_list[idx]
        decoded.append(symbol)
        symbol_list.pop(idx)
        symbol_list.insert(0, symbol)
    return bytes(decoded)

