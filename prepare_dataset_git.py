import os
import json
from pathlib import Path

tglang_2_gitlang_mapping_path = Path("tglang_2_gitlang_mapping.json")
tglanguages_path = Path("tglanguages.txt")
source_code_root = Path("")

with open(tglanguages_path) as f:
    tglanguages = {tglang.strip(): idx for idx, tglang in enumerate(f.readlines())}

with open(tglang_2_gitlang_mapping_path) as f:
    tglang_2_gitlang_mapping = json.load(f)

"""
    Не факт, что будет работать, ибо есть дубликаты в расширения

    ToDo Убрать дубликаты расширений из tglang_2_gitlang_mapping
"""
# extension_2_tglang_mapping = {}
# for tglang, meta in tglang_2_gitlang_mapping:
#     for extension in meta["git_extensions"]:
#         extension_2_tglang_mapping[extension] = tglang

for item in source_code_root.iterdir():
    if item.is_file():
        # Как из пути достать название языка?
        print(item)
