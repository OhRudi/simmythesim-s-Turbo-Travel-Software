
# Put the directory of converted files here.
#pyinstaller --onefile ConvertedCopier.py
#pyinstaller --onefile GameFileCopier.py
#pyinstaller --onefile TurboTravelConverter.py



import multiprocessing

if __name__ == "__main__":
    multiprocessing.freeze_support()
    from tkinter import *
    from tkinter.filedialog import askdirectory
    from glob import glob
    import os.path
    import shutil
    import glob

    import os

    converted_prefix = "converted"


    def get_all_converted_files_in_converted_directory(path):
        return glob.glob(path)


    with open("original file locations.txt", "r") as original_paths:
        paths = original_paths.read()
        paths = paths.split("\n")


    def get_path_filename(filename):
        return filename.split(os.sep)[-1].split(".")[0]


    def get_converted_original_filename(filename):
        return filename.split("-")[0]


    def get_converted_original_extension(filename):
        return filename.split(".")[1]

    def copy_converted_files_back_to_installation():

        converted_directory = "%s\\*-converted.*" % E1.get()
        print(converted_directory)
        for converted_filename in get_all_converted_files_in_converted_directory(converted_directory):
            print(converted_filename)
            if converted_prefix in converted_filename:
                converted_file_basename = get_converted_original_filename(get_path_filename(converted_filename))
                for path in paths:
                    original_path_filename = get_path_filename(path)
                    if original_path_filename == converted_file_basename and get_converted_original_extension(
                            path) == get_converted_original_extension(converted_filename):
                        print(path, converted_filename)
                        shutil.copy2(converted_filename, os.path.dirname(path))

        for path in paths:
            try:
                if path == '':
                    continue
                print(path)
                # Remove the original file and rename the original  
                if os.path.exists(path.replace(".", "-0-converted.")):
                    os.remove(path)
                    os.rename(path.replace(".", "-0-converted."), path)
            except Exception as e:
                print(e)
        E1.delete(0, END)
        E1.insert(0, "Done copying!")

    def get_directory():
        E1.delete(0, END)
        directory = askdirectory()
        E1.insert(0, directory)


    top = Tk()
    top.title("TurboTravel File Helper")

    scalevar = IntVar()
    scalevar.set(1)


    L1 = Label(top, text="Copy Files From Another Folder to Installation Folder")
    E1 = Entry(top, width = 70)

    B = Button(top, text ="Select Directory", command = get_directory)
    b1 = Button(top,text="Copy", command = copy_converted_files_back_to_installation)

    L1.grid(row=0, column=1)
    E1.grid(row=1, column=1)

    B.grid(row=1, column=2)
    E1.grid(row=1, column=1)
    b1.grid(row=1, column=3)


    top.mainloop()