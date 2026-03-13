import shutil
import os

with open("original file locations.txt", "r") as original_paths:
    paths = original_paths.read()
    paths = paths.split("\n")


for path in paths:
    try:
        if path == '':
            continue
        print(path)
        shutil.copy(path.replace(".", "-0-converted."), path)
        os.remove(path.replace(".", "-0-converted."))
    except Exception as e:
        print(e)
print(paths)