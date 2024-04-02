import os
import json
from pathlib import Path
from pprint import pprint
import pandas as pd

v1_tglanguages_path = Path("../v1_tglanguages.txt")
dataset_languages_path = Path("programming-languages.json")
tglang_2_dataset_path = Path("tglang_2_dataset.json")

output_dataset_path = Path("../../data/processed/bigcode-the-stack.parquet")

def create_map_dataset_lang_2_tg_lang(path):
    with open(dataset_languages_path) as f:
        dataset_languages = json.load(f)

    with open(v1_tglanguages_path) as f:
        tglanguages = list(filter(lambda x: x, map(str.strip, f.read().split())))

    data = [
        ("TGLANG_LANGUAGE_CPLUSPLUS", "C++"),
        ("TGLANG_LANGUAGE_CSHARP", "C#"),
        ("TGLANG_LANGUAGE_DART", "Dart"),
        ("TGLANG_LANGUAGE_DOCKER", "Dockerfile"),
        ("TGLANG_LANGUAGE_GO", "Go"),
        ("TGLANG_LANGUAGE_JAVA", "Java"),
        ("TGLANG_LANGUAGE_JAVASCRIPT", "JavaScript"),
        ("TGLANG_LANGUAGE_KOTLIN", "Kotlin"),
        ("TGLANG_LANGUAGE_LUA", "Lua"),
        ("TGLANG_LANGUAGE_NGINX", "Nginx"),
        ("TGLANG_LANGUAGE_POWERSHELL", "PowerShell"),
        ("TGLANG_LANGUAGE_PYTHON", "Python"),
        ("TGLANG_LANGUAGE_RUBY", "Ruby"),
        ("TGLANG_LANGUAGE_RUST", "Rust"),
        ("TGLANG_LANGUAGE_SHELL", "Shell"),
        ("TGLANG_LANGUAGE_SOLIDITY", "Solidity"),
        ("TGLANG_LANGUAGE_SWIFT", "Swift"),
        ("TGLANG_LANGUAGE_TYPESCRIPT", "TypeScript")
    ]
    data = dict(data)

    for tglanguage in tglanguages:
        lang = tglanguage.split("TGLANG_LANGUAGE_")[1]

        if lang in dataset_languages:
            data[tglanguage] = lang

    lang_2_tglang = {
        u: v for v, u in data.items()
    }

    for tglanguage in tglanguages:
        if tglanguage not in data:
            print(tglanguage)

    for tglanguage in data:
        data[tglanguage] = {
            "language": data[tglanguage],
            "filenames": []
        }

    data["TGLANG_LANGUAGE_CPLUSPLUS"]["filenames"] = [
        "data/c++/train-00000-of-00214.parquet",
        "data/c++/train-00001-of-00214.parquet",
        "data/c++/train-00002-of-00214.parquet",
        # "data/c++/train-00003-of-00214.parquet",
    ]
    data["TGLANG_LANGUAGE_CSHARP"]["filenames"] = [
        "data/c-sharp/train-00000-of-00142.parquet",
        "data/c-sharp/train-00001-of-00142.parquet",
        "data/c-sharp/train-00002-of-00142.parquet",
    ]
    data["TGLANG_LANGUAGE_DART"]["filenames"] = [
        "data/dart/train-00000-of-00013.parquet",
        "data/dart/train-00001-of-00013.parquet",
        "data/dart/train-00002-of-00013.parquet"
    ]
    data["TGLANG_LANGUAGE_DOCKER"]["filenames"] = [
        "data/dockerfile/train-00000-of-00003.parquet",
        "data/dockerfile/train-00001-of-00003.parquet",
        "data/dockerfile/train-00002-of-00003.parquet"
    ]
    data["TGLANG_LANGUAGE_GO"]["filenames"] = [
        "data/go/train-00000-of-00115.parquet",
        "data/go/train-00001-of-00115.parquet",
        # "data/go/train-00002-of-00115.parquet"
    ]
    data["TGLANG_LANGUAGE_JAVA"]["filenames"] = [
        "data/java/train-00000-of-00285.parquet",
        "data/java/train-00001-of-00285.parquet",
        # "data/java/train-00002-of-00285.parquet"
    ]
    data["TGLANG_LANGUAGE_JAVASCRIPT"]["filenames"] = [
        "data/javascript/train-00000-of-00499.parquet",
        "data/javascript/train-00001-of-00499.parquet",
        # "data/javascript/train-00002-of-00499.parquet"
    ]
    data["TGLANG_LANGUAGE_KOTLIN"]["filenames"] = [
        "data/kotlin/train-00000-of-00015.parquet",
        "data/kotlin/train-00001-of-00015.parquet",
        # "data/kotlin/train-00002-of-00015.parquet"
    ]
    data["TGLANG_LANGUAGE_LUA"]["filenames"] = [
        "data/lua/train-00000-of-00008.parquet",
        "data/lua/train-00001-of-00008.parquet",
        # "data/lua/train-00002-of-00008.parquet"
    ]
    data["TGLANG_LANGUAGE_NGINX"]["filenames"] = [
        "data/nginx/train-00000-of-00001.parquet"
    ]
    data["TGLANG_LANGUAGE_POWERSHELL"]["filenames"] = [
        "data/powershell/train-00001-of-00004.parquet",
        "data/powershell/train-00002-of-00004.parquet"
    ]
    data["TGLANG_LANGUAGE_PYTHON"]["filenames"] = [
        "data/python/train-00000-of-00206.parquet",
        "data/python/train-00001-of-00206.parquet",
        # "data/python/train-00002-of-00206.parquet"
    ]
    data["TGLANG_LANGUAGE_RUBY"]["filenames"] = [
        "data/ruby/train-00000-of-00029.parquet",
        "data/ruby/train-00001-of-00029.parquet",
        # "data/ruby/train-00002-of-00029.parquet"
    ]
    data["TGLANG_LANGUAGE_RUST"]["filenames"] = [
        "data/rust/train-00000-of-00040.parquet",
        "data/rust/train-00001-of-00040.parquet",
        # "data/rust/train-00002-of-00040.parquet"
    ]
    data["TGLANG_LANGUAGE_SHELL"]["filenames"] = [
        "data/shell/train-00000-of-00011.parquet",
        "data/shell/train-00001-of-00011.parquet",
        # "data/shell/train-00002-of-00011.parquet"
    ]
    data["TGLANG_LANGUAGE_SOLIDITY"]["filenames"] = [
        "data/solidity/train-00000-of-00004.parquet",
        "data/solidity/train-00001-of-00004.parquet",
        # "data/solidity/train-00002-of-00004.parquet"
    ]
    data["TGLANG_LANGUAGE_SWIFT"]["filenames"] = [
        "data/swift/train-00000-of-00015.parquet",
        "data/swift/train-00001-of-00015.parquet",
        # "data/swift/train-00002-of-00015.parquet"
    ]
    data["TGLANG_LANGUAGE_TYPESCRIPT"]["filenames"] = [
        "data/typescript/train-00000-of-00139.parquet",
        "data/typescript/train-00001-of-00139.parquet",
        # "data/typescript/train-00002-of-00139.parquet"
    ]
    data["TGLANG_LANGUAGE_C"]["filenames"] = [
        "data/c/train-00000-of-00257.parquet",
        "data/c/train-00001-of-00257.parquet",
        # "data/c/train-00002-of-00257.parquet"
    ]
    data["TGLANG_LANGUAGE_CSS"]["filenames"] = [
        "data/css/train-00000-of-00147.parquet",
        "data/css/train-00001-of-00147.parquet",
        # "data/css/train-00002-of-00147.parquet"
    ]
    data["TGLANG_LANGUAGE_HTML"]["filenames"] = [
        "data/html/train-00000-of-00802.parquet",
        "data/html/train-00001-of-00802.parquet",
        # "data/html/train-00002-of-00802.parquet"
    ]
    data["TGLANG_LANGUAGE_JSON"]["filenames"] = [
        "data/json/train-00000-of-01329.parquet",
        "data/json/train-00001-of-01329.parquet",
        # "data/json/train-00002-of-01329.parquet"
    ]
    data["TGLANG_LANGUAGE_PHP"]["filenames"] = [
        "data/php/train-00000-of-00198.parquet",
        "data/php/train-00001-of-00198.parquet",
        # "data/php/train-00002-of-00198.parquet",
    ]
    data["TGLANG_LANGUAGE_SQL"]["filenames"] = [
        "data/sql/train-00000-of-00021.parquet",
        "data/sql/train-00001-of-00021.parquet",
        # "data/sql/train-00002-of-00021.parquet"
    ]
    data["TGLANG_LANGUAGE_XML"]["filenames"] = [
        "data/xml/train-00000-of-00297.parquet",
        "data/xml/train-00001-of-00297.parquet",
        # "data/xml/train-00002-of-00297.parquet"
    ]

    with open(path, "w+") as file:
        json.dump(data, file, indent=2)

    return data, lang_2_tglang


