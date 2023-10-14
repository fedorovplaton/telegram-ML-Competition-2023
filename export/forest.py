from sklearn.ensemble import RandomForestClassifier
from pathlib import Path
import numpy as np
from typing import List, Dict


FIELD_TO_NAME_C_TYPE: Dict[str, str] = dict(
    children_left=("allLeftChildren", "int"),
    children_right=("allRightChildren", "int"),
    threshold=("allThresholds", "double"),
    feature=("allIndices", "int"),
    value=("allClasses", "unsigned char"),
)

def compress_value_array(value: np.ndarray):
    value = np.squeeze(value, axis=(1,)).astype(np.int8)
    value = value.argmax(-1)
    return value


def get_values_from_forest(forest: RandomForestClassifier, field: str, dtype: type = int) -> List[np.ndarray]:
    return [
        dtree.tree_.__getattribute__(field).astype(dtype)
        for dtree in forest[:1]
    ]


def convert_array_to_cpp_const(array: List[np.ndarray], c_type: str, var_name: str) -> str:
    assert len(array[0].shape) == 1
    max_len = max(len(a) for a in array)
    code_lines = [f"const std::vector<std::array<{c_type}, {max_len}>> {var_name} = {{"]
    
    for arr in array:
        code_lines.append(
            f"    {{{', '.join([str(val) for val in arr.tolist()] + ['0'] * (max_len - len(arr)) )}}},"
        )
    code_lines.append("};")
    
    return "\n".join(code_lines)


def convert_param_to_cpp(forest: RandomForestClassifier, field: str, dtype: type = int):
    var_name, c_type = FIELD_TO_NAME_C_TYPE[field]
    arr_list = get_values_from_forest(forest, field, dtype)
    if field == "value":
        arr_list = list(map(compress_value_array, arr_list))
    code = convert_array_to_cpp_const(arr_list, c_type, var_name)
    
    return "\n".join([
        f"#ifndef {field.upper()}_H",
        f"#define {field.upper()}_H",
        "\n", 
        "#include <vector>",
        "#include <array>",
        code,
        f"\n#endif // {field.upper()}_H\n"
    ])


def make_param_files(forest: RandomForestClassifier, save_dir: Path):
    save_dir.mkdir(511, 1, 1)
    for field in FIELD_TO_NAME_C_TYPE:
        save_path = save_dir / f"{field}.h"
        dtype = np.float64 if field == "threshold" else int
        with open(save_path, "w") as file:
            file.write(convert_param_to_cpp(forest, field, dtype))



if __name__ == "__main__":
    import joblib
    forest = joblib.load("../forest.pkl")
    make_param_files(forest, Path("../deploy/"))