from shutil import copy
from glob import iglob

count = 0
for filename in iglob('world/**/*.xml', recursive=True):
    if "B6C8B6A0!" in filename:
        count += 1
        copy(filename, "dds")

print("There are {} textures".format(count))