# -*- coding: utf-8 -*-
# @Author: Lennart Keidel
# @Date:   2019-12-04 16:16:21
# @Last Modified by:   Lennart Keidel
# @Last Modified time: 2019-12-04 16:16:21
from dbpf.dbpf_parser import DBPFParser
from dbpf.dbpf_writer import DBPFWriter

TYPICAL_RANDOM_READ_SSD_PER_SECOND = 552000000  # 552 MB/s


class DBPFConverter:
    def __init__(self, package_name, extension, cpu_cores):
        self.package_name = package_name
        self.extension = extension
        self.dbpf_parser = DBPFParser(package_name, extension, cpu_cores)
        dbpf_header, splits, datas = self.dbpf_parser.read_package()
        print("Splits {}".format(splits))
        count = 0
        while count < len(splits) - 1:
            self.dbpf_writer = DBPFWriter(package_name + "-{}".format(count), extension, dbpf_header, splits[count], splits[count + 1])
            deleted_files = []
            self.dbpf_writer.prepare_resources()

            print(self.dbpf_writer.index_header)
            #Each index entry is 32 bytes large, and the index header itself starts with 4 bytes
            self.dbpf_writer.write_header(splits[count+1]-splits[count], 32*len(self.dbpf_writer.index_header)+4)
            for idx in range(splits[count], splits[count+1]):
                if idx not in deleted_files:
                    self.dbpf_writer.write_resource_data(datas[idx])
                else:
                    print("Idx {} is deleted Size {}".format(idx, len(datas[idx])))
            print("Current size, {} current reported size {}".format(self.dbpf_writer.byteWriter.opened_file.tell(), self.dbpf_writer.current_data_position))
            self.dbpf_writer.write_index()
            self.dbpf_writer.byteWriter.close_file()
            count += 1
        #self.dbpf_writer.

if __name__ == "__main__":
    import cProfile
    from glob import glob
    pr = cProfile.Profile()
    pr.enable()
    files = glob("C:\\Users\\Theo\\Documents\\Converted Files\\*.package")
    for file in files:
        if file.endswith(".objectCache"):
            dbpf_converter = DBPFConverter(file.split(".objectCache")[0], "objectCache", 8)
        elif file.endswith(".package"):
            dbpf_converter = DBPFConverter(file.split(".package")[0], "package", 8)
        else:
            raise Exception("File not recognized")
    pr.disable()

    import pstats
    stats = pstats.Stats(pr).sort_stats('cumtime')
    stats.print_stats()