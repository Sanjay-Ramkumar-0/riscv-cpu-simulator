""" note: all the inputs and outputs are int """

def mask64(value):
    # to keep only lower 64 bits
    return value & 0xFFFFFFFFFFFFFFFF

def sign_extend(value,bits):
    # for sign extension, converting width binary number (like a 4-bit or 16-bit integer) into a wider format preserving the sign   
    sign_bits = 1 << (bits - 1) 
    #ex: when the bits is 4, then it's sign bit is 1000
    return ((value & (sign_bits-1)) - (value & sign_bits))

def zero_extend(value,bits):
    return value&((1 << bits)-1)

def get_bits(value,high,low):
    # slicing the required bits
    mask = (1 << (high-low+1)) - 1
    return (value >> low) & mask

def bit(value,position):
    # returns single bit
    return (value>>position) & 1

def is_aligned(address,alignment):
    """
    Check address alignment.

    Example:
        is_aligned(0x1000, 8) -> True
        is_aligned(0x1003, 8) -> False
    """
    
    return (address % alignment) == 0


def to_signed(value,bits):
    #to convert the unsigned integer to signed integer
    sign_bit = 1 <<(bits - 1)
    if value & sign_bit:
        return value - (1<<bits)
    return value

def to_unsigned(value, bits):   
    # Convert signed integer to unsigned integer.
    
    return value & ((1 << bits) - 1)