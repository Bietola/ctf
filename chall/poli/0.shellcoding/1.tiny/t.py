# QUESTION: Why doesn't it break?

from pwn import *

sh = '''
mov al, 0x0
shl eax
'''

context.arch = 'amd64'
context.terminal = ['konsole', '-e']
gdb.debug_shellcode(asm(sh), gdbscript='b _start')