import openai
import os
import pandas as pd
from tqdm import tqdm
from sys import argv
from time import sleep
from typing import List


def walk_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if os.path.splitext(file)[0][-4:] != "CODE":
                continue
            file_path = os.path.join(root, file)
            with open(file_path, "r") as f:
                content = f.read()
            yield (content, file_path)


openai.api_key = "sk-MnfCqdar69XGVc4pC5D0A5Bc3b7348CfBbC7E5Bf86B74109"
openai.api_base = "https://neuroapi.host/v1"
LANGS = ['CPLUSPLUS', 'JAVA', 'CSS', 'OBJECTIVE_C', 'GO', 'NGINX', 'LUA', 'KOTLIN', 'DOCKER', 'JAVASCRIPT', 'PYTHON',
         'SHELL', 'SOLIDITY', 'HTML', 'RUST', 'PHP', 'DART', 'C', 'TYPESCRIPT', 'SWIFT', 'SQL', 'TL', 'POWERSHELL',
         'JSON', 'FUNC', 'XML', 'RUBY', 'CSHARP']
request_template = "\n".join([
    f"Here is a list of programming language names: {LANGS}",
    "You must determine in which language from the given list the following code is written:",
    "```\n{}\n```",
    "In response, write ONLY the most suitable line from the list. If none of the languages in the list is suitable, write `OTHER`. Don't write ANYTHING anymore."
])


def get_content(request: str) -> str:
    chat_completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": request}],
        stream=False,
    )

    if isinstance(chat_completion, dict):
        # not stream
        return chat_completion.choices[0].message.content
    else:
        res = []
        for token in chat_completion:
            content = token["choices"][0]["delta"].get("content")
            if content != None:
                res.append(content)
        return "".join(res)


def make_files(samples: list, start: int, pb: tqdm):
    results = []
    for code, file_path in samples:
        label = get_content(request_template.format(code))
        results.append([file_path, label])
        pb.update()
    return pd.DataFrame(results, columns=["path", "label"])


def main():
    start_num = int(argv[1]) if len(argv) > 1 else 0
    dir_1 = "/Users/platon.fedorov/Documents/telegram-ML-Competition-2023/dataset_v1/data/raw/ml2023-d1-dataset"
    save_dir = "/Users/platon.fedorov/Documents/telegram-ML-Competition-2023/dataset_v1/data/processed/ml2023-d1-dataset"
    samples = list(walk_directory(dir_1))
    d = 10

    pb = tqdm(total=len(samples) - start_num + 1)
    for k in range(start_num, len(samples), d):
        try:
            df = make_files(samples[k:k + d], k, pb)
            df.to_csv(f"{save_dir}/{k + d}.csv")
        except Exception as e:
            print("sleep 5 sec")
            sleep(5)
            continue


if __name__ == "__main__":
    main()
