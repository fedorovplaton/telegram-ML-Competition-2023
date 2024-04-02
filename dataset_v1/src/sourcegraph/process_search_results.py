
import os
import json
from pathlib import Path
import pandas as pd
from os.path import join as path_join
import requests
import requests
import io
import concurrent.futures

pathes = [
    Path("../../data/raw/sourcegraph/search_results/TGLANG_LANGUAGE_TL.csv"),
    Path("../../data/raw/sourcegraph/search_results/TGLANG_LANGUAGE_NGINX.csv"),
    Path("../../data/raw/sourcegraph/search_results/TGLANG_LANGUAGE_OBJECTIVE_C.csv")
]


def create_if_not_exists(path: Path):
    if not path.exists():
        os.makedirs(path)


def download_file(root, idx, url):
    file_name = f"{idx}.txt"
    file_path = path_join(root, file_name)
    response = requests.get(url)

    if idx % 1000 == 0:
        print(idx)

    if response.status_code == 200:
        open(file_path, 'wb').write(response.content)


for path in pathes:
    tglang = path.name.split("/")[-1].split(".")[0]
    output_root = path_join("../../data/raw/sourcegraph/git", tglang)

    print(tglang)

    df = pd.read_csv(path, index_col=False, on_bad_lines="skip")
    df = df[df["Repository"].str.startswith("github.com")]

    urls = []

    for idx, (repo, filepath) in df[["Repository", "File path"]].iterrows():
        repo = repo.split("github.com")[1]
        urls.append(
            "https://raw.githubusercontent.com" + path_join(repo, "master", filepath)
        )

    create_if_not_exists(Path(output_root))

    with concurrent.futures.ThreadPoolExecutor() as exector:
        args = ((output_root, idx, url) for idx, url in enumerate(urls))
        exector.map(lambda p: download_file(*p), args)
