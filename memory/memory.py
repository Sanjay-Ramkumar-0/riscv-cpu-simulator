from utils.constants import MEMORY_SIZE

# we choose memory size to be 64MB (64*1024*1024 bytes) so the address space is from 0x00000000 to 0x03FFFFFF. 

class Memory:

    def __init__(self):

        self.mem = bytearray(MEMORY_SIZE)

    # -----------------------------------------
    # Read Operations
    # -----------------------------------------

    def read8(self, addr: int) -> int:

        return self.mem[addr]

    def read16(self, addr: int) -> int:

        return int.from_bytes(
            self.mem[addr:addr + 2],
            byteorder="little"
        )

    def read32(self, addr: int) -> int:

        return int.from_bytes(
            self.mem[addr:addr + 4],
            byteorder="little"
        )

    def read64(self, addr: int) -> int:

        return int.from_bytes(
            self.mem[addr:addr + 8],
            byteorder="little"
        )

    # -----------------------------------------
    # Write Operations
    # -----------------------------------------

    def write8(self, addr: int, value: int) -> None:

        self.mem[addr] = value & 0xFF

    def write16(self, addr: int, value: int) -> None:

        self.mem[addr:addr + 2] = (
            value & 0xFFFF
        ).to_bytes(2, byteorder="little")

    def write32(self, addr: int, value: int) -> None:

        self.mem[addr:addr + 4] = (
            value & 0xFFFFFFFF
        ).to_bytes(4, byteorder="little")

    def write64(self, addr: int, value: int) -> None:

        self.mem[addr:addr + 8] = (
            value & 0xFFFFFFFFFFFFFFFF
        ).to_bytes(8, byteorder="little")

