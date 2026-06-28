"""
RV64M Instruction Execution Layer

Supports:
    MUL
    DIV
    REM
"""

from execution.muldiv import MulDiv


class RV64M:

    MULDIV_OPS = {
        "MUL",
        "DIV",
        "REM"
    }

    @staticmethod
    def execute(
        thread,
        memory,
        decoded
    ) -> None:

        op = decoded["op"]

        # ----------------------------------------
        # Validate Instruction
        # ----------------------------------------

        if op not in RV64M.MULDIV_OPS:

            raise ValueError(
                f"Unsupported RV64M instruction: {op}"
            )

        # ----------------------------------------
        # Read Source Registers
        # ----------------------------------------

        rs1_val = thread.read_reg(
            decoded["rs1"]
        )

        rs2_val = thread.read_reg(
            decoded["rs2"]
        )

        # ----------------------------------------
        # Execute MUL/DIV Unit
        # ----------------------------------------

        result = MulDiv.execute(
            op,
            rs1_val,
            rs2_val
        )

        # ----------------------------------------
        # Write Back Result
        # ----------------------------------------

        thread.write_reg(
            decoded["rd"],
            result
        )

        # ----------------------------------------
        # Advance PC
        # ----------------------------------------

        thread.advance_pc()


# --------------------------------------------------
# Simple Self-Test
# --------------------------------------------------

if __name__ == "__main__":

    from cpu.thread_context import ThreadContext

    t = ThreadContext(0)

    t.write_reg(1, 20)
    t.write_reg(2, 5)

    mul_inst = {
        "op": "MUL",
        "rd": 3,
        "rs1": 1,
        "rs2": 2,
        "imm": None
    }

    RV64M.execute(
        t,
        None,
        mul_inst
    )

    print("MUL Result:", t.read_reg(3))

    div_inst = {
        "op": "DIV",
        "rd": 4,
        "rs1": 1,
        "rs2": 2,
        "imm": None
    }

    RV64M.execute(
        t,
        None,
        div_inst
    )

    print("DIV Result:", t.read_reg(4))

    rem_inst = {
        "op": "REM",
        "rd": 5,
        "rs1": 1,
        "rs2": 2,
        "imm": None
    }

    RV64M.execute(
        t,
        None,
        rem_inst
    )

    print("REM Result:", t.read_reg(5))