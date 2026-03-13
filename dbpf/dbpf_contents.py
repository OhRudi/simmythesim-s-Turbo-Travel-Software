from dbpf.helpers import decompress_data


class IndexData:
    def __init__(self, t, g, iEx, i, location, compressed_size, uncompressed_size, compressed_bitfield):
        self.t = t
        self.g = g
        self.iEx = iEx
        self.i = i
        self.location = location
        self.compressed_size = compressed_size
        self.uncompresessed_size = uncompressed_size
        self.compressed_bitfield = compressed_bitfield

    def get_values(self):
        return self.t, self.g, self.iEx, self.i, self.location, self.compressed_size, self.uncompresessed_size, self.compressed_bitfield

    def __str__(self):
        return str(self.get_values())

    def __repr__(self):
        return str(self.get_values())


def decompress_and_save(count, data, is_compressed, decompressed_size):
    data = decompress_data(data, is_compressed, decompressed_size)
    #with open("test files/{}.resource".format(count), "wb") as file:
    #    file.write(data)
    return data