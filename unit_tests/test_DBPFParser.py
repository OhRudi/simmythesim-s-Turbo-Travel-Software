import hashlib
import unittest
from unittest import TestCase

from dbpf.dbpf_parser import DBPFParser
from dbpf.helpers import decompress_data


class EmptySims4TestParser(TestCase):
    def setUp(self):
        # Load test data
        self.dbpf_parser = DBPFParser("Unit Test Files/sims4empty", "package")
        self.dbpf_parser.setup_file_reader()

    def test_read_dbpf_header(self):
        return self.assertEqual(self.dbpf_parser.read_dbpf_magic_number(), b'DBPF')

    def test_read_version_number(self):
        return self.assertEqual(self.dbpf_parser.read_version_number(), (2, 1, 0, 0))

    def test_read_flags_and_date_stamp(self):
        return self.assertEqual(self.dbpf_parser.read_flags_and_date_stamp(), (0, 0, 0))

    def test_read_index_and_holes(self):
        index_size = 16
        index_position_ts4 = 96
        index_minor_version = 3
        return self.assertEqual(self.dbpf_parser.read_index_and_holes(),
                                (0, 0, 0, index_size, 0, 0, 0, index_minor_version, index_position_ts4))

    def test_read_index_flags(self):
        return self.assertEqual(self.dbpf_parser.read_index_flags(96), (1, 1, 1, 0, 0, 0, 16))

    #  def test_read_index_entries(self):
    #  return self.assertEqual(self.dbpf_parser.read_index_entries(96+4, 0, 0, 0, 0), [])

    def tearDown(self):
        self.dbpf_parser.byteReader.close_file()



class OneFileSims4TestParser(EmptySims4TestParser):
    def setUp(self):
        # Load test data
        self.dbpf_parser = DBPFParser("Unit Test Files/sims4onefile", "package")
        self.dbpf_parser.setup_file_reader()

    def test_read_index_and_holes(self):
        index_size = 36
        index_position_ts4 = 121
        index_minor_version = 3
        entry_count = 1
        return self.assertEqual(self.dbpf_parser.read_index_and_holes(),
                                (0, entry_count, 0, index_size, 0, 0, 0, index_minor_version, index_position_ts4))

    def test_read_index_flags(self):
        return self.assertEqual(self.dbpf_parser.read_index_flags(121), (0, 0, 0, 0, 0, 0, 4))

    def test_read_index_entries(self):
        results = self.dbpf_parser.read_index_entries(121 + 4, 1, 0, 0, 0, 0, 0, 0, 4 - 4)
        expected_position = 96
        self.assertEqual(results[0].get_values(),
                         (62078431, 2147483648, 148365759, 622275963, expected_position, [25, 1], 25, [0, 1]))
        return

    def test_read_data(self):
        index_sizes_and_locations = [(96, 25)]
        data = self.dbpf_parser.read_data(index_sizes_and_locations)
        self.assertEqual(data, [b'Will I ever make a sound?'])



class ActualSims4FileTests(EmptySims4TestParser):
    def setUp(self):
        # Load test data
        self.dbpf_parser = DBPFParser("Unit Test Files/sims4actual", "package")
        self.dbpf_parser.setup_file_reader()

    def test_read_index_and_holes(self):
        index_size = 412588
        index_position_ts4 = 985552250
        index_minor_version = 3
        entry_count = 14735
        return self.assertEqual(self.dbpf_parser.read_index_and_holes(),
                                (0, entry_count, 0, index_size, 0, 0, 0, index_minor_version, index_position_ts4))

    def test_read_index_flags(self):
        return self.assertEqual(self.dbpf_parser.read_index_flags(985552250), (0, 1, 0, 0, 0, 0, 8))

    def test_read_index_entries(self):
        results = self.dbpf_parser.read_index_entries(985552250 + 4, 14735, 0, 1, 0, 0, 0, 0, 8 - 4)
        print(results[0].location, results[0].compressed_size[0])
        for result in results:
            self.assertIsNot(result.location, 0)
            self.assertIsNot(result.compressed_size[0], 0)
            self.assertIsNot(result.uncompresessed_size, 0)

            self.assertLessEqual(result.compressed_size[0], result.uncompresessed_size)
        return

    def test_read_data(self):
        self.assertIsNot(self.dbpf_parser.read_data([(175143705, 249822)]), "")

    def test_read_package_file(self):
        results = self.dbpf_parser.read_header_and_datas()
        self.fail("Placeholder")

