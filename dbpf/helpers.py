import struct
import zlib


def decompress_old_files(compressed_data, uncompressed_data, uncompressed_size, count):
    uncompressed_memory_view = memoryview(uncompressed_data)
    compressed_memory_view = memoryview(compressed_data)

    compressed_ints = compressed_memory_view.tolist()

    def copy_plain_text(compressed_position, num_plain_text: int, position: int):
        # copy one at a time
        for i in range(0, num_plain_text):
            read_byte = compressed_memory_view[compressed_position + i]
            uncompressed_memory_view[position] = read_byte
            position += 1
        return num_plain_text

    def copy_compressed_text(num_to_copy: int, position: int, copy_offset: int):

        # copy compressed text one at a time
        currentPosition = position
        for i in range(0, num_to_copy):
            uncompressed_memory_view[position] = uncompressed_memory_view[currentPosition - copy_offset + i]
            position += 1
        return position - currentPosition

    read_bytes = 0
    compressed_read_bytes = 0
    times_looped = 0
    while read_bytes < uncompressed_size:
        times_looped += 1
        #  print(compressed_read_bytes, read_bytes)
        byte0 = compressed_ints[compressed_read_bytes]
        compressed_read_bytes += 1
        if byte0 <= 0x7F:
            byte1 = compressed_ints[compressed_read_bytes]

            compressed_read_bytes += 1

            num_plain_text = byte0 & 0x03
            numToCopy = ((byte0 & 0x1C) >> 2) + 3
            copyOffset = ((byte0 & 0x60) << 3) + byte1 + 1

            bytes_read = copy_plain_text(compressed_read_bytes, num_plain_text, read_bytes)
            read_bytes += bytes_read
            compressed_read_bytes += bytes_read

            bytes_copied = copy_compressed_text(numToCopy, read_bytes, copyOffset)
            read_bytes += bytes_copied

        elif byte0 <= 0xBF and byte0 > 0x7F:
            byte1 = compressed_ints[compressed_read_bytes]

            compressed_read_bytes += 1
            byte2 = compressed_ints[compressed_read_bytes]

            compressed_read_bytes += 1

            num_plain_text = ((byte1 & 0xC0) >> 6) & 0x03
            numToCopy = (byte0 & 0x3F) + 4
            copyOffset = ((byte1 & 0x3F) << 8) + byte2 + 1

            bytes_read = copy_plain_text(compressed_read_bytes, num_plain_text, read_bytes)

            read_bytes += bytes_read
            compressed_read_bytes += bytes_read

            bytes_copied = copy_compressed_text(numToCopy, read_bytes, copyOffset)
            read_bytes += bytes_copied
            #    print("BC", bytes_copied)


        elif byte0 <= 0xDF and byte0 > 0xBF:
            byte1 = compressed_ints[compressed_read_bytes]

            compressed_read_bytes += 1
            byte2 = compressed_ints[compressed_read_bytes]

            compressed_read_bytes += 1
            byte3 = compressed_ints[compressed_read_bytes]

            compressed_read_bytes += 1

            num_plain_text = byte0 & 0x03
            numToCopy = ((byte0 & 0x0C) << 6) + byte3 + 5
            copyOffset = ((byte0 & 0x10) << 12) + (byte1 << 8) + byte2 + 1

            bytes_read = copy_plain_text(compressed_read_bytes, num_plain_text, read_bytes)

            read_bytes += bytes_read
            compressed_read_bytes += bytes_read

            bytes_copied = copy_compressed_text(numToCopy, read_bytes, copyOffset)
            read_bytes += bytes_copied


        elif byte0 <= 0xFB and byte0 > 0xDF:
            num_plain_text = ((byte0 & 0x1F) << 2) + 4

            bytes_read = copy_plain_text(compressed_read_bytes, num_plain_text, read_bytes)

            read_bytes += bytes_read
            compressed_read_bytes += bytes_read


        elif byte0 <= 0xFF and byte0 > 0xFB:
            num_plain_text = byte0 & 0x03

            bytes_read = copy_plain_text(compressed_read_bytes, num_plain_text, read_bytes)

            read_bytes += bytes_read
            compressed_read_bytes += bytes_read
    # print("Times looped {}".format(times_looped))

    return uncompressed_data, count
def convert_to_8bytes(data):
    result = struct.pack("<Q", data)
   # print(data, "{}".format(result.hex()))
    return result


def convert_to_4bytes(data):
    result = struct.pack("<L", data)
   # print(data, "{}".format(result.hex()))
    return result


def convert_to_2bytes(data):
    return struct.pack("<H", data)


def decompress_data(data, is_compressed, decompressed_size):
    if is_compressed and decompressed_size != 4294967295:
        try:
            return zlib.decompress(data)
        except:
            compressionType = int.from_bytes(data[0:1], "little", signed=False)

            if compressionType == 0x80:
                index_size = 4
            else:
                index_size = 3
            old_decompressed_size = int.from_bytes(data[2:2+index_size], "big", signed=False)
            #print(decompressed_size, old_decompressed_size, hex(compressionType))

            uncompressed_data = bytearray(old_decompressed_size)
            compressed_data = bytearray(data[2+index_size:])
            #Start at index 3 because the first few bytes designate what type the file is
            decompress_old_files(compressed_data, uncompressed_data, old_decompressed_size, 0)
            return uncompressed_data
    return data