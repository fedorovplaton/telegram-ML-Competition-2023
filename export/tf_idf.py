import numpy as np
import json
import re
from typing import Sequence, Callable
from sklearn.feature_extraction.text import TfidfVectorizer
from pathlib import Path


def escape_string(string):
    string = string.replace("\\", "\\\\")
    string = string.replace("\"", "\\\"")
    string = string.replace("\n", "\\n")
    string = string.replace("\t", "\\t")
    string = re.sub(r"([^\x00-\x7F])", r"\\u\1", string)
    return f'"{string}"'


def convert_array_to_cpp_const(array: Sequence, c_type: str, var_name: str, func: Callable) -> str:
    return (
        f"\nconst std::vector<{c_type}> {var_name} = {{"
        +
        ", ".join(func(x) for x in array) + "};\n"
    )


def convert_tfidf_to_cpp(tf_idf: TfidfVectorizer, save_path: str):
    idf_vec = tf_idf.idf_
    voc: dict = tf_idf.vocabulary_
    word_vec = [''] * len(voc)
    for k in voc:
        word_vec[int(voc[k])] = k
    
    with open(save_path, "w") as h_file:
        h_file.write("".join([
            "#ifndef TF_IDF_H\n",
            "#define TF_IDF_H\n",
            "\n"    
            "#include <vector>\n",
            "#include <string>\n",
        ]))
        h_file.write(
            convert_array_to_cpp_const(
                idf_vec, "double", "IDF_VEC", str
            )
        )
        h_file.write(
            convert_array_to_cpp_const(
                word_vec, "std::string", "WORD_VEC", escape_string
            )
        )
        h_file.write("".join([
            "\nstd::vector<double> tfidf(const std::vector<std::string>& doc);\n"
            "\n#endif // TF_IDF_H\n"
        ]))


if __name__ == "__main__":
    import joblib
    path = "../tf_idf.pkl"
    tf_idf = joblib.load(path)
    
    convert_tfidf_to_cpp(tf_idf, "../deploy/tf_idf.h")
