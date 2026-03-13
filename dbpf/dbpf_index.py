from dbpf.helpers import convert_to_4bytes


class DBPFIndex:
    def __init__(self, magic_number, version_number, unused_flags_and_date, index_and_holes, flags, tgi_index):
        self._magic_number = magic_number
        self._version_number = version_number
        self._unused_flags_and_date = unused_flags_and_date
        self._index_and_holes = index_and_holes
        self._flags = flags
        self._flag_header = None
        self._tgi_index = tgi_index

    def convert_data(self, data):
        return b"".join(map(convert_to_4bytes, data))

    @property
    def magic_number(self):
        return self._magic_number

    @property
    def version_number(self):
        return convert_to_4bytes(self._version_number[0]) + convert_to_4bytes(self._version_number[1]) + convert_to_4bytes(self._version_number[2]) + convert_to_4bytes(self._version_number[3])

    @property
    def zero(self):
        return convert_to_4bytes(0)

    @property
    def unused_flags_and_date(self):
        return convert_to_4bytes(self._unused_flags_and_date[0]) + convert_to_4bytes(self._unused_flags_and_date[1]) + convert_to_4bytes(self._unused_flags_and_date[2])

    @property
    def index_and_holes(self):
       # print(self._index_and_holes)
        return self.convert_data(self._index_and_holes[4:-1])

    @property
    #Doesn't support constant ids right now
    def flags(self):
        data_list = []
        data_list.append(convert_to_4bytes(self._flags[0]))
        return b"".join(data_list)
    @property
    def reserved(self):
        data = b""
        data_list = []
        for i in range(6):
            data_list.append(convert_to_4bytes(0))

        data = b"".join(data_list)
        return data


    @property
    def tgi_index(self):
        return self._tgi_index


    def __repr__(self):
        return "{} {} {} {} {}".format(self._magic_number, self._version_number, self._unused_flags_and_date, self._index_and_holes, self._flags)