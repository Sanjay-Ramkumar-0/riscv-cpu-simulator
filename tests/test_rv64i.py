from cpu.thread_context import ThreadContext
from memory.memory import Memory
from isa.rv64i import RV64I

thread = ThreadContext(0)
memory = Memory()

thread.write_reg(1, 10)
thread.write_reg(2, 20)

decoded = {
    "op": "ADD",
    "rd": 3,
    "rs1": 1,
    "rs2": 2,
    "imm": None
}

RV64I.execute(
    thread,
    memory,
    decoded
)

print(
    thread.read_reg(3)
)