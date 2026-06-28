"""
Returns a tuple
It doesn't update the PC, it just returns the new PC if the branch is taken and to check if the branch is taken.
"""

from utils.helpers import (
    mask64,
    to_signed
)


class BranchUnit:

    @staticmethod
    def execute(
        op: str,
        pc: int,
        rs1: int,
        rs2: int,
        imm: int
    ) -> tuple[bool, int]:
        """
        Returns:
            (taken, target)
        """

        # ---------------------------------
        # Conditional Branches
        # ---------------------------------

        if op == "BEQ":

            taken = (rs1 == rs2)
            target = mask64(pc + imm)

        elif op == "BNE":

            taken = (rs1 != rs2)
            target = mask64(pc + imm)

        elif op == "BLT":

            taken = (
                to_signed(rs1, 64)
                <
                to_signed(rs2, 64)
            )

            target = mask64(pc + imm)

        elif op == "BGE":

            taken = (
                to_signed(rs1, 64)
                >=
                to_signed(rs2, 64)
            )

            target = mask64(pc + imm)

        elif op == "BLTU":

            taken = (
                mask64(rs1)
                <
                mask64(rs2)
            )

            target = mask64(pc + imm)

        elif op == "BGEU":

            taken = (
                mask64(rs1)
                >=
                mask64(rs2)
            )

            target = mask64(pc + imm)

        # ---------------------------------
        # Unconditional Jumps
        # ---------------------------------

        elif op == "JAL":

            taken = True
            target = mask64(pc + imm)

        elif op == "JALR":

            taken = True
            target = mask64(rs1 + imm)

            # RISC-V requirement:
            target &= ~1

        else:
            raise ValueError(
                f"Unsupported branch op: {op}"
            )

        return taken, target
    
