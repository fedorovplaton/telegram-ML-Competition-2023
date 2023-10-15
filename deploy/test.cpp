#include <fstream>
#include <iostream>
#include <vector>
#include <string>
#include <chrono>

#include "transform.h"
#include "tf_idf.h"
#include "forest.h"


int main(int argc, char** argv) {
    // std::cout << "start\n";
    std::string file_path = argv[1];
    std::ifstream input_file(file_path);
    if (!input_file) {
        std::cout << file_path << " doesn't exist" << std::endl;
        return 1;
    }
    // std::cout << "reading done\n";
    std::string text((std::istreambuf_iterator<char>(input_file)), std::istreambuf_iterator<char>());
    input_file.close();
    
    std::vector<std::string> doc = tokenize(preprocess(text));
    // std::cout << "tokenization done\n";
    std::vector<double> result = tfidf(doc);
    // std::cout << "TF-IDF done\n";
    std::array<double, N_FEATURES> arr_res;
    std::copy(result.begin(), result.end(), arr_res.begin());
    // std::cout << "start predict\n";
    int ans = predict(arr_res);
    // std::cout << ans << std::endl;

    int K = 100;

    auto startTime = std::chrono::high_resolution_clock::now();

    for (int i = 0; i < K; ++i) {
        doc = tokenize(preprocess(text));
        result = tfidf(doc);
        std::copy(result.begin(), result.end(), arr_res.begin());
        ans = predict(arr_res);
    }

    auto endTime = std::chrono::high_resolution_clock::now();

    auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(endTime - startTime).count();

    std::cout << "Время работы цикла: " << duration << " миллисекунд" << std::endl;

    double averageDuration = duration / static_cast<double>(K);

    std::cout << "Среднее время работы цикла: " << averageDuration << " миллисекунд" << std::endl;

    return 0;
}
