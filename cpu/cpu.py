"""
CPU

Top-level CPU model.

Responsibilities:
    - Manage hardware threads
    - Fetch instructions
    - Decode instructions
    - Dispatch to RV64I / RV64M
    - Run programs
"""

from cpu.thread_context import ThreadContext
from memory.memory import Memory
from isa.decoder import Decoder
from isa.rv64i import RV64I
from isa.rv64m import RV64M
from frontend.predictor import BranchPredictor
from frontend.btb import BranchTargetBuffer
from memory.cache import Cache

class CPU:

    def __init__(self):

        # =====================================
        # Hardware Threads (SMT2)
        # =====================================

        self.threads = [
            ThreadContext(0),
            ThreadContext(1)
        ]

        # Frontend

        self.predictor = BranchPredictor()

        self.btb = BranchTargetBuffer()
        # =====================================
        # Main Memory
        # =====================================

        self.memory = Memory()

        # =====================================
        # Caches
        # =====================================

        self.icache = Cache(
            self.memory,
            name="I-Cache"
        )

        self.dcache = Cache(
            self.memory,
            name="D-Cache"
        )

    # =====================================
    # Fetch
    # =====================================

    def fetch(self, thread_id: int) -> int:
        """
        Fetch one 32-bit instruction.
        """

        thread = self.threads[thread_id]

        pc = thread.get_pc()

        return self.memory.read32(pc)

    # =====================================
    # Decode
    # =====================================

    def decode(self, inst: int) -> dict:
        """
        Decode instruction.
        """

        return Decoder.decode(inst)

    # =====================================
    # Execute One Instruction
    # =====================================

    def step(self, thread_id: int) -> None:

        thread = self.threads[thread_id]

        # -------------------------
        # Fetch
        # -------------------------

        inst = self.fetch(thread_id)

        # -------------------------
        # Decode
        # -------------------------

        decoded = self.decode(inst)

        op = decoded["op"]

        # -------------------------
        # Dispatch
        # -------------------------

        if op in {

            # RV64I ALU
            "ADD",
            "SUB",
            "AND",
            "OR",
            "XOR",
            "SLL",
            "SRL",
            "SRA",
            "SLT",
            "SLTU",

            # Immediate
            "ADDI",

            # Memory
            "LD",
            "SD",

            # Branches
            "BEQ",
            "BNE",
            "BLT",
            "BGE",
            "BLTU",
            "BGEU",

            # Jump
            "JAL",

            # Upper Immediate
            "LUI",
            "AUIPC"
        }:

            RV64I.execute(
                thread,
                self.memory,
                decoded
            )

        elif op in {

            "MUL",
            "DIV",
            "REM"

        }:

            RV64M.execute(
                thread,
                self.memory,
                decoded
            )

        else:

            raise ValueError(
                f"Unsupported instruction: {op}"
            )

    # =====================================
    # Run
    # =====================================

    def run(
        self,
        thread_id: int,
        cycles: int
    ) -> None:
        """
        Execute N instructions.
        """

        for _ in range(cycles):
            self.step(thread_id)

    # =====================================
    # Program Loading
    # =====================================

    def load_program(
        self,
        filename: str,
        start_address: int = 0
    ) -> None:
        """
        Load binary into memory.
        """

        with open(filename, "rb") as f:
            program = f.read()

        for i, byte in enumerate(program):

            self.memory.write8(
                start_address + i,
                byte
            )

    # =====================================
    # Thread Selection
    # =====================================

    def get_thread(
        self,
        thread_id: int
    ) -> ThreadContext:

        return self.threads[thread_id]

    # =====================================
    # Reset CPU
    # =====================================

    def reset(self):

        self.memory = Memory()

        self.icache = Cache(
            self.memory
        )

        self.dcache = Cache(
            self.memory
        )

        self.threads = [
            ThreadContext(0),
            ThreadContext(1)
        ]

    # =====================================
    # Debug
    # =====================================

    def dump_state(
        self,
        thread_id: int
    ) -> None:

        thread = self.threads[thread_id]

        thread.dump_state()

        thread.dump_registers()


