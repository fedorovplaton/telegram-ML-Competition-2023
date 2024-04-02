import gc
import os
import json
from pathlib import Path
import pandas as pd
from os.path import join as path_join
from tqdm import tqdm

roseta_data_path = Path("../data/processed/roseta_dataset.parquet")
tglanguages_path = Path("v1_tglanguages.txt")
bigcode_the_stack_path = Path("../data/processed/bigcode-the-stack.parquet")
tg_path_r = Path("../data/raw/ml2023-r1-dataset")
tg_path_d = Path("../data/raw/ml2023-d1-dataset")

# OUTPUT PATH
output_path = Path("../data/tglang_dataset/tglang_dataset_v2.parquet")

error_404 = "404: Not Found"

random_state = 138
samples_per_lang = 20000

"""
    Зазгрузим мапу tglang -> language idx
"""
with open(tglanguages_path) as f:
    tglanguages_to_idx = {tglang.strip(): idx for idx, tglang in enumerate(f.readlines())}

"""
    Зазгрузим roseta dataset
"""
roseta = pd.read_parquet(roseta_data_path)[["code", "tglang"]]
roseta = roseta[roseta["tglang"].isin(list(k for k in tglanguages_to_idx))]
roseta["target"] = roseta["tglang"].replace(tglanguages_to_idx)

print("Roseta info")
print(roseta.columns)
print(roseta.shape)
print(len(roseta["tglang"].unique()))
print(roseta["tglang"].value_counts())

"""
    Зазгрузим bigcode dataset
"""
bigcode = pd.read_parquet(bigcode_the_stack_path)[["code", "tglang"]]
bigcode = bigcode[bigcode["tglang"].isin(list(k for k in tglanguages_to_idx))]
bigcode["target"] = bigcode["tglang"].replace(tglanguages_to_idx)

bigcode = bigcode\
    .groupby("tglang")\
    .apply(lambda x: x.sample(n=min(samples_per_lang, x.shape[0]), random_state=random_state))

print("Bigcode info")
print(bigcode.columns)
print(bigcode.shape)
print(len(bigcode["tglang"].unique()))
print(bigcode["tglang"].value_counts())

"""
    Загрузим CODE для статистик
"""

data_2_add = []

for tgother_subfolder in tg_path_r.iterdir():
    if tgother_subfolder.is_dir():
        subfolder = tgother_subfolder.name

        for tgother_file in Path(path_join(tg_path_r, subfolder)).iterdir():
            if "CODE" in tgother_file.name:
                with open(tgother_file) as f:
                    data_2_add.append([f.read(), "TGLANG_LANGUAGE_OTHER", 0])

for tgother_subfolder in tg_path_d.iterdir():
    if tgother_subfolder.is_dir():
        subfolder = tgother_subfolder.name

        for tgother_file in Path(path_join(tg_path_d, subfolder)).iterdir():
            if "CODE" in tgother_file.name:
                with open(tgother_file) as f:
                    data_2_add.append([f.read(), "TGLANG_LANGUAGE_OTHER", 0])

tgcode_dataset = pd.DataFrame(data_2_add, columns=["code", "tglang", "target"])
tgcode_dataset["len"] = tgcode_dataset["code"].str.len()

import numpy as np
from scipy.stats import norm
import statistics
from numpy import random

mean = statistics.mean(tgcode_dataset["len"]) / 20
sd = statistics.stdev(tgcode_dataset["len"]) / 5
weights = norm.pdf([i for i in range(1, 4097)], mean, sd)

for i in range(len(weights)):
    weights[i] += 0.0002 - min((i / 10000000), 0.0001999999)

for i in range(20):
    weights[i] /= ((20 - i) / 1)

weights = weights / np.sum(weights)

"""
    Функция, которая семплирует длину для датасета
"""


def select_length():
    return random.choice([i for i in range(1, 4097)], 1, p=weights)[0]


"""
    Зазгрузим код из файликов
"""

code_dirs = [
    "../data/raw/git_code",
    "../data/raw/problem_languages",
    "../data/raw/sourcegraph/git"
]

total_files = 0
problem_files = 0

data_2_add = []

for code_dir in code_dirs:
    code_dir_path = Path(code_dir)

    for tglang_dir in code_dir_path.iterdir():
        if tglang_dir.is_dir():
            tglang = tglang_dir.name
            tglang_ = tglang

            if tglang not in tglanguages_to_idx:
                tglang = "TGLANG_LANGUAGE_OTHER"

            target = tglanguages_to_idx[tglang]

            for code_example_path in Path(path_join(code_dir, tglang_)).iterdir():
                total_files += 1

                try:
                    with open(code_example_path, "r") as f:
                        code_example = f.read()

                    if code_example.strip() != error_404:
                        data_2_add.append([code_example, tglang, target])

                except Exception as e:
                    problem_files += 1

custom_dataset = pd.DataFrame(data_2_add, columns=["code", "tglang", "target"])
custom_dataset = custom_dataset\
    .groupby("tglang")\
    .apply(lambda x: x.sample(n=min(samples_per_lang, x.shape[0]), random_state=random_state))

