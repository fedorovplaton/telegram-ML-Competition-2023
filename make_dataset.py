import os
import json
from pathlib import Path
import pandas as pd
from os.path import join as path_join

roseta_data_path = Path("datasets/roseta/raw/roseta_dataset.parquet")
tglanguages_path = Path("tglanguages.txt")

error_404 = "404: Not Found"

with open(tglanguages_path) as f:
    tglanguages_to_idx = {tglang.strip(): idx for idx, tglang in enumerate(f.readlines())}

dataset = pd.read_parquet(roseta_data_path)[["code", "key", "tglang"]]

print(dataset.columns)
print(dataset.shape)
print(len(dataset["tglang"].unique()))

code_dirs = [
    "ignored/git_code",
    "datasets/problem_languages/raw"
]

total_files = 0
problem_files = 0

data_2_add = []

for code_dir in code_dirs:
    code_dir_path = Path(code_dir)

    for tglang_dir in code_dir_path.iterdir():
        if tglang_dir.is_dir():

            tglang = tglang_dir.name
            tglang_key = tglanguages_to_idx[tglang]

            for code_example_path in Path(path_join(code_dir, tglang)).iterdir():
                total_files += 1

                try:
                    with open(code_example_path, "r") as f:
                        code_example = f.read()

                    if code_example.strip() != error_404:
                        data_2_add.append([code_example, tglang_key, tglang])

                except Exception as e:
                    problem_files += 1

dataset = pd.concat([
    dataset,
    pd.DataFrame(
        data_2_add,
        columns=dataset.columns
    )
])

print(dataset.columns)
print(dataset.shape)
print(len(dataset["tglang"].unique()))

print("total_files", total_files)
print("problem_files", problem_files)

dataset.to_parquet("datasets/final/dataset_v0.parquet")
