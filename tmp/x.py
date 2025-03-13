from pwn import *

p = process('./vuln')

p.sendline(b'hey there')

p.interactive()
