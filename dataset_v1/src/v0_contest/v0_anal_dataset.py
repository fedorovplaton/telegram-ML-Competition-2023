import os
import json
from pathlib import Path
import pandas as pd
from os.path import join as path_join
from pprint import pprint

dataset = pd.read_parquet("../../../datasets/final/dataset_v0.parquet")

tglanguages_path = Path("v0_tglanguages.txt")

with open(tglanguages_path) as f:
    tglanguages_to_idx = {tglang.strip(): idx for idx, tglang in enumerate(f.readlines())}

for tglang in dataset["tglang"].unique():
    snippets = sum(
        map(
            lambda code: max(1, len(code) // 4096),
            dataset[dataset["tglang"] == tglang]["code"].tolist()
        )
    )

    if snippets < 200:
        print(tglang, len(dataset[dataset["tglang"] == tglang]), snippets)

print(
    "Языки про которые ничгео не знаем:", set(tglanguages_to_idx.keys()).difference(set(dataset["tglang"].unique()))
)
