#include "tglang.h"

#include <stdlib.h>
#include <string.h>

#include "transform.h"
#include "tf_idf.h"
#include "forest.h"

#include <fstream>
#include <iostream>
#include <chrono>

enum TglangLanguage tglang_detect_programming_language(const char *text) {
  std::vector<std::string> doc = tokenize(std::move(preprocess(std::string(text))));
  std::array<double, N_FEATURES> result = tfidf(doc);
  return static_cast<TglangLanguage>(predict(result));
}

// int main(int argc, char** argv) {
//     // std::cout << "start\n";
//     std::string file_path = argv[1];
//     std::ifstream file(file_path);


//     if (file) {
//         file.seekg(0, std::ios::end);
//         std::streampos fileSize = file.tellg();
//         file.seekg(0, std::ios::beg);

//         // Выделяем соответствующий размер памяти для хранения текста
//         char* text = new char[fileSize + 1];

//         // Читаем текст из файла
//         file.read(text, fileSize);
//         file.close();
//         text[fileSize] = '\0'; // Добавляем завершающий нулевой символ

//         TglangLanguage lang = tglang_detect_programming_language(text);
//         std::cout << lang << std::endl;
//         // Закрываем файл и освобождаем память
//         delete[] text;
        
//     } else {
//         std::cout << "Не удалось открыть файл!" << std::endl;
//     }

//     return 0;
// }