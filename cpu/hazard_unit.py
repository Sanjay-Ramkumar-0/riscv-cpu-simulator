"""
Hazard Detection Unit

Detects hazards that cannot yet be solved
by forwarding.

Current design:
- Forwarding handles EX_MEM and MEM_WB
- Stall only when producer is in ID_EX
"""


class HazardUnit:

    @staticmethod
    def has_raw_hazard(
        if_id_decoded,
        id_ex,
        ex_mem,
        mem_wb
    ) -> bool:

        if if_id_decoded is None:
            return False

        if id_ex is None:
            return False

        producer = id_ex["decoded"]

        producer_rd = producer.get("rd")

        if producer_rd is None:
            return False

        if producer_rd == 0:
            return False

        rs1 = if_id_decoded.get("rs1")
        rs2 = if_id_decoded.get("rs2")

        if rs1 is not None and rs1 == producer_rd:
            return True

        if rs2 is not None and rs2 == producer_rd:
            return True

        return False