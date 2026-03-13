from glob import glob
import os.path
import random
import matplotlib.pyplot as plt
import numpy as np
filesizes = []
count = 0
for file in glob("SimulationFullBuildAll/*.xml"):
    filesizes.append(os.path.getsize(file))
    print(count)
    count += 1
    if count > 100:
        break

print(filesizes)

#group into clusters of 4
32000

class Cluster:

    def __init__(self):

    @property
    def average_size(self):
        return self.total_size / self.file_count

for size in filesizes:
