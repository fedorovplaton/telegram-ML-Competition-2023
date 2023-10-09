import pandas as pd
from pprint import pprint

df = pd.read_parquet("0000.parquet")

"""
    Достаем языки из roseta
"""
roseta_langs = set(map(str.lower, df["language_name"].unique()))

"""
    Достаем языки из tglang
"""

tglangs_raw_languages="""
TGLANG_LANGUAGE_OTHER
TGLANG_LANGUAGE_1S_ENTERPRISE
TGLANG_LANGUAGE_ABAP
TGLANG_LANGUAGE_ACTIONSCRIPT
TGLANG_LANGUAGE_ADA
TGLANG_LANGUAGE_APACHE_GROOVY
TGLANG_LANGUAGE_APEX
TGLANG_LANGUAGE_APPLESCRIPT
TGLANG_LANGUAGE_ASP
TGLANG_LANGUAGE_ASSEMBLY
TGLANG_LANGUAGE_AUTOHOTKEY
TGLANG_LANGUAGE_AWK
TGLANG_LANGUAGE_BASIC
TGLANG_LANGUAGE_BATCH
TGLANG_LANGUAGE_BISON
TGLANG_LANGUAGE_C
TGLANG_LANGUAGE_CLOJURE
TGLANG_LANGUAGE_CMAKE
TGLANG_LANGUAGE_COBOL
TGLANG_LANGUAGE_COFFESCRIPT
TGLANG_LANGUAGE_COMMON_LISP
TGLANG_LANGUAGE_CPLUSPLUS
TGLANG_LANGUAGE_CRYSTAL
TGLANG_LANGUAGE_CSHARP
TGLANG_LANGUAGE_CSS
TGLANG_LANGUAGE_CSV
TGLANG_LANGUAGE_D
TGLANG_LANGUAGE_DART
TGLANG_LANGUAGE_DELPHI
TGLANG_LANGUAGE_DOCKER
TGLANG_LANGUAGE_ELIXIR
TGLANG_LANGUAGE_ELM
TGLANG_LANGUAGE_ERLANG
TGLANG_LANGUAGE_FIFT
TGLANG_LANGUAGE_FORTH
TGLANG_LANGUAGE_FORTRAN
TGLANG_LANGUAGE_FSHARP
TGLANG_LANGUAGE_FUNC
TGLANG_LANGUAGE_GAMS
TGLANG_LANGUAGE_GO
TGLANG_LANGUAGE_GRADLE
TGLANG_LANGUAGE_GRAPHQL
TGLANG_LANGUAGE_HACK
TGLANG_LANGUAGE_HASKELL
TGLANG_LANGUAGE_HTML
TGLANG_LANGUAGE_ICON
TGLANG_LANGUAGE_IDL
TGLANG_LANGUAGE_INI
TGLANG_LANGUAGE_JAVA
TGLANG_LANGUAGE_JAVASCRIPT
TGLANG_LANGUAGE_JSON
TGLANG_LANGUAGE_JULIA
TGLANG_LANGUAGE_KEYMAN
TGLANG_LANGUAGE_KOTLIN
TGLANG_LANGUAGE_LATEX
TGLANG_LANGUAGE_LISP
TGLANG_LANGUAGE_LOGO
TGLANG_LANGUAGE_LUA
TGLANG_LANGUAGE_MAKEFILE
TGLANG_LANGUAGE_MARKDOWN
TGLANG_LANGUAGE_MATLAB
TGLANG_LANGUAGE_NGINX
TGLANG_LANGUAGE_NIM
TGLANG_LANGUAGE_OBJECTIVE_C
TGLANG_LANGUAGE_OCAML
TGLANG_LANGUAGE_OPENEDGE_ABL
TGLANG_LANGUAGE_PASCAL
TGLANG_LANGUAGE_PERL
TGLANG_LANGUAGE_PHP
TGLANG_LANGUAGE_PL_SQL
TGLANG_LANGUAGE_POWERSHELL
TGLANG_LANGUAGE_PROLOG
TGLANG_LANGUAGE_PROTOBUF
TGLANG_LANGUAGE_PYTHON
TGLANG_LANGUAGE_QML
TGLANG_LANGUAGE_R
TGLANG_LANGUAGE_RAKU
TGLANG_LANGUAGE_REGEX
TGLANG_LANGUAGE_RUBY
TGLANG_LANGUAGE_RUST
TGLANG_LANGUAGE_SAS
TGLANG_LANGUAGE_SCALA
TGLANG_LANGUAGE_SCHEME
TGLANG_LANGUAGE_SHELL
TGLANG_LANGUAGE_SMALLTALK
TGLANG_LANGUAGE_SOLIDITY
TGLANG_LANGUAGE_SQL
TGLANG_LANGUAGE_SWIFT
TGLANG_LANGUAGE_TCL
TGLANG_LANGUAGE_TEXTILE
TGLANG_LANGUAGE_TL
TGLANG_LANGUAGE_TYPESCRIPT
TGLANG_LANGUAGE_UNREALSCRIPT
TGLANG_LANGUAGE_VALA
TGLANG_LANGUAGE_VBSCRIPT
TGLANG_LANGUAGE_VERILOG
TGLANG_LANGUAGE_VISUAL_BASIC
TGLANG_LANGUAGE_WOLFRAM
TGLANG_LANGUAGE_XML
TGLANG_LANGUAGE_YAML
"""
tglang_langs = set()
tglang_langs_indexes = {}
for idx, row in enumerate(tglangs_raw_languages.split()):
    row = row.strip()
    lang = row.split("TGLANG_LANGUAGE_")[1].lower()
    tglang_langs.add(lang)
    tglang_langs_indexes[row] = idx

