#include <fstream>
#include <vector>
#include <unordered_map>
#include <string>
#include <cstdint>
#include <stdexcept>
#include <iostream>

using namespace std;

struct Key {
    uint32_t parent;
    uint8_t symbol;

    bool operator==(const Key &other) const {
        return parent == other.parent && symbol == other.symbol;
    }
};

namespace std {
    template<> struct hash<Key> {
        size_t operator()(const Key &k) const {
            return hash<uint32_t>()(k.parent) ^ (hash<uint8_t>()(k.symbol) << 1);
        }
    };
}

void write_uint32_le(uint32_t value, ostream &out) {
    uint8_t bytes[4];
    bytes[0] = value & 0xFF;
    bytes[1] = (value >> 8) & 0xFF;
    bytes[2] = (value >> 16) & 0xFF;
    bytes[3] = (value >> 24) & 0xFF;
    out.write(reinterpret_cast<const char*>(bytes), 4);
}

uint32_t read_uint32_le(istream &in) {
    uint8_t bytes[4];
    in.read(reinterpret_cast<char*>(bytes), 4);
    if (in.gcount() != 4) {
        throw runtime_error("Unexpected end of file");
    }
    return bytes[0] | (bytes[1] << 8) | (bytes[2] << 16) | (bytes[3] << 24);
}

void compress(const string &input_filename, const string &output_filename) {
    ifstream input(input_filename, ios::binary);
    if (!input) {
        throw runtime_error("Cannot open input file for compression");
    }
    ofstream output(output_filename, ios::binary);
    if (!output) {
        throw runtime_error("Cannot open output file for compression");
    }

    vector<uint8_t> data((istreambuf_iterator<char>(input)), istreambuf_iterator<char>());
    input.close();

    uint32_t original_size = data.size();

    // Write header (original size in little-endian)
    write_uint32_le(original_size, output);

    unordered_map<Key, uint32_t> dictionary;
    uint32_t next_index = 1;
    uint32_t current_index = 0;

    for (uint8_t c : data) {
        Key key{current_index, c};
        auto it = dictionary.find(key);
        if (it != dictionary.end()) {
            current_index = it->second;
        } else {
            write_uint32_le(current_index, output);
            output.put(c);
            dictionary[key] = next_index++;
            current_index = 0;
        }
    }

    if (current_index != 0) {
        write_uint32_le(current_index, output);
        output.put(0);
    }

    output.close();
}

void decompress(const string &input_filename, const string &output_filename) {
    ifstream input(input_filename, ios::binary);
    if (!input) {
        throw runtime_error("Cannot open input file for decompression");
    }
    ofstream output(output_filename, ios::binary);
    if (!output) {
        throw runtime_error("Cannot open output file for decompression");
    }

    // Read header
    uint32_t original_size = read_uint32_le(input);

    vector<string> dictionary;
    dictionary.emplace_back(""); // Index 0 is empty string

    string output_data;

    while (true) {
        uint32_t index;
        uint8_t c;

        try {
            index = read_uint32_le(input);
        } catch (const runtime_error &e) {
            if (input.eof()) break;
            throw;
        }

        c = input.get();
        if (input.eof()) break;

        if (index >= dictionary.size()) {
            throw runtime_error("Invalid index in compressed file");
        }

        string phrase = dictionary[index];
        phrase.push_back(static_cast<char>(c));

        output_data += phrase;
        dictionary.push_back(phrase);
    }

    if (output_data.size() > original_size) {
        output_data.resize(original_size);
    }

    output.write(output_data.data(), output_data.size());
    output.close();
}

int main(int argc, char *argv[]) {
    if (argc != 4) {
        cerr << "Usage: " << argv[0] << " [compress|decompress] input_file output_file\n";
        return 1;
    }

    string mode = argv[1];
    string input_file = argv[2];
    string output_file = argv[3];

    try {
        if (mode == "compress") {
            compress(input_file, output_file);
        } else if (mode == "decompress") {
            decompress(input_file, output_file);
        } else {
            cerr << "Invalid mode. Use 'compress' or 'decompress'\n";
            return 1;
        }
    } catch (const exception &e) {
        cerr << "Error: " << e.what() << endl;
        return 1;
    }

    return 0;
}