
def to_32_bit(value:int):
    return value & 0xffffffff

def to_32_bit_unsigned(value:int):
    return (value & 0xffffffff) + (1<<32)