class OneFileCompressedSims4Test(EmptySims4TestParser):
    def setUp(self):
        # Load test data
        self.dbpf_parser = DBPFParser("Unit Test Files/sims4compressedfile", "package")
        self.dbpf_parser.setup_file_reader()

    def test_read_index_and_holes(self):
        index_size = 36
        index_position_ts4 = 1430
        index_minor_version = 3
        entry_count = 1
        return self.assertEqual(self.dbpf_parser.read_index_and_holes(),
                                (0, entry_count, 0, index_size, 0, 0, 0, index_minor_version, index_position_ts4))

    def test_read_index_flags(self):
        return self.assertEqual(self.dbpf_parser.read_index_flags(1430), (1, 1, 1, 62078431, 2147483648, 148365759, 16))

    def test_read_index_entries(self):
        results = self.dbpf_parser.read_index_entries(1430 + 4, 1, 1, 1, 1, 62078431, 2147483648, 148365759, 16 - 4)
        expected_position = 96
        compressed_flag = 23106
        decompressed_size = 3346
        compressed_size = 1334
        self.assertEqual(results[0].get_values(),
                         (62078431, 2147483648, 148365759, 622275963, expected_position, [compressed_size, 1],
                          decompressed_size, [compressed_flag, 1]))
        return

    def test_decompress_data(self):
        from unit_tests.constants import filler_text_hash
        compressed_size = 1334
        decompressed_size = 3346

        index_sizes_and_locations = [(96, compressed_size)]
        data = self.dbpf_parser.read_data(index_sizes_and_locations)
        uncompressed_data = decompress_data(data[0], True, decompressed_size)
        m = hashlib.sha256()
        m.update(uncompressed_data)
        uncompressed_data_hash = m.hexdigest()
        print(uncompressed_data_hash)
        self.assertEqual(uncompressed_data_hash, filler_text_hash)


class ActualSims3FileTests(EmptySims4TestParser):
    def setUp(self):
        # Load test data
        self.dbpf_parser = DBPFParser("Unit Test Files/sims3actual", "package")
        self.dbpf_parser.setup_file_reader()

    def test_read_version_number(self):
        return self.assertEqual(self.dbpf_parser.read_version_number(), (2, 0, 0, 0))

    def test_read_index_and_holes(self):
        index_size = 382852
        index_position_ts4 = 1255267924
        index_minor_version = 3
        entry_count = 11964
        return self.assertEqual(self.dbpf_parser.read_index_and_holes(),
                                (0, entry_count, 0, index_size, 0, 0, 0, index_minor_version, index_position_ts4))

    def test_read_index_flags(self):
        return self.assertEqual(self.dbpf_parser.read_index_flags(1255267924), (0, 0, 0, 0, 0, 0, 4))

    def test_read_index_entries(self):
        results = self.dbpf_parser.read_index_entries(1255267924 + 4, 11964, 0, 0, 0, 0, 0, 0, 4 - 4)
        print(results[0].location, results[0].compressed_size[0])
        for result in results:
            self.assertIsNot(result.location, 0)
            self.assertIsNot(result.compressed_size[0], 0)
            self.assertIsNot(result.uncompresessed_size, 0)

            self.assertLessEqual(result.compressed_size[0], result.uncompresessed_size)
        return

    def test_read_data(self):
        self.assertIsNot(self.dbpf_parser.read_data([(1239001778, 16682)]), "")


class OneFileSims3Compressed(ActualSims3FileTests):
    def setUp(self):
        # Load test data
        self.dbpf_parser = DBPFParser("Unit Test Files/sims3compressedfile", "package")
        self.dbpf_parser.setup_file_reader()

    def test_read_index_and_holes(self):
        index_size = 36
        index_position_ts4 = 2085
        index_minor_version = 3
        entry_count = 1
        return self.assertEqual(self.dbpf_parser.read_index_and_holes(),
                                (0, entry_count, 0, index_size, 0, 0, 0, index_minor_version, index_position_ts4))

    def test_read_index_flags(self):
        return self.assertEqual(self.dbpf_parser.read_index_flags(2085), (1, 1, 1, 53690476, 0, 2043403390, 16))

    def test_read_index_entries(self):
        results = self.dbpf_parser.read_index_entries(2085 + 4, 1, 1, 1, 1, 62078431, 2147483648, 148365759, 16 - 4)
        expected_position = 96
        compressed_flag = 65535
        decompressed_size = 2822
        compressed_size = 1989
        self.assertEqual(results[0].get_values(),
                         (62078431, 2147483648, 148365759, 2503320826, expected_position, [compressed_size, 1],
                          decompressed_size, [compressed_flag, 1]))
        return

    def test_decompress_data(self):
        compressed_size = 1989
        decompressed_size = 2822

        index_sizes_and_locations = [(96, compressed_size)]
        data = self.dbpf_parser.read_data(index_sizes_and_locations)
        uncompressed_data = decompress_data(data[0], True, decompressed_size)
        m = hashlib.sha256()
        m.update(uncompressed_data)
        uncompressed_data_hash = m.hexdigest()
        print(uncompressed_data)
        self.assertEqual(uncompressed_data_hash, "f00f0628f75afb001305e841f8bb4c9455db65a9ebe6ac3d7ea6874fbf2edbb3")



if __name__ == '__main__':
    unittest.main()
