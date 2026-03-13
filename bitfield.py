def bitfield(n):
    return [int(digit) for digit in bin(n).zfill(32)] # [2:] to chop off the "0b" part