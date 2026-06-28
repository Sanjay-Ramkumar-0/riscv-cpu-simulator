from cpu.thread_context import ThreadContext

t = ThreadContext(0)

t.write_reg(1, 123) #register write works

print(t.read_reg(1))

t.write_reg(0, 999)

print(t.read_reg(0)) #x0 register is always 0

t.advance_pc() #PC update works

print(t.get_pc())