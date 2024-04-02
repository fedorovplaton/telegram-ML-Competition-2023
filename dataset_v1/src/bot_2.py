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
LANGS = ['CPLUSPLUS', 'JAVA', 'CSS', 'OBJECTIVE_C', 'GO', 'NGINX', 'LUA', 'KOTLIN', 'DOCKER', 'JAVASCRIPT', 'PYTHON', 'SHELL', 'SOLIDITY', 'HTML', 'RUST', 'PHP', 'DART', 'C', 'TYPESCRIPT', 'SWIFT', 'SQL', 'TL', 'POWERSHELL', 'JSON', 'FUNC', 'XML', 'RUBY', 'CSHARP', 'OTHER']
request_template = "\n".join([
    f"You must answer with ONLY ONE 'word', an element from this list: {LANGS}",
    "Under no circumstances should you write anything other than one word from the list above. Try to choose the most suitable one, if nothing fits, send in response the last element of the list - 'OTHER'.",
    "Your task is to guess in which programming language from those presented this piece of code is written:",
    "If your answer is even one character different from the correct element from the list, I will suffer terribly for many days.",
    "```\n{}\n```",
    # "If enone of the languages in the list is suitable, write `OTHER`. UNDER NO CIRCUMSTANCES WRITE ANYTHING BUT ONE WORD. IT MUST BE AN ELEMENT FROM THE LIST UP TO EACH CHARACTER."
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

def read_file(path):
    with open(path, "r") as f:
        return f.read(), path

def get_text(path):
    df = pd.read_csv(path)
    df = df[df["label"] == "ERROR"]
    return [
        list(read_file(p)) for p in df["path"] 
    ]

def main():
    start_num = int(argv[1]) if len(argv) > 1 else 0
    # dir_1 = "/home/kama/pythonProjects/telegram-ML-Competition-2023/datasets/test/"
    save_dir = "/Users/platon.fedorov/Documents/telegram-ML-Competition-2023/dataset_v1/data/processed/докачка"
    samples = get_text("/Users/platon.fedorov/Documents/telegram-ML-Competition-2023/dataset_v1/data/raw/докачка/merged_2_platon.csv")
    print(len(samples))
    d = 10
    
    pb = tqdm(total=len(samples) - start_num + 1)
    for k in range(start_num, len(samples), d):
        try:
            df = make_files(samples[k:k+d], k, pb)
            df.to_csv(f"{save_dir}/{k+d}.csv")
        except Exception as e:
            print("sleep 5 sec")
            sleep(5)
            continue

if __name__ == "__main__":
    main()