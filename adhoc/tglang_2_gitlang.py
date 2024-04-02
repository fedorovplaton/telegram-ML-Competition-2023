import yaml
import json

tglangs_text = """
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

with open('gitlangs.yml', 'r') as file:
    gitlangs = yaml.safe_load(file)

gitlangs_data = {}
for key, value in gitlangs.items():
    if "extensions" not in value and "filenames" not in value:
        gitlangs_data[key.lower()] = {
            "name": key,
            "type": value["type"],
            "extensions": []
        }

        continue

    gitlangs_data[key.lower()] = {
        "name": key,
        "type": value["type"],
        "extensions": value["extensions"] if "extensions" in value \
            else list(filter(lambda s: s.startswith("."), value["filenames"]))
    }

mapping = {
    "TGLANG_LANGUAGE_OTHER": {
        "git_lang": "",
        "git_type": "",
        "git_extensions": []
    },
    "TGLANG_LANGUAGE_1S_ENTERPRISE": {
        "git_lang": "1C Enterprise",
        "git_type": "programming",
        "git_extensions": [".bsl", ".os"]
    },
    "TGLANG_LANGUAGE_APACHE_GROOVY": {
        "git_lang": "Groovy",
        "git_type": "programming",
        "git_extensions": [".groovy", ".grt", ".gtpl", ".gvy"]
    },
    "TGLANG_LANGUAGE_ASP": {
        "git_lang": "Classic ASP",
        "git_type": "programming",
        "git_extensions": [".asp"]
    },
    "TGLANG_LANGUAGE_BATCH": {
        "git_lang": "Batchfile",
        "git_type": "programming",
        "git_extensions": [".bat", ".cmd"]
    },
    "TGLANG_LANGUAGE_COFFESCRIPT": {
        "git_lang": "CoffeeScript",
        "git_type": "programming",
        "git_extensions": [".coffee", "._coffee", ".cake", ".cjsx", ".iced"]
    },
    "TGLANG_LANGUAGE_COMMON_LISP": {
        "git_lang": "Common Lisp",
        "git_type": "programming",
        "git_extensions": [".lisp", ".asd", ".cl", ".l", ".lsp", ".ny", ".podsl", ".sexp"]
    },
    "TGLANG_LANGUAGE_CPLUSPLUS": {
        "git_lang": "C++",
        "git_type": "programming",
        "git_extensions": [".cpp", ".c++", ".cc", ".cp", ".cxx", ".h", ".h++", ".hpp", ".hxx", ".inc", ".inl", ".ino",
                           ".ipp", ".re", ".tcc", ".tpp"]
    },
    "TGLANG_LANGUAGE_CSHARP": {
        "git_lang": "C#",
        "git_type": "programming",
        "git_extensions": [".cs", ".cake", ".csx", ".linq"]
    },
    "TGLANG_LANGUAGE_DELPHI": {
        "git_lang": "Component Pascal",
        "git_type": "programming",
        "git_extensions": [".cp", ".cps"]
    },
    "TGLANG_LANGUAGE_DOCKER": {
        "git_lang": "Dockerfile",
        "git_type": "programming",
        "git_extensions": [".dockerfile"]
    },
    "TGLANG_LANGUAGE_FSHARP": {
        "git_lang": "F#",
        "git_type": "programming",
        "git_extensions": [".fs", ".fsi", ".fsx"]
    },
    "TGLANG_LANGUAGE_LATEX": {
        "git_lang": "TeX",
        "git_type": "markup",
        "git_extensions": [".tex", ".aux", ".bbx", ".cbx", ".cls", ".dtx", ".ins", ".lbx", ".ltx", ".mkii", ".mkiv",
                           ".mkvi", ".sty", ".toc"]
    },
    "TGLANG_LANGUAGE_OBJECTIVE_C": {
        "git_lang": "Objective-C",
        "git_type": "programming",
        "git_extensions": [".m", ".h"]
    },
    "TGLANG_LANGUAGE_OPENEDGE_ABL": {
        "git_lang": "OpenEdge ABL",
        "git_type": "programming",
        "git_extensions": [".p", ".cls", ".w"]
    },
    "TGLANG_LANGUAGE_PL_SQL": {
        "git_lang": "PLSQL",
        "git_type": "programming",
        "git_extensions": [".pls", ".bdy", ".ddl", ".fnc", ".pck", ".pkb", ".pks", ".plb", ".plsql", ".prc", ".spc",
                           ".sql", ".tpb", ".tps", ".trg", ".vw"]
    },
    "TGLANG_LANGUAGE_PROTOBUF": {
        "git_lang": "Protocol Buffer",
        "git_type": "data",
        "git_extensions": [".proto"]
    },
    "TGLANG_LANGUAGE_REGEX": {
        "git_lang": "Regular Expression",
        "git_type": "data",
        "git_extensions": [".regexp", ".regex"]
    },
    "TGLANG_LANGUAGE_TL": {
        "git_lang": "Type Language",
        "git_type": "data",
        "git_extensions": [".tl"]
    },
    "TGLANG_LANGUAGE_VISUAL_BASIC": {
        "git_lang": "VBA",
        "git_type": "programming",
        "git_extensions": [".bas", ".cls", ".frm", ".frx", ".vba"]
    },
    "TGLANG_LANGUAGE_FIFT": {
        "git_lang": "",
        "git_type": "",
        "git_extensions": []
    },
    "TGLANG_LANGUAGE_FUNC": {
        "git_lang": "",
        "git_type": "",
        "git_extensions": []
    },
    "TGLANG_LANGUAGE_ICON": {
        "git_lang": "",
        "git_type": "",
        "git_extensions": []
    },
    "TGLANG_LANGUAGE_KEYMAN": {
        "git_lang": "",
        "git_type": "",
        "git_extensions": []
    },
    "TGLANG_LANGUAGE_LISP": {
        "git_lang": "",
        "git_type": "",
        "git_extensions": []
    },
    "TGLANG_LANGUAGE_LOGO": {
        "git_lang": "",
        "git_type": "",
        "git_extensions": []
    },
    "TGLANG_LANGUAGE_WOLFRAM": {
        "git_lang": "",
        "git_type": "",
        "git_extensions": []
    }
}
problem_langs = []
warning_langs = []

for tglang in tglangs_text.split("\n"):
    tglang = tglang.strip()

    if len(tglang) == 0:
        continue

    tglang_name = tglang.split("TGLANG_LANGUAGE_")[1].lower()

    if tglang in mapping:
        continue

    if tglang_name in gitlangs_data:

        if gitlangs_data[tglang_name]["type"] == "":
            warning_langs.append(tglang)
        if (gitlangs_data[tglang_name]["extensions"]) == 0:
            warning_langs.append(tglang)

        mapping[tglang] = {
            "git_lang": gitlangs_data[tglang_name]["name"],
            "git_type": gitlangs_data[tglang_name]["type"],
            "git_extensions": gitlangs_data[tglang_name]["extensions"],
        }
    else:
        problem_langs.append(tglang)

print(len(problem_langs))
print(problem_langs)

print(len(mapping))

with open("v0_tglang_2_gitlang_mapping.json", "w+") as file:
    json.dump(mapping, file, indent=4)
