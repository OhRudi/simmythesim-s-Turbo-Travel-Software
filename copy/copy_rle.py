from shutil import copy
from glob import iglob

count = 0
for filename in iglob('world/**/*.xml', recursive=True):
    if "BA856C78!" in filename:
        count += 1
        copy(filename, "rles")

print("There are {} textures".format(count))