if __name__ == "__main__":
    tglang_2_dataset, lang_2_tglang = create_map_dataset_lang_2_tg_lang(tglang_2_dataset_path)
    pprint(tglang_2_dataset)
    pprint(lang_2_tglang)

    from huggingface_hub import hf_hub_download

    for tglang in tglang_2_dataset:
        local_pathes = []

        if len(tglang_2_dataset[tglang]["filenames"]) > 0:
            for filename in tglang_2_dataset[tglang]["filenames"]:
                print(tglang, filename)

                # if tglang == "TGLANG_LANGUAGE_CPLUSPLUS":
                local_path = hf_hub_download(
                    repo_id="bigcode/the-stack",
                    filename=filename,
                    repo_type="dataset",
                    token="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"
                )
                local_pathes.append(local_path)
        tglang_2_dataset[tglang]["local_pathes"] = local_pathes
    pprint(tglang_2_dataset)

    dataset = pd.DataFrame({"tglang": [], "code": []})

    for tglang in tglang_2_dataset:
        total = 0
        local_pathes = tglang_2_dataset[tglang]["local_pathes"]

        if len(local_pathes) == 0:
            print(tglang, "0 Files")
            continue

        language_df = pd.DataFrame({"lang": [], "content": []})

        for path in local_pathes:
            df_tmp = pd.read_parquet(path)[["lang", "content"]]
            language_df = pd.concat([language_df, df_tmp])

        language_df = language_df.sample(n=min(40000, language_df.shape[0]), random_state=137)
        language_df["lang"] = language_df["lang"].replace(lang_2_tglang)
        language_df = language_df.rename(columns={"lang": "tglang", "content": "code"})
        language_df = language_df[["tglang", "code"]]

        dataset = pd.concat([dataset, language_df])
        print(tglang, language_df.shape)

    print(dataset["tglang"].unique())
    dataset.to_parquet(output_dataset_path, engine="pyarrow")

