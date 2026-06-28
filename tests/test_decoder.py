from isa.decoder import Decoder

inst = 0x002081B3

print(
    Decoder.decode(inst)
)