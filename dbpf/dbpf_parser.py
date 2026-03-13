from dbpf.dbpf_index import DBPFIndex
from dbpf.dbpf_contents import decompress_and_save, IndexData
from dbpf.dbpf_format import Bitfield
from reader.byte_reader import ByteReader


class DBPFParser:

    def __init__(self, package_name, extension, cpu_cores):
        self.package_name = package_name
        self.extension = extension
        self.byteReader = None
        self.cpu_cores = cpu_cores
        self.setup_file_reader()

    def read_at_position(self, position=0, bytesToRead=0):
        return self.byteReader.read_bytes_at_position(position, bytesToRead)

    def read_package(self):
        return self.read_header_and_datas()

    def setup_file_reader(self):
        assert self.byteReader is None
        print("Opening {}".format(self.package_name))
        self.byteReader = ByteReader("{}.{}".format(self.package_name, self.extension))
        self.byteReader.open_file()

    def read_header_and_datas(self):
        from multiprocessing import Pool

        dbpf_identifier = self.read_dbpf_magic_number()

        major, minor, majorUser, minorUser = self.read_version_number()
        flags, created, modified = self.read_flags_and_date_stamp()
        major_version, entry_count, ts2_location, size, hole_count, hole_location, hole_size, minor_version, ts3_location = self.read_index_and_holes()
        print("Index location is {}".format(ts3_location))
        print("Read entry count is {}".format(entry_count))
        constantType, constantGroup, constantInstanceEx, constant_type_id, constant_group_id, constant_ex_id, flags_bytes = self.read_index_flags(ts3_location)
        results = self.read_index_entries(ts3_location + 4, entry_count, constantType, constantGroup, constantInstanceEx, constant_type_id, constant_group_id, constant_ex_id, flags_bytes - 4)
       # print(results)
        resources = []
        for resource in results:
            resources.append((resource.location, resource.compressed_size[0]))

       # print(resources)
        resources_data = self.read_data(resources)

        pool = Pool(self.cpu_cores)

        datas_compressed = []
        uncompressed_sizes = []
        splits = [0]
        current_chunk_total_size = 0
        #1200 megabytes
        MAX_BYTES_PER_CHUNK = 1200000000
        for idx in range(len(resources_data)):
            datas_compressed.append(results[idx].compressed_bitfield[0] != 0)
            uncompressed_sizes.append(results[idx].uncompresessed_size)
            if results[idx].uncompresessed_size < 4294967295:
                current_chunk_total_size += results[idx].uncompresessed_size
            else:
                current_chunk_total_size += 1
            if current_chunk_total_size > MAX_BYTES_PER_CHUNK:
                splits.append(idx)
                current_chunk_total_size = 0
        splits.append(len(resources_data))

        datas = pool.starmap(decompress_and_save, zip(range(0, len(resources_data)), resources_data, datas_compressed, uncompressed_sizes))
       # datas = []
       # for idx in range(len(resources_data)):
       #     datas.append(decompress_and_save(idx, resources_data[idx], datas_compressed[idx], uncompressed_sizes[idx]))
        #pool.close()

        version = (major, minor, majorUser, minorUser)
        index_and_holes = (major_version, entry_count, ts2_location, size, hole_count, hole_location, hole_size, minor_version, ts3_location)
        unused_flags = (flags, created, modified)
        #flags = (constantType, constantGroup, constantInstanceEx, constant_type_id, constant_group_id, constant_ex_id)
        flags = (0, 0, 0, 0)
        return DBPFIndex(dbpf_identifier, version, unused_flags, index_and_holes, flags, results), splits, datas

    def read_dbpf_magic_number(self):
        return self.read_at_position(position=0, bytesToRead=4)

    def read_version_number(self):
        major, minor, majorUser, minorUser = map(self.read_and_cast, [4, 8, 12, 16])
        return major, minor, majorUser, minorUser

    def read_flags_and_date_stamp(self):
        flags, created, modified = map(self.read_and_cast, [20, 24, 28])
        return flags, created, modified

    def read_index_and_holes(self):
        major_version, entry_count, ts2_location, size, hole_count, hole_location, hole_size, minor_version = map(self.read_and_cast, [32, 36, 40,44, 48, 52, 56, 60])
        ts3_location = self.read_and_cast_uint64(64)
        return major_version, entry_count, ts2_location, size, hole_count, hole_location, hole_size, minor_version, ts3_location

    def read_index_flags(self, index_position):
        flags = self.read_and_cast(index_position)
        constantType, constantGroup, constantInstanceEx, reserved = Bitfield(flags,
                                                                             [1, 1, 1, 29]).get_bit_values()
        current_count = 4
        constant_type_id, constant_group_id, constant_ex_id = 0, 0, 0
        if constantType:
            constant_type_id = self.read_and_cast(index_position + current_count)
            current_count += 4
        if constantGroup:
            constant_group_id = self.read_and_cast(index_position + current_count)
            current_count += 4

        if constantInstanceEx:
            constant_ex_id = self.read_and_cast(index_position + current_count)
            current_count += 4

        return constantType, constantGroup, constantInstanceEx, constant_type_id, constant_group_id, constant_ex_id, current_count

    def read_if_flag_is_set(self, flag, constant_value, position, current_count):
        if flag != 0:
            return constant_value, current_count
        else:
            return self.read_and_cast(position), current_count + 4

    def get_size_of_each_index(self, constant_type, constant_group, constant_ex):
        actual_size = 32
        if constant_type != 0:
            actual_size -= 4
        if constant_group != 0:
            actual_size -= 4
        if constant_ex != 0:
            actual_size -= 4
        return actual_size

    def read_index_entries(self, index_entries_position, index_entry_count, constantType, constantGroup, constantIndexEx, constantTypeId, constantGroupId, constantIndexIdEx, header_extra_bytes):
        index_datas = []
        individual_index_size = self.get_size_of_each_index(constantType, constantGroup, constantIndexEx)
        for current_entry_count in range(index_entry_count):
            current_index_entry_position = index_entries_position + header_extra_bytes + (current_entry_count * individual_index_size)
            current_count = 0
            type, current_count = self.read_if_flag_is_set(constantType, constantTypeId, current_index_entry_position + current_count, current_count)
            group, current_count = self.read_if_flag_is_set(constantGroup, constantGroupId, current_index_entry_position + current_count, current_count)
            instance_ex, current_count = self.read_if_flag_is_set(constantIndexEx, constantIndexIdEx, current_index_entry_position + current_count, current_count)

            instance, location, size_bitfield, size_decompressed = map(self.read_and_cast, range(current_index_entry_position + current_count, current_index_entry_position + current_count + 16, 4))
            compressed_size, extended_compression = Bitfield(size_bitfield, [31, 1]).get_bit_values()
            compression_type, committed = map(self.read_and_cast_uint16, range(current_index_entry_position + current_count + 16, current_index_entry_position + current_count + 20, 2))
            index_datas.append(
                IndexData(type, group, instance_ex, instance, location, [compressed_size, extended_compression], size_decompressed, [compression_type, committed]))
      #  print(index_datas)
        return index_datas

    def read_and_cast(self, position):
        raw_bytes = self.read_at_position(position=position, bytesToRead=4)
        return self.cast_to_uint32(raw_bytes)

    def read_and_cast_uint16(self, position):
        raw_bytes = self.read_at_position(position=position, bytesToRead=2)
        return self.cast_to_uint32(raw_bytes)


    def read_and_cast_uint64(self, position):
        raw_bytes = self.read_at_position(position=position, bytesToRead=8)
        return self.cast_to_uint32(raw_bytes)

    def cast_to_uint32(self, raw_bytes):
        return int.from_bytes(memoryview(raw_bytes), "little", signed=False)

    def read_index(self):
        raise NotImplementedError

    def read_data(self, index_sizes_and_locations):
        data = []
        for pos, size in index_sizes_and_locations:
            if pos == 0 and size == 0:
                data.append(b"")
            else:
                entry_data = self.read_at_position(pos, size)
                data.append(entry_data)
        return data
