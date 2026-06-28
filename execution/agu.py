#Address Generation Unit

from utils.helpers import (
    mask64,
    sign_extend
)


class AGU:

    @staticmethod
    def compute_address(
        base: int,
        offset: int
    ) -> int:
        """
        Compute effective memory address.

        Address = Base + Offset
        """

        return mask64(base + offset)