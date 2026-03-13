from glob import iglob
import shutil
import os
#EA_Sims_3_folder = "C:\\Program Files (x86)\\Origin Games\\The Sims 3"



#worlds = get_all_files_in_EA_matching_this("**/*.{}".format(world_extension))
#object_caches = get_all_files_in_EA_matching_this("**/*.{}".format(objectCache_extension))

import multiprocessing
if __name__ == "__main__":
    multiprocessing.freeze_support()
    from tkinter import *
    from tkinter.filedialog import askdirectory
    import os.path

    def get_installation_directory():
        E2.delete(0, END)
        directory = askdirectory()
        E2.insert(0, directory)

    def get_directory():
        E1.delete(0, END)
        directory = askdirectory()
        E1.insert(0, directory)


    def copy_files():
        global progress

        EA_Sims_3_folder = E2.get()
        EA_Sims_3_pack_deltas_folder = "{}{}GameData\\Shared\\DeltaPackages".format(EA_Sims_3_folder, os.sep)
        EA_Sims_3_pack_BG_deltas_folder = "{}{}GameData\\Shared\\Packages".format(EA_Sims_3_folder, os.sep)

        package_extension = "package"
        objectCache_extension = "objectCache"
        world_extension = "world"

        def get_all_files_in_EA_matching_this(pattern):
            return list(iglob(EA_Sims_3_folder + os.sep + pattern, recursive=True))

        def get_all_files_in_pack_deltas_matching_this(pattern):
            return list(iglob(EA_Sims_3_pack_deltas_folder + os.sep + pattern, recursive=True))

        def get_all_files_in_pack_BG_deltas_matching_this(pattern):
            return list(iglob(EA_Sims_3_pack_BG_deltas_folder + os.sep + pattern, recursive=True))


        fullbuilds = get_all_files_in_EA_matching_this("**/{}*.{}".format("Full", package_extension))
        deltabuilds = get_all_files_in_pack_deltas_matching_this("**/{}*.{}".format("Delta", package_extension))
        bg_deltas = get_all_files_in_pack_BG_deltas_matching_this("**/{}*.{}".format("Delta", package_extension))
        all_files = fullbuilds + deltabuilds + bg_deltas

        print(all_files)

        with open("original file locations.txt", "w") as settings:
            paths = ""
            for file in all_files:
                shutil.copy2(file, E1.get())
                paths += file + "\n"
            settings.write(paths)

        E1.delete(0, END)
        E1.insert(0, "Done copying!")


    top = Tk()
    top.title("TurboTravel Helper - Copy Files From Installation to Another Folder")

    L2 = Label(top, text="Where is the Sims 3 Installation Folder?")
    E2 = Entry(top, width = 70)

    L1 = Label(top, text="Where to put copied files?")
    E1 = Entry(top, width = 70)

    B = Button(top, text ="Select Directory", command = get_directory)
    B2 = Button(top, text ="Select Directory", command = get_installation_directory)

    b1 = Button(top, text="Copy Files", command = copy_files)

    L2.grid(row=0, column=1)
    E2.grid(row=1, column=1)

    B2.grid(row=1, column=2)

    L1.grid(row=2, column=1)
    E1.grid(row=3, column=1)

    B.grid(row=3, column=2)
    b1.grid(row=4, column=1)


    top.mainloop()

