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
    std::array<double, N_FEATURES> result = tfidf(doc);
    int ans = predict(result);
    // std::cout << ans << std::endl;

    int K = 100;

    auto startTime = std::chrono::high_resolution_clock::now();

    for (int i = 0; i < K; ++i) {
        doc = tokenize(preprocess(text));
        result = tfidf(doc);
        ans = predict(result);
    }

    auto endTime = std::chrono::high_resolution_clock::now();

    auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(endTime - startTime).count();

    std::cout << "Время работы цикла: " << duration << " миллисекунд" << std::endl;

    double averageDuration = duration / static_cast<double>(K);

    std::cout << "Среднее время работы цикла: " << averageDuration << " миллисекунд" << std::endl;

    return 0;
}