print("Custom dataset info")
print(custom_dataset.columns)
print(custom_dataset.shape)
print(len(custom_dataset["tglang"].unique()))
print(custom_dataset["tglang"].value_counts())

dataset = pd.concat([roseta, bigcode, custom_dataset])
# dataset = pd.concat([tgother_dataset, roseta, custom_dataset])
print("Dataset info")
print(dataset.columns)
print(dataset.shape)
print(len(dataset["tglang"].unique()))
print(dataset["tglang"].value_counts())

print("No data for languages:", list(filter(
    lambda x: x not in dataset["tglang"].unique(),
    list(k for k in tglanguages_to_idx)))
)

del tgcode_dataset, roseta, bigcode, custom_dataset
# del tgother_dataset, roseta, custom_dataset
gc.collect()

"""
    Нужна базовая дедупликация
"""
# ToDo

dataset = dataset.drop_duplicates()
print("Deduplicated Dataset info")
print(dataset.shape)

"""
    Нужно нарезать файлики
"""
# ToDo

snippets_cols = ["code", "tglang", "target"]
snippets_data = []

def get_indent(row: str):
    indent = 0
    for char in row:
        id = ord(char)
        if id == 9:
            indent += 4
        elif id == 32:
            indent += 1
        else:
            break
    if indent == len(row):
        return -1
    return indent

def get_parts(levels, _struct):
    result = []
    for level in levels:
        i, j = 1, 1
        while i < len(_struct) - 1:
            if _struct[i][0] == level:
                j = i + 1
                while _struct[j][0] == level and j < len(_struct) - 1:
                    if j == len(_struct) - 1:
                        print("j reaches end")
                        break
                    j += 1
                result.append([i, j - 1])

                top = _struct[i - 1][0]
                bottom = _struct[j][0]
                while bottom > top and j < len(_struct) - 1:
                    j += 1
                    bottom = _struct[j][0]

                if top < level and level != 0:
                    for k in range(i, j):
                        _struct[k][0] = top
                # else:
                #     print("wow1")
                i = j - 1
            i += 1
    return result

def sample_code(code):
    indents_ = [0] + list(map(lambda r: get_indent(r), code.split("\n"))) + [0]
    indents  = [0 for i in range(len(indents_))]

    for i in range(1, len(indents_) - 1):
        if indents_[i] == -1:
            indents[i] = max(indents_[i-1], indents_[i+1])
        else:
            indents[i] = indents_[i]

    levels = sorted(list(set(indents)), reverse=True)
    _struct = list(map(lambda ir: [ir[1], (ir[0], ir[0])], enumerate(indents)))

    rows = ("\n" + code + "\n").split("\n")
    # pprint(list(zip(indents_, _struct, map(lambda row: row[:20], rows))))

    code_parts = []
    last_high_level = 1

    for indent_, indent in zip(indents_, _struct):
        if indent_ == -1 and indent[0] == 0:
            code_parts.append([last_high_level, indent[1][0]])
            last_high_level = indent[1][0]

    try:
        code_parts += get_parts(levels, _struct)
    except Exception as e:
        print(e)
        print(code)
        print(code_parts)
        print(levels)
        print(_struct)
        print(get_parts(levels, _struct))
        exit(1)

    rows = code.split("\n")
    # for i, part in enumerate(code_parts):
    #     print(f"========={i}=========", "Num rows:", part[0])
    #     print(part[1])

    return list(map(
        lambda x: x[1],
        sorted(filter(
            lambda x: len(x[1]) > 0,
            map(
                lambda part: (part[1] - part[0] + 1, "\n".join(rows[part[0] - 1:part[1]]).strip()),
                code_parts
            )
        ))
    ))

def has_eng_letters(code):
    return any(ord(c) in range(65, 91) or ord(c) in range(97, 123) for c in code)

for row_idx, row in tqdm(dataset.reset_index().iterrows(), total=dataset.shape[0]):
    code = row["code"].strip()
    tglang = row["tglang"]
    target = row["target"]
    sampled_length = select_length()

    # if tglang != "TGLANG_LANGUAGE_TL" and tglang != "TGLANG_LANGUAGE_OTHER" and tglang != "TGLANG_LANGUAGE_FUNC":
    #     if random.random() <= 0.001:
    #         continue

    # code_lines = code.split("\n")

    tmp_idx = 0
    tmp_snippet = []
    tmp_chars = 0

    if tglang != "TGLANG_LANGUAGE_OTHER":
        # for line_idx, line in enumerate(code_lines):
        #     line_chars = len(line)
        #
        #     if tmp_chars + line_chars > sampled_length:
        #         snippets_data.append(
        #             [
        #                 "\n".join(tmp_snippet),
        #                 tglang,
        #                 target
        #             ]
        #         )
        #
        #         tmp_snippet = [line]
        #         tmp_chars = line_chars
        #         tmp_idx = line_idx
        #     else:
        #         tmp_snippet.append(line)
        #         tmp_chars += line_chars
        code_samples = sample_code(code)

        for i, sample in enumerate(code_samples):
            if ((i > 0 and len(sample) > sampled_length) or i == len(code_samples) - 1) and has_eng_letters(sample):
                snippets_data.append(
                    [
                        sample,
                        tglang,
                        target
                    ]
                )
                break
    else:
        snippets_data.append(
            [
                code,
                tglang,
                target
            ]
        )

