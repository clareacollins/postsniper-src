import os, json
from pathlib import Path as path

root = str(path(os.getcwd()).parent)

LoginData = json.load(open(f"{root}\\src\\redacted_info.json", "r"))