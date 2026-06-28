"""
RV64I Instruction Execution Layer

Executes decoded RV64I instructions.
rv64i.py takes that decoded instruction and Reads registers, Calls execution units, Updates registers, Updates PC, Accesses memory
"""

from execution.alu import ALU
from execution.branch_unit import BranchUnit
from execution.agu import AGU


class RV64I:

    ALU_OPS = {
        "ADD",
        "SUB",
        "AND",
        "OR",
        "XOR",
        "SLL",
        "SRL",
        "SRA",
        "SLT",
        "SLTU"
    }

    @staticmethod
    def execute(
        thread,
        memory,
        decoded
    ) -> None:

        op = decoded["op"]

        # ==================================================
        # Generic ALU Operations
        # ==================================================

        if op in RV64I.ALU_OPS:

            a = thread.read_reg(
                decoded["rs1"]
            )

            b = thread.read_reg(
                decoded["rs2"]
            )

            result = ALU.execute(
                op,
                a,
                b
            )

            thread.write_reg(
                decoded["rd"],
                result
            )

            thread.advance_pc()

        # ==================================================
        # ADDI
        # ==================================================

        elif op == "ADDI":

            a = thread.read_reg(
                decoded["rs1"]
            )

            result = ALU.execute(
                "ADD",
                a,
                decoded["imm"]
            )

            thread.write_reg(
                decoded["rd"],
                result
            )

            thread.advance_pc()

        # ==================================================
        # LD
        # ==================================================

        elif op == "LD":

            base = thread.read_reg(
                decoded["rs1"]
            )

            addr = AGU.compute_address(
                base,
                decoded["imm"]
            )

            value = memory.read64(
                addr
            )

            thread.write_reg(
                decoded["rd"],
                value
            )

            thread.advance_pc()

        # ==================================================
        # SD
        # ==================================================

        elif op == "SD":

            base = thread.read_reg(
                decoded["rs1"]
            )

            addr = AGU.compute_address(
                base,
                decoded["imm"]
            )

            value = thread.read_reg(
                decoded["rs2"]
            )

            memory.write64(
                addr,
                value
            )

            thread.advance_pc()

        # ==================================================
        # Branch Instructions
        # ==================================================

        elif op in {
            "BEQ",
            "BNE",
            "BLT",
            "BGE",
            "BLTU",
            "BGEU"
        }:

            rs1_val = thread.read_reg(
                decoded["rs1"]
            )

            rs2_val = thread.read_reg(
                decoded["rs2"]
            )

            taken, target = (
                BranchUnit.execute(
                    op,
                    thread.get_pc(),
                    rs1_val,
                    rs2_val,
                    decoded["imm"]
                )
            )

            if taken:
                thread.set_pc(target)
            else:
                thread.advance_pc()

        # ==================================================
        # JAL
        # ==================================================

        elif op == "JAL":

            return_addr = (
                thread.get_pc() + 4
            )

            thread.write_reg(
                decoded["rd"],
                return_addr
            )

            thread.set_pc(
                thread.get_pc()
                +
                decoded["imm"]
            )

        # ==================================================
        # LUI
        # ==================================================

        elif op == "LUI":

            thread.write_reg(
                decoded["rd"],
                decoded["imm"]
            )

            thread.advance_pc()

        # ==================================================
        # AUIPC
        # ==================================================

        elif op == "AUIPC":

            value = (
                thread.get_pc()
                +
                decoded["imm"]
            )

            thread.write_reg(
                decoded["rd"],
                value
            )

            thread.advance_pc()

        # ==================================================
        # Unsupported
        # ==================================================

        else:

            raise ValueError(
                f"Unsupported RV64I instruction: {op}"
            )