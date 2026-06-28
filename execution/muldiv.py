#SR-Core Multiply / Divide Unit

from utils.helpers import (
    mask64,
    to_signed,
    to_unsigned
)


class MulDiv:

    @staticmethod
    def execute(
        op: str,
        a: int,
        b: int
    ) -> int:

        # ----------------------------
        # Multiply
        # ----------------------------

        if op == "MUL":

            return mask64(a * b)

        elif op == "MULH":

            product = (
                to_signed(a, 64)
                *
                to_signed(b, 64)
            )

            return mask64(product >> 64)

        # ----------------------------
        # Divide
        # ----------------------------

        elif op == "DIV":

            if b == 0:
                return 0xFFFFFFFFFFFFFFFF

            return mask64(
                int(
                    to_signed(a, 64)
                    /
                    to_signed(b, 64)
                )
            )

        elif op == "DIVU":

            if b == 0:
                return 0xFFFFFFFFFFFFFFFF

            ua = to_unsigned(a, 64)
            ub = to_unsigned(b, 64)

            return mask64(ua // ub)

        # ----------------------------
        # Remainder
        # ----------------------------

        elif op == "REM":

            if b == 0:
                return mask64(a)

            return mask64(
                to_signed(a, 64)
                %
                to_signed(b, 64)
            )

        elif op == "REMU":

            if b == 0:
                return mask64(a)

            ua = to_unsigned(a, 64)
            ub = to_unsigned(b, 64)

            return mask64(
                ua % ub
            )

        else:
            raise ValueError(
                f"Unsupported MUL/DIV op: {op}"
            )
        
if __name__ == "__main__":

    print(MulDiv.execute("MUL", 10, 20))

    print(MulDiv.execute("DIV", 20, 5))

    print(MulDiv.execute("REM", 20, 6))

    print(
        hex(
            MulDiv.execute(
                "DIV",
                20,
                0
            )
        )
    )