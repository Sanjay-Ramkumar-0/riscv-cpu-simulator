from utils.helpers import (
    mask64,
    to_signed
)


class ALU:

    @staticmethod
    def execute(op: str, a: int, b: int) -> int:

        if op == "ADD":
            return mask64(a + b)

        elif op == "SUB":
            return mask64(a - b)

        elif op == "AND":
            return mask64(a & b)

        elif op == "OR":
            return mask64(a | b)

        elif op == "XOR":
            return mask64(a ^ b)

        elif op == "SLL":
            return mask64(a << (b & 0x3F))

        elif op == "SRL":
            return mask64(a >> (b & 0x3F))

        elif op == "SRA":

            shift = b & 0x3F

            return mask64(
                to_signed(a, 64) >> shift
            )

        elif op == "SLT":

            return int(
                to_signed(a, 64)
                <
                to_signed(b, 64)
            )

        elif op == "SLTU":

            return int(
                mask64(a)
                <
                mask64(b)
            )

        else:
            raise ValueError(
                f"Unsupported ALU op: {op}"
            )
        
