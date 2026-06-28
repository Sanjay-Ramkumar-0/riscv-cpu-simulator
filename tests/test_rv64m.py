from cpu.thread_context import ThreadContext
from isa.rv64m import RV64M
from memory.memory import Memory

thread = ThreadContext(0)
memory = Memory()

thread.write_reg(1, 10)
thread.write_reg(2, 20)

decoded = {
    "op": "MUL",
    "rd": 3,
    "rs1": 1,
    "rs2": 2,
    "imm": None
}

RV64M.execute(
    thread,
    memory,
    decoded
)

print(
    thread.read_reg(3)
)