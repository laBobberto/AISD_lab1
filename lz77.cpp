#include <iostream>
#include <fstream>
#include <vector>
#include <cstdint>
#include <string>
#include <algorithm>

using namespace std;


struct Token {
    uint16_t offset;  // расстояние до начала найденного совпадения в окне
    uint8_t length;   // длина совпадения
    char next;        // следующий символ после совпадения
    bool isLast;      // если true, то токен завершающий и поле next не используется
};

vector<Token> compress(const string& input, int windowSize, int lookaheadBufferSize) {
    vector<Token> tokens;
    size_t i = 0;
    while(i < input.size()) {
        int bestLength = 0;
        int bestOffset = 0;
        int start = (i >= windowSize) ? i - windowSize : 0;
        for (int j = start; j < i; j++) {
            int length = 0;
            while (length < lookaheadBufferSize && i + length < input.size() &&
                   input[j + length] == input[i + length]) {
                length++;
            }
            if(length > bestLength) {
                bestLength = length;
                bestOffset = i - j;
            }
        }
        Token token;
        if(i + bestLength < input.size()){
            token.offset = (bestLength > 0) ? bestOffset : 0;
            token.length = bestLength;
            token.next = input[i + bestLength];
            token.isLast = false;
            tokens.push_back(token);
            i += bestLength + 1;
        } else {
            token.offset = (bestLength > 0) ? bestOffset : 0;
            token.length = bestLength;
            token.next = 0;
            token.isLast = true;
            tokens.push_back(token);
            i += bestLength;
        }
    }
    return tokens;
}


string decompress(const vector<Token>& tokens) {
    string output;
    for (const auto& token : tokens) {
        if(token.length > 0) {
            int pos = output.size() - token.offset;
            for (int i = 0; i < token.length; i++) {
                output.push_back(output[pos + i]);
            }
        }
        if(!token.isLast) {
            output.push_back(token.next);
        }
    }
    return output;
}

int main(int argc, char* argv[]) {
    if (argc != 6) {
        cerr << "Использование: " << argv[0] << " <compress|decompress> <input_file> <output_file> <window_size> <lookahead_buffer_size>\n";
        return 1;
    }

    string mode = argv[1];
    string inputFile = argv[2];
    string outputFile = argv[3];
    int windowSize = stoi(argv[4]);
    int lookaheadBufferSize = stoi(argv[5]);

    // Чтение входного файла
    ifstream in(inputFile, ios::binary);
    if (!in) {
        cerr << "Не удалось открыть входной файл " << inputFile << "\n";
        return 1;
    }
    string inputData((istreambuf_iterator<char>(in)), istreambuf_iterator<char>());
    in.close();

    if (mode == "compress") {
        vector<Token> tokens = compress(inputData, windowSize, lookaheadBufferSize);

        ofstream out(outputFile, ios::binary);
        if (!out) {
            cerr << "Не удалось создать файл " << outputFile << "\n";
            return 1;
        }
        uint32_t tokenCount = tokens.size();
        out.write(reinterpret_cast<const char*>(&tokenCount), sizeof(tokenCount));
        for (const auto& token : tokens) {
            out.write(reinterpret_cast<const char*>(&token.offset), sizeof(token.offset));
            out.write(reinterpret_cast<const char*>(&token.length), sizeof(token.length));
            out.write(&token.next, sizeof(token.next));
            out.write(reinterpret_cast<const char*>(&token.isLast), sizeof(token.isLast));
        }
        out.close();
    } else if (mode == "decompress") {
        ifstream inCompressed(inputFile, ios::binary);
        if (!inCompressed) {
            cerr << "Не удалось открыть файл " << inputFile << "\n";
            return 1;
        }
        uint32_t tokenCount;
        inCompressed.read(reinterpret_cast<char*>(&tokenCount), sizeof(tokenCount));
        vector<Token> tokens(tokenCount);
        for (uint32_t i = 0; i < tokenCount; i++) {
            Token token;
            inCompressed.read(reinterpret_cast<char*>(&token.offset), sizeof(token.offset));
            inCompressed.read(reinterpret_cast<char*>(&token.length), sizeof(token.length));
            inCompressed.read(&token.next, sizeof(token.next));
            inCompressed.read(reinterpret_cast<char*>(&token.isLast), sizeof(token.isLast));
            tokens[i] = token;
        }
        inCompressed.close();

        string decompressedData = decompress(tokens);

        ofstream out(outputFile, ios::binary);
        if (!out) {
            cerr << "Не удалось создать файл " << outputFile << "\n";
            return 1;
        }
        out.write(decompressedData.data(), decompressedData.size());
        out.close();
    } else {
        cerr << "Неверный режим. Используйте 'compress' или 'decompress'.\n";
        return 1;
    }

    return 0;
}