"""
Branch Target Buffer (BTB)

Stores the destination (target address)
of previously executed branch instructions.

Key   : Branch PC
Value : Target PC

The Branch Predictor decides WHETHER
a branch is taken.

The BTB decides WHERE it goes.
"""


class BranchTargetBuffer:

    # =====================================
    # Constructor
    # =====================================

    def __init__(self):

        # Branch Target Buffer
        #
        # Key   : Branch PC
        # Value : Target Address

        self.table = {}

    # =====================================
    # Lookup
    # =====================================

    def lookup(
        self,
        pc: int
    ):

        return self.table.get(
            pc,
            None
        )

    # =====================================
    # Update
    # =====================================

    def update(
        self,
        pc: int,
        target: int
    ) -> None:

        self.table[pc] = target

    # =====================================
    # Check Entry
    # =====================================

    def contains(
        self,
        pc: int
    ) -> bool:

        return pc in self.table

    # =====================================
    # Remove Entry
    # =====================================

    def remove(
        self,
        pc: int
    ) -> None:

        if pc in self.table:

            del self.table[pc]

    # =====================================
    # Clear BTB
    # =====================================

    def reset(self) -> None:

        self.table.clear()

    # =====================================
    # Dump Contents
    # =====================================

    def dump(self) -> None:

        print("\n========== Branch Target Buffer ==========")

        if not self.table:

            print("Empty")

        else:

            for pc in sorted(self.table):

                print(
                    f"PC     : 0x{pc:08X}"
                )

                print(
                    f"Target : 0x{self.table[pc]:08X}"
                )

                print()

        print("==========================================")

if __name__ == "__main__":

    btb = BranchTargetBuffer()

    pc = 0x100

    print(
        "Lookup before insert:",
        btb.lookup(pc)
    )

    btb.update(
        pc,
        0x200
    )

    print(
        "Lookup after insert:",
        hex(
            btb.lookup(pc)
        )
    )

    print(
        "Contains:",
        btb.contains(pc)
    )

    btb.dump()

    btb.remove(pc)

    print(
        "\nAfter removal:"
    )

    btb.dump()