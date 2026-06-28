from memory.memory import Memory

mem = Memory()

mem.write64(0x100, 123456)

print(mem.read64(0x100))