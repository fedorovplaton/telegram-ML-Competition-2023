#include <fstream>
#include <iostream>
#include <vector>
#include <string>

#include "transform.h"
#include "tf_idf.h"
#include "forest.h"


int main(int argc, char** argv) {
    std::string file_path = argv[1];
    std::ifstream input_file(file_path);
    if (!input_file) {
        std::cout << file_path << " doesn't exist" << std::endl;
        return 1;
    }
    
    std::string text((std::istreambuf_iterator<char>(input_file)), std::istreambuf_iterator<char>());
    input_file.close();
    
    std::vector<std::string> doc = tokenize(preprocess(text));
    std::vector<double> result = tfidf(doc);
    std::array<double, N_FEATURES> arr_res;
    std::copy(result.begin(), result.end(), arr_res.begin());

    int ans = predict(arr_res);
    std::cout << ans << std::endl;
    return 0;
}
