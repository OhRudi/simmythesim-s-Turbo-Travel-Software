from shutil import copy
from glob import iglob
import os.path
import sys
from itertools import chain
fullbuild_tgis_to_filenames = {}
fullbuilds = 'Sims 4/SimulationFullBuildAll/'
deltabuilds_packs = 'Sims 4/SimDeltaPacks/'
deltabuilds_bg = 'Sims 4/SimDeltaBG/'

for filename in iglob('%s*.xml' % fullbuilds, recursive=True):
    tgi = os.path.basename(filename).split("!")[0:3]
    tgi_string = "!".join(tgi)
    fullbuild_tgis_to_filenames[tgi_string] = os.path.basename(filename)
overwritten_files = 0

for filename in chain(iglob('%s*.xml' % deltabuilds_packs, recursive=True), iglob('%s*.xml' % deltabuilds_bg, recursive=True)):
    tgi = os.path.basename(filename).split("!")[0:3]
    tgi_string = "!".join(tgi)
    if tgi_string in fullbuild_tgis_to_filenames:
        try:
            os.remove("{}/{}".format(fullbuilds, fullbuild_tgis_to_filenames[tgi_string]))
            overwritten_files += 1
            if overwritten_files % 100 == 0:
                print(overwritten_files)
        except Exception as e:
            print(e)
    copy(filename, fullbuilds)

            #print("File already removed")
print("Overwrote {} files.".format(overwritten_files))