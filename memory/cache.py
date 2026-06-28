"""
Generic Direct-Mapped Cache
"""

from memory.cache_line import CacheLine
from memory.cache_stats import CacheStats


class Cache:

    def __init__(
        self,
        memory,
        name="Cache",
        size=32 * 1024,
        line_size=64
    ):
        self.memory = memory
        self.size = size
        self.name = name

        self.line_size = line_size

        self.num_lines = (
            size // line_size
        )

        self.lines = [

            CacheLine(line_size)

            for _ in range(self.num_lines)

        ]

        self.stats = CacheStats()

    # -----------------------------------
    # Address Decode
    # -----------------------------------

    def decode_address(
        self,
        address
    ):

        line_addr = (
            address //
            self.line_size
        )

        index = (
            line_addr %
            self.num_lines
        )

        tag = (
            line_addr //
            self.num_lines
        )

        offset = (
            address %
            self.line_size
        )

        return (

            tag,

            index,

            offset

        )
    # -----------------------------------
    # Cache Lookup
    # -----------------------------------

    def lookup(
        self,
        address
    ):

        tag, index, offset = self.decode_address(
            address
        )

        line = self.lines[index]

        # Cache Hit

        if (

            line.valid

            and

            line.tag == tag

        ):

            return (

                True,

                line,

                offset

            )

        # Cache Miss

        return (

            False,

            line,

            offset

        )
    
    # -----------------------------------
    # Fill Cache Line
    # -----------------------------------

    def fill_line(
        self,
        address
    ):

        tag, index, offset = self.decode_address(
            address
        )

        line = self.lines[index]

        line_start = (

            address

            // self.line_size

        ) * self.line_size

        # Read one cache line from memory

        for i in range(self.line_size):

            line.data[i] = self.memory.read8(
                line_start + i
            )

        line.valid = True

        line.tag = tag

        return line

    # -----------------------------------
    # Read
    # -----------------------------------

    def read(
        self,
        address
    ):

        hit, line, offset = self.lookup(address)

        if hit:

            print(
                f"{self.name} HIT  : 0x{address:08X}"
            )

            self.stats.read_hits += 1

            return line.data[offset]

        print(
            f"{self.name} MISS : 0x{address:08X}"
        )

        self.stats.read_misses += 1

        line = self.fill_line(address)

        return line.data[offset]
    # -----------------------------------
    # Read 32-bit Word
    # -----------------------------------

    def read32(
        self,
        address
    ):

        value = 0

        for i in range(4):

            value |= (

                self.read(address + i)

                << (8 * i)

            )

        return value
    
    # -----------------------------------
    # Read 64-bit Value
    # -----------------------------------

    def read64(
        self,
        address
    ):

        value = 0

        for i in range(8):

            value |= (

                self.read(address + i)

                << (8 * i)

            )

        return value

    # -----------------------------------
    # Write
    # -----------------------------------

    def write(
        self,
        address,
        value
    ):

        hit, line, offset = self.lookup(address)

        if hit:

            print(
                f"{self.name} WRITE HIT  : 0x{address:08X}"
            )

            self.stats.write_hits += 1

        else:

            print(
                f"{self.name} WRITE MISS : 0x{address:08X}"
            )

            self.stats.write_misses += 1

            line = self.fill_line(address)

        # Update Cache

        line.data[offset] = value & 0xFF

        # Write Through

        self.memory.write8(
            address,
            value & 0xFF
        )
    
    # -----------------------------------
    # Write 64-bit Value
    # -----------------------------------

    def write64(
        self,
        address,
        value
    ):

        for i in range(8):

            byte = (

                value >>

                (8 * i)

            ) & 0xFF

            self.write(
                address + i,
                byte
            )

if __name__ == "__main__":

    from memory.memory import Memory

    memory = Memory()

    cache = Cache(memory)

    print("Testing write64...")

    cache.write64(
        100,
        0x1122334455667788
    )

    value = cache.read64(100)

    print(
        hex(value)
    )

    print()

    cache.stats.print()