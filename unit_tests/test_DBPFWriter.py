import hashlib
import unittest
from unittest import TestCase
from dbpf.dbpf_index import DBPFIndex
from dbpf.dbpf_writer import DBPFWriter


class SimpleWriterTest(TestCase):
    def setUp(self):
        # Load test data
        self.dbpf_writer = DBPFWriter("Unit Test Files/testoutput", "package", DBPFIndex(b"DBPF", (2, 1, 0, 0), (0, 0, 0), (0, 1, 0, 16, 0, 0, 0, 3, 96), (0, 0, 0, 0, 0, 0)))
        self.dbpf_writer.setup_file_writer()

    def write_something(self, to_write):
        self.dbpf_writer.write_resource_data(to_write)
        self.dbpf_writer.byteWriter.close_file()

        m2 = hashlib.sha256()
        self.assertIsNotNone(self.dbpf_writer.byteWriter.filepath)

        with open(self.dbpf_writer.byteWriter.filepath, "rb") as file:
            compressed = file.read()
            # print(compressed)
            self.assertNotEqual(compressed, b"")

            m2.update(compressed)
        written_data_hash = m2.hexdigest()
        return written_data_hash, compressed


    def test_write_magic_number(self):
        data_hash = "b2df5d4febb1c193a8ae49c799ce4f07f5ca1068c2521ca920c67f23e82b3fcf"
        written_hash, written_data = self.write_something(self.dbpf_writer.dbpf_header.magic_number)
        self.assertEqual(written_hash, data_hash)

    def test_write_version_number(self):
        data_hash = "22b69f7a90adc41bde5758f5664f4cad8a2d03761d826ab511044b4e82c2586f"
        written_hash, written_data = self.write_something(self.dbpf_writer.dbpf_header.version_number)
        self.assertEqual(written_hash, data_hash)

    def test_zero(self):
        data_hash = "df3f619804a92fdb4057192dc43dd748ea778adc52bc498ce80524c014b81119"
        written_hash, written_data = self.write_something(self.dbpf_writer.dbpf_header.zero)
        self.assertEqual(written_hash, data_hash)

    def test_write_unused_flags_and_date(self):
        data_hash = "15ec7bf0b50732b49f8228e07d24365338f9e3ab994b00af08e5a3bffe55fd8b"
        written_hash, written_data = self.write_something(self.dbpf_writer.dbpf_header.unused_flags_and_date)
        self.assertEqual(written_hash, data_hash)

    def test_write_index_and_holes(self):
        data_hash = "2738d0bd89b1b25a7c2caea73636c7c7551342f1824efc2095e27976454e20e0"
        written_hash, written_data = self.write_something(self.dbpf_writer.dbpf_header.index_and_holes)

        self.assertEqual(written_hash, data_hash)

    def test_write_flags(self):
        data_hash = "d92cde06dd991ae5c5f75ca67c82b53a30b0b0425a0fb161a47e6187e343ea12"
        written_hash, written_data = self.write_something(self.dbpf_writer.dbpf_header.flags)

        self.assertEqual(written_hash, data_hash)

    def test_prepare_one_resource(self):
        test_resource = "On the outside, always looking in\
                        Will I ever be more than I've always been?\
                        'Cause I'm tap, tap, tapping on the glass\
                        Waving through a window\
                        I try to speak, but nobody can hear\
                        So I wait around for an answer to appear\
                        While I'm watch, watch, watching people pass\
                        Waving through a window, oh\
                        Can anybody see, is anybody waving?"
        index_header = self.dbpf_writer.prepare_resource(62078431, 2147483648, 148365759, 622275963, len(test_resource))
        self.assertEqual(index_header, [(62078431, 2147483648, 148365759, 622275963, 96, 2147484160, 512, 0, 1)])
        self.dbpf_writer.write_index()

if __name__ == '__main__':
    unittest.main()
