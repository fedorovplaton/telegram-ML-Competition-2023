#include <regex>  // for std::regex_replace
#include <string> // for std::string
#include <vector>
#include <algorithm>

#include <fstream>
#include <iostream>

#include "tf_idf.h"

std::string preprocess(std::string x) {
    std::regex pattern1(R"(\b[A-Za-z]\b)");          // regex pattern for removing single letters
    std::regex pattern2(R"(\b([A-Za-z])\1+\b)");     // regex pattern for removing repeating letters

    x = std::regex_replace(x, pattern2, "");         // remove repeating letters
    x = std::regex_replace(x, pattern1, "");         // remove single letters
    std::transform(x.begin(), x.end(), x.begin(), ::tolower);
    return x;
}


std::vector<std::string> tokenize(std::string code_str) {
    std::regex regex_pattern(R"(\b[A-Za-z_]\w*\b|[!\#\$%\&\*\+:\-\./<=>\?@\\\^_\|\~]+|[ \t\(\),;\{\}\[\]`"'])");
    std::smatch matches;
    
    std::vector<std::string> tokens;
    
    while (std::regex_search(code_str, matches, regex_pattern)) {
        tokens.push_back(matches.str());
        code_str = matches.suffix();
    }
    
    return tokens;
}


int main() {
    std::ifstream input_file("../samples/input.txt");
    if (!input_file) {
        std::cout << "file input.txt doesn't exist" << std::endl;
        return 1;
    }
    
    std::string text((std::istreambuf_iterator<char>(input_file)), std::istreambuf_iterator<char>());
    input_file.close();
    
    std::vector<std::string> doc = tokenize(preprocess(text));
    std::vector<double> result = tfidf(doc);
    
    for (size_t i = 0; i < result.size(); i++) {
        if (result[i] != 0) {
            std::cout << "(" << i << ", " << result[i] << ") ";
        }
    }
    std::cout << std::endl;
    return 0;
}