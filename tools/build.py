import os

files = os.listdir("src/")

try:
    files.remove("boot.py")
    files.remove("LICENSE")
    files.remove("main.py")
    files.remove("README.md")
    files.remove("sha.json")
except ValueError:
    pass

files = sorted(files)

import shutil
for f in files:
    shutil.copyfile('src/'+f, 'build/'+f)
