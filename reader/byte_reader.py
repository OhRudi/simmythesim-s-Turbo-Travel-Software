
class ByteReader:
    def __init__(self, filepath):
        self.filepath = filepath
        self.opened_file = None


    def open_file(self):
        self.opened_file = open(self.filepath, "rb")
        return True

    def read_bytes_at_position(self, position, bytes_to_read):
        self.opened_file.seek(position, 0) # Seek to this offset from the beginning
        read_bytes = self.opened_file.read(bytes_to_read)
        return read_bytes

    def close_file(self):
        self.opened_file.close()
        self.opened_file = None
        return True


class ByteWriter:
    def __init__(self, filepath):
        self.filepath = filepath
        self.opened_file = None


    def open_file(self):
        self.opened_file = open(self.filepath, "wb")
        self.opened_file.write(b"")
        self.opened_file.close()
        self.opened_file = open(self.filepath, "ab")
        return True

    def write_bytes(self, write_bytes):
        self.opened_file.write(write_bytes)

    def close_file(self):
        self.opened_file.close()
        self.opened_file = None
        return True
