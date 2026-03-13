import unittest
from unittest import TestCase
from dbpf.dbpf_converter import DBPFConverter


class SimpleWriterTest(TestCase):
    def test(self):
        # Load test data
        self.dbpf_converter = DBPFConverter("Unit Test Files/sims4actual", "package")
        self.fail()


if __name__ == '__main__':
    unittest.main()
