#include <regex>  // for std::regex_replace
#include <string> // for std::string
#include <vector>
#include <algorithm>

#include <fstream>
#include <iostream>

#include "tf_idf.h"


const std::regex pattern1(R"(\b([A-Za-z])\1+\b)");
const std::regex pattern2(R"(\b[A-Za-z]\b)");
const std::regex regex_pattern(R"(\b[A-Za-z_]\w*\b|[!\#\$%\&\*\+:\-\./<=>\?@\\\^_\|\~]+|[ \t\(\),;\{\}\[\]`"'])");

std::string preprocess(std::string x) {
    x = std::regex_replace(x, pattern1, "");
    x = std::regex_replace(x, pattern2, "");
    std::transform(x.begin(), x.end(), x.begin(), ::tolower);
    return x;
}

std::vector<std::string> tokenize(std::string code_str) {
    std::smatch matches;
    
    std::vector<std::string> tokens;
    
    while (std::regex_search(code_str, matches, regex_pattern)) {
        tokens.push_back(matches.str());
        code_str = matches.suffix();
    }
    
    return tokens;
}
