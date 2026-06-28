"""
Our architecture is:
    - 1 Core
    - 2 Hardware Threads (SMT2)

Each thread has:
    - Program Counter (PC)
    - Register File (x0-x31)
    - CSR State (future)
    - Thread Status

thread_context.py represents the architectural state
of a single hardware thread.
"""

from utils.constants import XLEN, NUM_REGS
from utils.helpers import mask64


class ThreadContext:

    def __init__(self, thread_id: int):

        self.thread_id: int = thread_id

        self.pc: int = 0

        self.regs: list[int] = [0] * NUM_REGS

        self.csrs: dict[int, int] = {}

        self.active: bool = True

    # =====================================
    # Register Operations
    # =====================================

    def read_reg(self, reg_num: int) -> int:

        if reg_num == 0:
            return 0

        return self.regs[reg_num]

    def write_reg(
        self,
        reg_num: int,
        value: int
    ) -> None:

        if reg_num == 0:
            return

        self.regs[reg_num] = mask64(value)

    # =====================================
    # Program Counter Operations
    # =====================================

    def get_pc(self) -> int:

        return self.pc

    def set_pc(
        self,
        value: int
    ) -> None:

        self.pc = mask64(value)

    def advance_pc(self) -> None:

        self.pc = mask64(self.pc + 4)

    # =====================================
    # Reset
    # =====================================

    def reset(self) -> None:

        self.pc = 0

        self.regs = [0] * NUM_REGS

        self.csrs.clear()

        self.active = True

    # =====================================
    # Debug Functions
    # =====================================

    def dump_state(self) -> None:

        print(f"Thread ID : {self.thread_id}")
        print(f"PC        : 0x{self.pc:016X}")
        print(f"Active    : {self.active}")

    def dump_registers(self) -> None:

        print(
            f"\n========== Thread {self.thread_id} =========="
        )

        for i in range(NUM_REGS):

            print(
                f"x{i:02d} = 0x{self.read_reg(i):016X}"
            )

        print(
            "======================================"
        )