import os, json
from pathlib import Path as path

root = str(path(os.getcwd()).parent)

target = f"{root}\\target.txt"

img = f"{root}\\in\\img"

post = f"{root}\\in\\preview"

inline = f"{root}\\in\\il"

LoginData = json.load(open(f"{root}\\redacted_info.json", "r"))