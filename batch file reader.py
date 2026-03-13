from glob import iglob
from dbpf.dbpf_parser import DBPFParser
import random
import os
if __name__ == "__main__":

    SIMS2_CONVERSION = False
    total_files = 0

 #   pool = ThreadPool(4)
    filenames = []
    extensions = []



    for filename_with_directory in iglob("Sims 4 All Packs/" + '**/*.*', recursive=True):
        filename = filename_with_directory.split(".")[0]
        extension = filename_with_directory.split(".")[1]
        #if "Strings_" in filename or "thumbnails" in filename or "magalog" in filename:
         #   continue

        filename_only = os.path.basename(filename_with_directory)
        lowercase_filename = filename_only.lower()

        valid = True
        if SIMS2_CONVERSION:
            for object_count in range(9+1):
                object_filename = "Objects{}.package".format("{}".format(object_count).zfill(2))
                if filename_only == object_filename:
                    valid = True
                    break

            for sim_count in range(13+1):
                sim_filename = "Sims{}.package".format("{}".format(sim_count).zfill(2))
                if filename_only == sim_filename:
                    valid = True
                    break

            lowercase_filename_with_directory = filename_with_directory.lower()
            if "ui" in lowercase_filename or "skin" in lowercase_filename or "text" in lowercase_filename_with_directory or "ui" in lowercase_filename_with_directory \
                or "wants" in lowercase_filename_with_directory or "skins" in lowercase_filename_with_directory or "thumbnails" in lowercase_filename_with_directory or "collections" in lowercase_filename_with_directory \
                or "material" in lowercase_filename_with_directory or "neighborhood" in lowercase_filename_with_directory:
                valid = False



        if not valid:
            continue

        if extension == "package" or extension == "objectCache" or extension == "world":
            filenames.append(filename)
            extensions.append(extension)

    combined = list(zip(filenames, extensions))
    random.shuffle(combined)

    filenames[:], extensions[:] = zip(*combined)
    print(filenames)

    for i in range(len(filenames)):
        filename = filenames[i]
        extension = extensions[i]
        DBPFParser.uncompress_file(None, filename, extension, optimizeFiles=True)
        print("{}% complete".format(round(((i + 1) / len(filenames))* 100, 4)))

   # pool.starmap(, zip(filenames, extensions,))
   # pool.close()
   # pool.join()

