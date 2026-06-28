"""
Forwarding Unit

Provides data forwarding (bypassing)
from later pipeline stages to the EX stage.

Priority:

1. EX_MEM (newest value)
2. MEM_WB
3. Register File value
"""


class ForwardingUnit:

    @staticmethod
    def forward_operand(
        reg_num,
        reg_value,
        ex_mem,
        mem_wb
    ):
        """
        Return the most recent value for a register.

        Parameters
        ----------
        reg_num : int
            Source register number (rs1 or rs2)

        reg_value : int
            Value read from register file

        ex_mem : dict | None
            EX/MEM pipeline register

        mem_wb : dict | None
            MEM/WB pipeline register
        """

        # x0 is always zero

        if reg_num == 0:
            return 0

        # ==================================
        # Forward from EX_MEM
        # ==================================

        if ex_mem is not None:

            decoded = ex_mem["decoded"]

            rd = decoded.get("rd")

            if (
                rd is not None
                and rd != 0
                and rd == reg_num
            ):
                return ex_mem["result"]

        # ==================================
        # Forward from MEM_WB
        # ==================================

        if mem_wb is not None:

            decoded = mem_wb["decoded"]

            rd = decoded.get("rd")

            if (
                rd is not None
                and rd != 0
                and rd == reg_num
            ):
                return mem_wb["result"]

        # ==================================
        # No forwarding needed
        # ==================================

        return reg_value