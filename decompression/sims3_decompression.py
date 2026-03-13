def copy_plain_text(compressed, compressed_position, data: bytearray, num_plain_text: int, position: int):
    # copy one at a time
    for i in range(0, num_plain_text):
        read_byte = compressed[compressed_position+i]
        data[position] = read_byte
        position += 1
    return num_plain_text


def copy_compressed_text(data: bytearray, num_to_copy: int, position: int, copy_offset: int):

    # copy compressed text one at a time
    currentPosition = position
    for i in range(0, num_to_copy):
        data[position] = data[currentPosition - copy_offset + i]
        position += 1
    return position - currentPosition