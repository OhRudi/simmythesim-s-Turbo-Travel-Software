from bit_unpacker import pack_bits_little3
from bitarray import bitarray

class Bitfield:
    def __init__(self, bits, bitslices):

        self.bitfield = str(bin(bits)).replace("0b", "").replace("'", "").replace(" ", "").zfill(32)
       # print("Bit field ", self.bitfield)

       # print("BF, ", self.bitfield, " ", type(self.bitfield))

        #print(self.bitfield)
        self.bitslices = bitslices[::-1]
        #print(self.bitslices)

    def get_bit_values(self):
        self.datas = []
        element_count = 0
        byte_list = []
        #print(datas)
        currentBytesRead = 0
       # print(self.bitfield)
        for bits in  self.bitslices:
            element = self.bitfield[currentBytesRead:currentBytesRead+bits]
            currentBytesRead += bits
            #print(element)
            self.datas.append(element)

            element_count += 1

        binary_data = "".join(self.datas)
       # print(binary_data)
        new_data = []
        bitsRead = 0
        for bitslice in self.bitslices:
            new_data.append(int(binary_data[bitsRead:bitsRead+bitslice], base=2))
            bitsRead += bitslice
        new_data.reverse()
       # print(new_data)

        return new_data


def sum(numbers):
    total = 0
    for x in numbers:
        total += x
    return total

class BitfieldWriter:
    def __init__(self, datas, bitslices):
        #datas.reverse()
        #bitslices.reverse()
        self.datas = []
        self.bitslices = bitslices
        element_count = 0
        byte_list = []
        #print(datas)
        for element in datas:
           # print(element)
            aob = bitarray()

            count = 0
            total_count = 0
        #    print(pack_bits_little3(element))
            for character in pack_bits_little3(element)[:int(bitslices[element_count])]:
                aob.append(character == "1")
                count += 1
                total_count += 1
               # print(total_count)
                if count == 4 or total_count == int(bitslices[element_count]):
                   # print(aob)
                    aob.reverse()
                    byte_list.append(aob.to01())
                    aob = bitarray()
                    count = 0

            element_count += 1

        self.datas = byte_list[::-1]
        #print("".join(self.datas))
        #print(self.bitfield)
        #print(self.datas)



    def set_bit_values(self):
        self.datas = "".join(self.datas)
     #   print(self.datas)
#        print("Bitfield2", unpack_bits_little(int(self.datas, base=2)))
        return self.datas
