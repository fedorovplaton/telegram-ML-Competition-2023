import os
import json
from pathlib import Path
from pprint import pprint
from os.path import join as path_join
import numpy as np

import requests
import io
import concurrent.futures


tglang_2_urls_path = Path("v0_tglang_2_urls.json")
save_root = Path("../../data/raw/git_code")


def create_if_not_exists(path: Path):
    if not path.exists():
        os.makedirs(path)


create_if_not_exists(save_root)

with open(tglang_2_urls_path) as f:
    tglang_2_urls = json.load(f)


def download_file(root, idx, url):
    file_name = f"{idx}.txt"
    file_path = path_join(root, file_name)
    response = requests.get(url)

    open(file_path, 'wb').write(response.content)


for tglang, urls in tglang_2_urls.items():
    print(tglang)

    tglang_root = path_join(save_root, tglang)
    create_if_not_exists(Path(tglang_root))

    with concurrent.futures.ThreadPoolExecutor() as exector:
        args = ((tglang_root, idx, url) for idx, url in enumerate(urls))
        exector.map(lambda p: download_file(*p), args)
