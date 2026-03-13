from shutil import copy
from glob import iglob

for filename in iglob('FullBuilds\Full/**/*.xml', recursive=True):
    copy(filename,  "FullBuilds/Full Total")
#Fix overlapping things