import os
import json
from pathlib import Path
import requests
from tqdm import tqdm
from time import sleep


GIT_TOKEN = os.environ.get("GIT_TOKEN")
HEADERS = {
    "Authorization": f"Bearer {GIT_TOKEN}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
}
BAN_SEC = 60
MAX_PAGE = 10
PER_PAGE = 100
save_dir = Path("git_stats/")

mapping_json = "tglang_2_gitlang_mapping.json"



def get_repositories_with_lang(
        language: str, max_page: int | None = None, start_page: int = 1, per_page: int = PER_PAGE
    ):
    if max_page is None:
        max_page = float("inf")
    page = start_page
    while page <= max_page:
        query = f"language:{language}&sort=stars&order=desc&per_page={per_page}&page={page}"
        response = requests.get(
            f"https://api.github.com/search/repositories?q={query}",
            headers=HEADERS
        )
        page += 1
        if response.ok:
            repo_items = response.json().get("items")
            if repo_items is None:
                continue
            for repo_info in repo_items:
                if repo_info.get("private", True) or repo_info.get("fork", True):
                    continue
                url = repo_info["url"]
                yield dict(
                    id=repo_info["id"],
                    name=repo_info["full_name"],
                    languages=requests.get(
                        os.path.join(url, "languages"),
                        headers=HEADERS
                    ).json(),
                    contents=requests.get(
                        "/".join([url, "git/trees/master?recursive=1"]),
                        headers=HEADERS
                    ).json(),
                )
        elif response.status_code == 403:
            sleep(BAN_SEC)
        else:
            return


if __name__ == "__main__":
    with open(mapping_json, "r") as fp:
        langs_mapping: dict = json.load(fp)
        for lang_info in langs_mapping.values():
            language = lang_info["git_lang"]
            if not language:
                continue
            stats = [
                res
                for res in tqdm(
                    get_repositories_with_lang(language, max_page=MAX_PAGE),
                    desc=language,
                    total=PER_PAGE * MAX_PAGE
                )
            ]
            with open(save_dir / f"{language}.json", "w") as fp:
                json.dump(stats, fp, indent=4)
