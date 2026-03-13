from glob import iglob
import shutil
import os
EA_Sims_3_folder = "C:\\Program Files (x86)\\Origin Games\\The Sims 3"
converted_folder = "C:\\Users\\Theo\\Documents\\Converted Files"

package_extension = "package"
objectCache_extension = "objectCache"
world_extension = "world"

def get_all_files_in_EA_matching_this(pattern):
    return list(iglob(EA_Sims_3_folder + os.sep + pattern, recursive=True))

worlds = get_all_files_in_EA_matching_this("**/*.{}".format(world_extension))
#object_caches = get_all_files_in_EA_matching_this("**/*.{}".format(objectCache_extension))
fullbuilds = get_all_files_in_EA_matching_this("**/{}*.{}".format("Full", package_extension))
deltabuilds = get_all_files_in_EA_matching_this("**/{}*.{}".format("Delta", package_extension))

all_files = fullbuilds + deltabuilds + worlds
print(all_files)


with open("original file locations.txt", "w") as settings:
    paths = ""
    for file in all_files:
        paths += file + "\n"
    settings.write(paths)
