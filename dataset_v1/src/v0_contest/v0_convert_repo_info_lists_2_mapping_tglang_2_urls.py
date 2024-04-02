import os
import json
from pathlib import Path
from pprint import pprint
import numpy as np

tglang_2_gitlang_mapping_path = Path("v0_tglang_2_gitlang_mapping.json")
tglanguages_path = Path("v0_tglanguages.txt")
repo_info_lists_root = Path("../../../ignored/repo_info_lists")

with open(tglanguages_path) as f:
    tglanguages = {tglang.strip(): idx for idx, tglang in enumerate(f.readlines())}

with open(tglang_2_gitlang_mapping_path) as f:
    tglang_2_gitlang_mapping = json.load(f)

"""
    Убираем дубликаты расширений, чтобы не ошибиться
"""

extension_2_tglang = {}

for key, value in tglang_2_gitlang_mapping.items():
    for extension in value["git_extensions"]:
        if extension not in extension_2_tglang:
            extension_2_tglang[extension] = []

        extension_2_tglang[extension].append(key)

extension_2_remove = {}
for key, value in extension_2_tglang.items():
    if len(value) > 1:
        for tglang in value:
            if tglang not in extension_2_remove:
                extension_2_remove[tglang] = []

            extension_2_remove[tglang].append(key)

# Языка, у которых не осталось расширений, нужно в ручную будет дополнить их
broke_tglangs = []

for key, value in tglang_2_gitlang_mapping.items():
    if key in extension_2_remove and len(value["git_extensions"]) <= len(extension_2_remove[key]):
        broke_tglangs.append(key)

print("broke_tglangs", broke_tglangs)

for key, value in tglang_2_gitlang_mapping.items():
    if key in extension_2_remove:
        value["git_extensions"] = list(filter(
            lambda ext: ext not in extension_2_remove[key],
            value["git_extensions"]
        ))

"""
    Строим статистики по полноте языков
"""

extension_2_tglang = {}
for key, value in tglang_2_gitlang_mapping.items():
    for extension in value["git_extensions"]:
        extension_2_tglang[extension] = key

tglang_stats = {key: 0 for key in tglang_2_gitlang_mapping.keys()}
tglang_2_urls = {}

for i, item in enumerate(repo_info_lists_root.iterdir()):
    if item.is_file():
        # Как из пути достать название языка?
        print(i, item.name)

        with open(item) as f:
            file_data = json.load(f)

            for project in file_data:
                project_name = project["name"]

                for path in project["files"]:

                    filename = path.split("/")[-1]

                    if "." in filename:
                        file_extension = "." + path.split("/")[-1].split(".")[-1]

                        if file_extension in extension_2_tglang:
                            path_tglang = extension_2_tglang[file_extension]
                            tglang_stats[path_tglang] += 1

                            url = f"https://raw.githubusercontent.com/{project_name}/master/{path}"

                            if path_tglang not in tglang_2_urls:
                                tglang_2_urls[path_tglang] = []

                            tglang_2_urls[path_tglang].append(url)

# Посемплируем до 500 ссылок

result_data = {}

for key, value in tglang_2_urls.items():
    result_data[key] = np.random.choice(value, min(500, len(value)), replace=False).tolist()

# https://pastebin.com/XfC2AaiX

with open("v0_tglang_2_urls.json", "w+") as f:
    json.dump(result_data, f, indent=2)

print("broke_tglangs", broke_tglangs)