"""

Problem languages

TGLANG_LANGUAGE_OTHER
TGLANG_LANGUAGE_FUNC
TGLANG_LANGUAGE_OBJECTIVE_C
TGLANG_LANGUAGE_TL

TGLANG_LANGUAGE_NGINX (15, 2)

TGLANG_LANGUAGE_CPLUSPLUS (40000, 2)
TGLANG_LANGUAGE_CSHARP (40000, 2)
TGLANG_LANGUAGE_DART (40000, 2)
TGLANG_LANGUAGE_DOCKER (40000, 2)
TGLANG_LANGUAGE_GO (40000, 2)
TGLANG_LANGUAGE_JAVA (40000, 2)
TGLANG_LANGUAGE_JAVASCRIPT (40000, 2)
TGLANG_LANGUAGE_KOTLIN (40000, 2)
TGLANG_LANGUAGE_LUA (40000, 2)
TGLANG_LANGUAGE_POWERSHELL (40000, 2)
TGLANG_LANGUAGE_PYTHON (40000, 2)
TGLANG_LANGUAGE_RUBY (40000, 2)
TGLANG_LANGUAGE_RUST (40000, 2)
TGLANG_LANGUAGE_SHELL (40000, 2)
TGLANG_LANGUAGE_SOLIDITY (40000, 2)
TGLANG_LANGUAGE_SWIFT (40000, 2)
TGLANG_LANGUAGE_TYPESCRIPT (40000, 2)
TGLANG_LANGUAGE_C (40000, 2)
TGLANG_LANGUAGE_CSS (40000, 2)
TGLANG_LANGUAGE_HTML (40000, 2)
TGLANG_LANGUAGE_JSON (40000, 2)
TGLANG_LANGUAGE_PHP (40000, 2)
TGLANG_LANGUAGE_SQL (40000, 2)
TGLANG_LANGUAGE_XML (40000, 2)

"""
