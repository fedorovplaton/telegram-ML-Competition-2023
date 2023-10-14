from sklearn.ensemble import RandomForestClassifier
from pathlib import Path
import numpy as np
from typing import List, Dict


FIELD_TO_NAME_C_TYPE: Dict[str, str] = dict(
    children_left=("allLeftChildren", "int"),
    children_right=("allRightChildren", "int"),
    threshold=("allThresholds", "double"),
    feature=("allIndices", "int"),
    value=("allClasses", "int"),
)


def get_values_from_forest(forest: RandomForestClassifier, field: str) -> List[np.ndarray]:
    res = [
        dtree.tree_.__getattribute__(field)
        for dtree in forest
    ]
    if field == "value":
        res = [np.squeeze(arr, axis=(1,)).astype(int) for arr in res]
    return res


def convert_array_to_cpp_const(array: List[np.ndarray], c_type: str, var_name: str) -> str:
    dim = len(array[0].shape) + 1
    code_lines = [f"const {'std::vector<' * dim}{c_type}{'>' * dim} {var_name} = {{"]
    if dim == 2:
        for arr in array:
            code_lines.append(
                f"    {{{', '.join(str(val) for val in arr.tolist())}}},"
            )
    else:
        for arr in array:
            sub_vectors = [
                f"{{{', '.join([str(val) for val in row.tolist()])}}}"
                for row in arr
            ]
            code_lines.append("    {" + ", ".join(sub_vectors) + "},")
    code_lines.append("};")
    
    return "\n".join(code_lines)


def convert_forest_to_cpp(forest: RandomForestClassifier, save_path: Path) -> None:
    code_blocks = (
        convert_array_to_cpp_const(
            get_values_from_forest(forest, field),
            c_type,
            var_name
        )
        for field, (var_name, c_type) in FIELD_TO_NAME_C_TYPE.items()
    )
    with open(save_path, "w") as h_file:
        h_file.write("".join([
            "#ifndef FOREST_PARAMS_H\n",
            "#define FOREST_PARAMS_H\n",
            "\n"    
            "#include <vector>\n",
            "\n"
        ]))
        for block in code_blocks:
            h_file.write(block)
        h_file.write("\n\n#endif // FOREST_PARAMS_H\n")


if __name__ == "__main__":
    import joblib
    forest = joblib.load("../forest.pkl")
    # val = forest[0].tree_.value
    # print(convert_array_to_cpp_const(val, "int", "allClasses")[:100])
    convert_forest_to_cpp(forest, "../deploy/forest_params.h")
