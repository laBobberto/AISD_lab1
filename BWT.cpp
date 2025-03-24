#include <iostream>
#include <fstream>
#include <vector>
#include <algorithm>
#include <string>
#include <stdexcept>
#include <iterator>
#include <cstdint>
#include <numeric>

using namespace std;

vector<uint8_t> bwt_transform(const vector<uint8_t>& block, int& index) {
    int n = block.size();
    if (n == 0) {
        index = 0;
        return {};
    }

    vector<int> indices(n);
    iota(indices.begin(), indices.end(), 0);

    // Сортируем индексы, сравнивая циклические вращения через исходный блок
    sort(indices.begin(), indices.end(), [&block, n](int a, int b) {
        for (int i = 0; i < n; ++i) {
            uint8_t ca = block[(a + i) % n];
            uint8_t cb = block[(b + i) % n];
            if (ca != cb) return ca < cb;
        }
        return false; // равны
    });

    // Найти позицию исходного блока (индекс 0)
    auto it = find(indices.begin(), indices.end(), 0);
    index = distance(indices.begin(), it);

    // Собрать transformed из последних символов каждого вращения
    vector<uint8_t> transformed;
    transformed.reserve(n);
    for (int i : indices) {
        transformed.push_back(block[(i + n - 1) % n]);
    }

    return transformed;
}

vector<uint8_t> bwt_inverse(const vector<uint8_t>& transformed, int index) {
    int n = transformed.size();
    if (n == 0) return {};

    vector<pair<uint8_t, int>> table;
    table.reserve(n);
    for (int i = 0; i < n; ++i) {
        table.emplace_back(transformed[i], i);
    }

    stable_sort(table.begin(), table.end(),
                [](const pair<uint8_t, int>& a, const pair<uint8_t, int>& b) {
                    return a.first < b.first;
                });

    vector<int> T(n);
    for (int i = 0; i < n; ++i) {
        T[table[i].second] = i;
    }

    vector<uint8_t> original;
    original.reserve(n);
    int current = index;
    for (int i = 0; i < n; ++i) {
        original.push_back(transformed[current]);
        current = T[current];
    }

    reverse(original.begin(), original.end());
    return original;
}

void compress(const string& input_file, const string& output_file, int block_size) {
    if (block_size <= 0) {
        throw invalid_argument("Block size must be positive");
    }

    ifstream input(input_file, ios::binary);
    ofstream output(output_file, ios::binary);

    if (!input) throw runtime_error("Cannot open input file: " + input_file);
    if (!output) throw runtime_error("Cannot open output file: " + output_file);

    vector<uint8_t> block;
    block.reserve(block_size);

    while (true) {
        block.resize(block_size);
        input.read(reinterpret_cast<char*>(block.data()), block_size);
        streamsize bytes_read = input.gcount();
        if (bytes_read == 0) break;
        block.resize(bytes_read);

        int index;
        vector<uint8_t> transformed = bwt_transform(block, index);

        int32_t index32 = static_cast<int32_t>(index);
        int32_t size32 = static_cast<int32_t>(bytes_read);

        output.write(reinterpret_cast<const char*>(&index32), sizeof(index32));
        output.write(reinterpret_cast<const char*>(&size32), sizeof(size32));
        output.write(reinterpret_cast<const char*>(transformed.data()), transformed.size());
    }
}

void decompress(const string& input_file, const string& output_file) {
    ifstream input(input_file, ios::binary);
    ofstream output(output_file, ios::binary);

    if (!input) throw runtime_error("Cannot open input file: " + input_file);
    if (!output) throw runtime_error("Cannot open output file: " + output_file);

    while (true) {
        int32_t index32;
        input.read(reinterpret_cast<char*>(&index32), sizeof(index32));
        if (input.gcount() == 0) break;

        int32_t size32;
        input.read(reinterpret_cast<char*>(&size32), sizeof(size32));
        if (input.gcount() < sizeof(size32)) {
            throw runtime_error("Truncated block header");
        }

        int n = static_cast<int>(size32);
        if (n < 0) throw runtime_error("Invalid block size");

        vector<uint8_t> transformed(n);
        input.read(reinterpret_cast<char*>(transformed.data()), n);
        if (input.gcount() < n) {
            throw runtime_error("Truncated block data");
        }

        vector<uint8_t> original = bwt_inverse(transformed, index32);
        output.write(reinterpret_cast<const char*>(original.data()), original.size());
    }
}

int main(int argc, char* argv[]) {
    if (argc != 5) {
        cerr << "Usage: " << argv[0] << " [compress|decompress] input output block_size\n";
        return 1;
    }

    string mode = argv[1];
    string input_file = argv[2];
    string output_file = argv[3];
    int block_size = stoi(argv[4]);

    try {
        if (mode == "compress") {
            compress(input_file, output_file, block_size);
        } else if (mode == "decompress") {
            decompress(input_file, output_file);
        } else {
            cerr << "Invalid mode. Use 'compress' or 'decompress'\n";
            return 1;
        }
    } catch (const exception& e) {
        cerr << "Error: " << e.what() << endl;
        return 1;
    }

    return 0;
}