from shutil import copy
from glob import iglob
for filename in iglob('FullBuilds/Delta/**/*.xml', recursive=True):
    copy(filename,  "FullBuilds/Delta Total")