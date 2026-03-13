from dbpf.helpers import convert_to_8bytes, convert_to_4bytes, convert_to_2bytes
from dbpf.dbpf_format import BitfieldWriter
from reader.byte_reader import ByteWriter


class DBPFWriter:

    def __init__(self, package_name, extension, dbpf_header, starting_idx, stop):
        self.byteWriter = None
        self.package_name = package_name
        self.extension = extension
        self.dbpf_header = dbpf_header
        self.index_header = []
        self.current_data_position = 96 #96 for dbpf header
        self.starting_idx = starting_idx
        self.stop = stop

    def setup_file_writer(self):
        print("Opening {}".format(self.package_name))
        self.byteWriter = ByteWriter("{}-converted.{}".format(self.package_name, self.extension))
        self.byteWriter.open_file()

    def write_resource_data(self, data):
        if self.byteWriter is None:
            self.setup_file_writer()
        self.byteWriter.write_bytes(data)

    #Rix bug where stuff
    def prepare_resource(self, t, g, iEx, i, data_len, compressed_len, compression_type):
        memory_size = data_len
        if data_len == 4294967295:
            data_len = 1
        bitfield_writer = BitfieldWriter([data_len, 1], [31, 1])
        compressed_size = int(bitfield_writer.set_bit_values(), base=2)
        #print("Adding to index header", (t, g, iEx, i, self.current_data_position, compressed_size, data_len, 0, 1))
        resource_data_position = self.current_data_position
        new_compression_type = 0
        if data_len == 0 and compressed_len == 0 and compression_type == 65504:
            resource_data_position = 0
            new_compression_type = compression_type
        self.index_header.append((t, g, iEx, i, resource_data_position, compressed_size, memory_size, new_compression_type, 1))
        if data_len == 4294967295:
            self.current_data_position += 1
        else:
            self.current_data_position += data_len
        return self.index_header

    def write_index(self):
        #print("FLAGS: {}".format(self.dbpf_header.flags))
        self.write_resource_data(self.dbpf_header.flags)

        total_bytes = []

        for entry in self.index_header:
            current_bytes = list()
           # print(entry)

            current_bytes.append(convert_to_4bytes(entry[0]))
            current_bytes.append(convert_to_4bytes(entry[1]))
            current_bytes.append(convert_to_4bytes(entry[2]))
            current_bytes.append(convert_to_4bytes(entry[3]))
            current_bytes.append(convert_to_4bytes(entry[4]))

            current_bytes.append(convert_to_4bytes(entry[5]))
            current_bytes.append(convert_to_4bytes(entry[6]))
            current_bytes.append(convert_to_2bytes(entry[7]))
            current_bytes.append(convert_to_2bytes(entry[8]))
           # print(current_bytes)

            total_bytes.extend(current_bytes)
        written_bytes = b"".join(total_bytes)
       # print(written_bytes)
        self.write_resource_data(written_bytes)

    def write_header(self, new_idx_entry_len, new_idx_size):
        #TODO new index entry len not correct
       # print(self.dbpf_header)
        self.write_resource_data(self.dbpf_header.magic_number)
        self.write_resource_data(self.dbpf_header.version_number)
        self.write_resource_data(self.dbpf_header.unused_flags_and_date)
        index_offset = convert_to_8bytes(self.current_data_position)
       # print("New data entry len {}".format(new_idx_entry_len))

        new_idx_entry_len = convert_to_4bytes(new_idx_entry_len)
        #Record entry, entry length, record size
        self.write_resource_data(convert_to_4bytes(0) + new_idx_entry_len + convert_to_4bytes(0) + convert_to_4bytes(new_idx_size) + self.dbpf_header.index_and_holes + index_offset)
        self.write_resource_data(self.dbpf_header.reserved)

    def prepare_resources(self):

        deleted_files = []
        for idx in range(self.starting_idx, self.stop):
            tgi_data = self.dbpf_header.tgi_index[idx]
           # print(tgi_data.uncompresessed_size)
            if tgi_data.uncompresessed_size == 4294967295:
                tgi_data.compressed_size[0] = 1

                #deleted_files.append(idx)
               # idx += 1
               # continue
            self.prepare_resource(tgi_data.t, tgi_data.g, tgi_data.iEx, tgi_data.i,
                                                             tgi_data.uncompresessed_size, tgi_data.compressed_size[0], tgi_data.compressed_bitfield[0])