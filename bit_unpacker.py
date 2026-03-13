from struct import pack, unpack
def unpack_bits_large(bits):
    bits = unpack('<Q', pack('>Q', bits))[0]
    return bits


def unpack_bits_little(bits):
    bits = unpack('<L', pack('>L', bits))[0]
    return bits


def unpack_bits_little2(bits):
    bits = unpack('<L', pack('<L', bits))[0]
    return bits

def access_bit(data, num):
    base = int(num/8)
    shift = num % 8
    return str((data[base] & (1<<shift)) >> shift)


def pack_bits_little3(bits):
    bits = pack('<L', bits)
    bits = [access_bit(bits,i) for i in range(len(bits)*8)]
    bits = "".join(bits)
    return bits

def pack_bits_little4(bits):
    bits = pack('>L', bits)
    bits = [access_bit(bits,i) for i in range(len(bits)*8)]
    bits = "".join(bits)
    return bits


def unpack_bits_even_littler(bits):
    bits = unpack('<H', pack('>H', bits))[0]
    return bits
