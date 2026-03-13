import shutil
import glob
import sys
import os

# Put the directory of converted files here.


converted_prefix = "converted"

def get_all_converted_files_in_converted_directory():
    return glob.glob("Converted Files\\*.*")


with open("Settings.settings", "r") as original_paths:
    paths = original_paths.read()
    paths = paths.split("\n")


def get_path_filename(filename):
    return filename.split(os.sep)[-1].split(".")[0]

def get_converted_original_filename(filename):
    return filename.split("-")[0]

def get_converted_original_extension(filename):
    return filename.split(".")[1]

print("Overwriting the following packages in the install directory...")
yes = input("Are you sure? Enter yes to continue.")
if yes != "yes":
    sys.exit()


for converted_filename in get_all_converted_files_in_converted_directory():
    print(converted_filename)
    if converted_prefix in converted_filename:
        converted_file_basename = get_converted_original_filename(get_path_filename(converted_filename))
        for path in paths:
            original_path_filename = get_path_filename(path)
            if original_path_filename == converted_file_basename and get_converted_original_extension(path) == get_converted_original_extension(converted_filename):
                print(path, converted_filename)
                shutil.copy2(converted_filename, os.path.dirname(path))
                break
