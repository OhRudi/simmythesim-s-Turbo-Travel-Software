from helpers.file_structure.disc import DiscInstall
from helpers.file_structure.settings import Settings
from helpers.copier import Copier
from helpers.file_structure.sims3_registry_paths import packs
import sys
import os
if __name__ == "__main__":
    settings = Settings()
    dst_folder = "Converted Files\\"
    print("The following pack files will be copied over to this folder. \nAre you sure? Enter 'yes' to continue!")
    for pack in packs:
        disc = DiscInstall()
        pack_installed = disc.find_install_directory(pack)
        if pack_installed:
            print("Pack: {}".format(pack))

    if input().lower() != "yes":
        sys.exit()
    if not os.path.exists("Converted Files"):
        os.mkdir("Converted Files")
    files_copied = []
    for pack in packs:

        disc = DiscInstall()
        pack_installed = disc.find_install_directory(pack)
        if pack_installed:
            print("Copying over pack {} files".format(pack))
            convertable_files = disc.get_convertable_files()
            settings.create(convertable_files)
            for file in convertable_files:
                if file in files_copied:
                    print("Not copying {} as it already has been copied.".format(file))
                else:
                    files_copied.append(file)
                    Copier(file, dst_folder)
                    print("Copied {}!".format(file.split("\\")[-1]))

    settings.write("Settings")