print(len(snippets_data))

snippets = pd.DataFrame(snippets_data, columns=snippets_cols)
del dataset
gc.collect()

"""
    Нужна базовая дедупликация
"""
# ToDo

snippets = snippets.drop_duplicates()
print("Deduplicated Dataset info")
print(snippets.shape)

print("Snippets info")
print(snippets.columns)
print(snippets.shape)
print(len(snippets["tglang"].unique()))
print(snippets["tglang"].value_counts())

"""
    Семплируем
"""

snippets = snippets\
    .groupby("tglang")\
    .apply(lambda x: x.sample(n=min(samples_per_lang, x.shape[0]), random_state=random_state))\
    [["code", "target"]]\
    .reset_index()

print("Датасет для обучения леса")
print(snippets.columns)
print(snippets.shape)
print(len(snippets["tglang"].unique()))
print(snippets["tglang"].value_counts())

"""
    Для test и eval надо взять
"""


def create_map_from_tg_code_file(df):
    result = {}

    for i, row in df.iterrows():
        tglang = "TGLANG_LANGUAGE_" + row["label"]

        if tglang in tglanguages_to_idx and tglang != "TGLANG_LANGUAGE_OTHER":
            result[row["path"]] = tglang

    return result
2

mapping_r_path = Path("../data/raw/ml2023-d1-dataset-mapping/tg_code_1.csv")
mapping_r = pd.read_csv(mapping_r_path)
mapping_r = create_map_from_tg_code_file(mapping_r)

data_2_add = []

for tg_path in tg_path_r.iterdir():
    if tg_path.is_dir():
        subfolder = tg_path.name

        for tgother_file in Path(path_join(tg_path_r, subfolder)).iterdir():
            if "OTHER" in tgother_file.name:
                with open(tgother_file) as f:
                    data_2_add.append([f.read(), "TGLANG_LANGUAGE_OTHER", 0])
            else:
                code_key = tgother_file.parent.name + "/" + tgother_file.name

                if code_key in mapping_r:
                    with open(tgother_file) as f:
                        data_2_add.append([f.read(), mapping_r[code_key], tglanguages_to_idx[mapping_r[code_key]]])

mapping_d_path = Path("../data/raw/ml2023-d1-dataset-mapping/tg_code_2.csv")
mapping_d = pd.read_csv(mapping_d_path)
mapping_d = create_map_from_tg_code_file(mapping_d)

for tg_path in tg_path_d.iterdir():
    if tg_path.is_dir():
        subfolder = tg_path.name

        for tgother_file in Path(path_join(tg_path_d, subfolder)).iterdir():
            if "OTHER" in tgother_file.name:
                with open(tgother_file) as f:
                    data_2_add.append([f.read(), "TGLANG_LANGUAGE_OTHER", 0])
            else:
                code_key = tgother_file.parent.name + "/" + tgother_file.name

                if code_key in mapping_d:
                    with open(tgother_file) as f:
                        data_2_add.append([f.read(), mapping_d[code_key], tglanguages_to_idx[mapping_d[code_key]]])
                else:
                    with open(tgother_file) as f:
                        data_2_add.append([f.read(), "TGLANG_LANGUAGE_OTHER", 0])

tg_dataset = pd.DataFrame(data_2_add, columns=["code", "tglang", "target"])

from sklearn.model_selection import train_test_split

X_train, X_test, _, _ = train_test_split(
    tg_dataset,
    tg_dataset["target"],
    test_size=0.5,
    random_state=random_state,
    stratify=tg_dataset["target"]
)

X_val, X_test, _, _ = train_test_split(
    X_test,
    X_test["target"],
    test_size=0.5,
    random_state=137,
    stratify=X_test["target"]
)

for i, df in enumerate([X_train, X_val, X_test]):

    if i == 0:
        print("Train")
    if i == 1:
        print("Eval")
    if i == 2:
        print("Test")

    print(df.columns)
    print(df.shape)
    print(len(df["tglang"].unique()))
    print(df["tglang"].value_counts())


X_train.to_parquet("../data/tglang_dataset/Bin_Train.parquet", engine="pyarrow")
X_val.to_parquet("../data/tglang_dataset/Eval.parquet", engine="pyarrow")
X_test.to_parquet("../data/tglang_dataset/Test.parquet", engine="pyarrow")


# snippets.to_parquet(output_path, engine="pyarrow")

X_train_forest = pd.concat([snippets, X_train])
X_train_forest.to_parquet("../data/tglang_dataset/Forest_Train.parquet", engine="pyarrow")

pd.concat([snippets, X_train, X_val, X_test]).to_parquet(
    "../data/tglang_dataset/Production_30000.parquet", engine="pyarrow")
