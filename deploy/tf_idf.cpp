#include <iostream>
#include <vector>
#include <unordered_map>
#include <cmath>
#include <regex>
#include <string>
#include <algorithm>

#include <fstream>
#include <iostream>

#include "tf_idf.h"


double tf(const std::string& t_, const std::unordered_map<std::string, int>& doc, int doc_len) {
    if (doc.count(t_) > 0) {
        return static_cast<double>(doc.at(t_)) / doc_len;
    }
    return 0.0;
}

std::array<double, N_FEATURES> tfidf(const std::vector<std::string>& doc) {
    int doc_len = doc.size();
    std::unordered_map<std::string, int> map_doc;
    for (const std::string& t : doc) {
        map_doc[t] += 1;
    }
    std::array<double, N_FEATURES> res;
    // res.reserve(WORD_VEC.size());
    for (size_t i = 0; i < WORD_VEC.size(); i++) {
        // double tf_val = tf(WORD_VEC[i], map_doc, doc_len);
        // double idf_val = IDF_VEC[i];
        res[i] = IDF_VEC[i] * tf(WORD_VEC[i], map_doc, doc_len);
    }
    double l2 = 0.0;
    for (double val : res) {
        l2 += val * val;
    }
    l2 = std::sqrt(l2);
    for (double & val : res) {
        val /= l2;
    }
    return res;
}
