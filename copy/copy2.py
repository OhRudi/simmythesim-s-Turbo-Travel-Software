from shutil import copy
from glob import iglob

thresholds = [400, 800, 3200, 1200]

current_threshold = 0
for filename in iglob('Full/**/*.xml', recursive=True):
    copy(filename, "C:\\Users\\Theo\\Documents\\GitHub\\DBPF-Reader\\Everything")

