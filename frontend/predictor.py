# Store prediction table, Predict Taken / Not Taken, Update predictor after branch executes

"""
2-Bit Dynamic Branch Predictor

Each branch instruction (identified by its PC)
has a 2-bit saturating counter.

Counter States

0 : Strongly Not Taken
1 : Weakly Not Taken
2 : Weakly Taken
3 : Strongly Taken

Prediction

0,1 -> Not Taken
2,3 -> Taken
"""


class BranchPredictor:

    # =====================================
    # Constructor
    # =====================================

    def __init__(self):

        # Branch History Table
        #
        # Key   : Branch PC
        # Value : 2-bit counter

        self.table = {}

    # =====================================
    # Predict Branch Direction
    # =====================================

    def predict(
        self,
        pc: int
    ) -> bool:

        # Default state:
        # Weakly Not Taken

        counter = self.table.get(
            pc,
            1
        )

        # States 2 and 3 predict TAKEN

        return counter >= 2

    # =====================================
    # Update Predictor
    # =====================================

    def update(
        self,
        pc: int,
        taken: bool
    ) -> None:

        counter = self.table.get(
            pc,
            1
        )

        if taken:

            if counter < 3:
                counter += 1

        else:

            if counter > 0:
                counter -= 1

        self.table[pc] = counter

    # =====================================
    # Read Counter
    # (Useful for debugging)
    # =====================================

    def get_counter(
        self,
        pc: int
    ) -> int:

        return self.table.get(
            pc,
            1
        )

    # =====================================
    # Reset Predictor
    # =====================================

    def reset(self) -> None:

        self.table.clear()

    # =====================================
    # Dump Predictor Table
    # =====================================

    def dump(self) -> None:

        print("\n========== Branch Predictor ==========")

        if not self.table:

            print("Empty")

        else:

            for pc in sorted(self.table):

                counter = self.table[pc]

                state = {
                    0: "Strong NT",
                    1: "Weak NT",
                    2: "Weak T",
                    3: "Strong T"
                }[counter]

                print(
                    f"PC 0x{pc:08X} -> "
                    f"{counter} ({state})"
                )

        print("======================================")

if __name__ == "__main__":

    predictor = BranchPredictor()

    pc = 0x100

    print("Initial Prediction:")
    print(
        predictor.predict(pc)
    )

    print(
        predictor.get_counter(pc)
    )

    # Simulate:
    #
    # Taken
    # Taken
    # Taken
    # Not Taken
    # Taken

    sequence = [
        True,
        True,
        True,
        False,
        True
    ]

    for taken in sequence:

        predictor.update(
            pc,
            taken
        )

        print(
            f"\nActual : {taken}"
        )

        print(
            "Prediction :",
            predictor.predict(pc)
        )

        print(
            "Counter :",
            predictor.get_counter(pc)
        )

    predictor.dump()