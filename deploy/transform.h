#ifndef TRANSFORM_H
#define TRANSFORM_H

#include <array>
#include <vector>
#include <string>


std::string preprocess(std::string x);
std::vector<std::string> tokenize(std::string code_str);
// std::vector<std::string>&& tokenize(std::string&& code_str);

#endif // TRANSFORM_H