"""
    Вручную что-то смапим
"""
custom_mapper = {
    "c++": "cplusplus",
    "visual basic": "visual_basic",
    "c_sharp": "csharp",
    "objective-c": "objective_c",
    "groovy": "apache_groovy",
    "common lisp": "common_lisp",
    "coffeescript": "coffescript",
    "pl/sql": "pl_sql",
    "f#": "fsharp"
}

"""
    Поиск языков, которые не удалось автоматически смапить
"""
mapped_languages = tglang_langs.intersection(roseta_langs)
custom_mapped_languages = set(custom_mapper.values())

problem_languages = tglang_langs.difference(mapped_languages.union(custom_mapped_languages))

"""
    Если нужно поискать, чтобы вручную что-то добавить
"""
# import Levenshtein
# for problem_language in problem_languages:
#
#     print("")
#     print("problem_language:", problem_language)
#
#     friends = sorted([
#         (Levenshtein.distance(problem_language, lang), lang) for lang in roseta_langs
#     ])[:10]
#
#     print(friends)

"""
    Итоговая мапа
"""

result_mapping = custom_mapper.copy()

for lang in mapped_languages:
    result_mapping[lang] = lang

result_mapping = {
    key: "TGLANG_LANGUAGE_" + value.upper() for (key, value) in result_mapping.items()
}

result_mapping = {
    key: (value, tglang_langs_indexes[value]) for (key, value) in result_mapping.items()
}

mapping_rosetalang_2_tglang = {key: value[0] for (key, value) in result_mapping.items()}
mapping_rosetalang_2_index = {key: value[1] for (key, value) in result_mapping.items()}

# print(df.head(2))

"""
    Собираем датасет
"""

dataset = df[["code", "language_name"]]
dataset["language_name"] = dataset["language_name"].map(str.lower)
dataset["key"] = dataset["language_name"].map(mapping_rosetalang_2_index)
dataset["tglang"] = dataset["language_name"].map(mapping_rosetalang_2_tglang)
dataset = dataset.dropna()
dataset["key"] = dataset["key"].astype(int)

dataset.to_parquet("roseta_dataset.parquet")

print("")
print("")
print("")

print(f"Нет {len(problem_languages)} языков")
print(problem_languages)

print("Колонки датасета")
print(list(dataset.columns))

print("")
print("Пример")
print(dataset.head(1))

print("")
print("Кол-во")

for key, value in dataset["language_name"].value_counts().items():
    print(key, value)
