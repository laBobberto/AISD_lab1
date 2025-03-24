from utils import search_two_min, count_bytes


class Node:
    def __init__(self, frequency, old_code="", left=None, right=None):
        self.left = left
        self.right = right
        self.frequency = frequency
        self.old_code = old_code

    def __lt__(self, other):
        return self.frequency < other.frequency


class HATree:
    def __init__(self):
        self.root = None
        self.codes = {}

    def build_tree(self, frequencies):
        nodes = [Node(frequencies[i], str(i)) for i in range(256) if frequencies[i] > 0]

        while len(nodes) > 1:
            left, right, left_index, right_index = search_two_min(nodes)

            nodes.pop(max(left_index, right_index))
            nodes.pop(min(left_index, right_index))

            merged = Node(left.frequency + right.frequency, left=left, right=right)
            nodes.append(merged)

        self.root = nodes[0] if nodes else None
        self._generate_codes(self.root, "")

    def _generate_codes(self, node, prefix):
        if node is None:
            return
        if not node.left and not node.right:
            self.codes[int(node.old_code)] = prefix
        self._generate_codes(node.left, prefix + "0")
        self._generate_codes(node.right, prefix + "1")


def ha_encoder(data: bytes) -> bytes:
    frequencies = count_bytes(data)
    tree = HATree()
    tree.build_tree(frequencies)

    encoded_bits = ''.join(tree.codes[byte] for byte in data)
    bit_length = len(encoded_bits)

    header = bit_length.to_bytes(4, 'little')
    non_zero = sum(1 for f in frequencies if f > 0)
    header += non_zero.to_bytes(4, 'little')

    for byte in range(256):
        if frequencies[byte] > 0:
            header += bytes([byte]) + frequencies[byte].to_bytes(4, 'little')

    padded_bits = encoded_bits.ljust(((bit_length + 7) // 8) * 8, '0')
    encoded_bytes = bytes(int(padded_bits[i:i + 8], 2) for i in range(0, len(padded_bits), 8))

    return header + encoded_bytes


def ha_decoder(encoded_data: bytes) -> bytes:
    bit_length = int.from_bytes(encoded_data[:4], 'little')
    non_zero = int.from_bytes(encoded_data[4:8], 'little')

    frequencies = [0] * 256
    pos = 8
    for _ in range(non_zero):
        byte = encoded_data[pos]
        freq = int.from_bytes(encoded_data[pos + 1:pos + 5], 'little')
        frequencies[byte] = freq
        pos += 5

    tree = HATree()
    tree.build_tree(frequencies)
    reverse_codes = {v: k for k, v in tree.codes.items()}

    encoded_bits = ''.join(f'{byte:08b}' for byte in encoded_data[pos:])
    encoded_bits = encoded_bits[:bit_length]

    decoded = []
    current_code = ''
    for bit in encoded_bits:
        current_code += bit
        if current_code in reverse_codes:
            decoded.append(reverse_codes[current_code])
            current_code = ''

    return bytes(decoded)



