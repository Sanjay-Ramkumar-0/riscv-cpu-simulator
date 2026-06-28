from cpu.cpu import CPU


cpu = CPU()

# ADDI x1, x0, 10
instruction = 0x00A00093

cpu.memory.write32(
    0,
    instruction
)

print("Before Execution:")
cpu.dump_state(0)

cpu.step(0)

print("\nAfter Execution:")
cpu.dump_state(0)

print(
    f"\nx1 = {cpu.threads[0].read_reg(1)}"
)

print(
    f"PC = {cpu.threads[0].get_pc()}"
)