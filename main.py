"""
SR-Core Simulator Entry Point
"""

from cpu.cpu import CPU


def main():

    print(
        "==================================="
    )

    print(
        "SR-Core RV64IM Simulator"
    )

    print(
        "==================================="
    )

    cpu = CPU()

    print(
        f"Threads : {len(cpu.threads)}"
    )

    print(
        "\nInitial CPU State:"
    )

    cpu.dump_state(0)

    print(
        "\nSimulation Complete."
    )


if __name__ == "__main__":

    main()