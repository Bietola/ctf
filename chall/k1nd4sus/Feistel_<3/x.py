from pwn import *
from time import sleep

from Crypto.Util.number import bytes_to_long, getPrime, long_to_bytes
from Crypto.Util.Padding import pad
import os, signal

from l import *

EX_NAME = './vuln-32'

# elf = ELF(EX_NAME)
# context.arch = 'x86'
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
        p = process(['python', 'crypto.py'])

def dbg_stop():
    if 'GDB' in os.environ:
        input('Waiting...')

sleep(0.5)
line = p.recvline()
log.info(line)
flag = int(line[line.find(b'=')+1:], 16)
log.success(f'flag: {hex(flag)}')

sleep(0.5)
line = p.recvline()
log.info(line)
N = int(line[line.find(b'=')+1:], 10)
log.success(f'N: {N}')

sleep(0.5)
log.info(p.clean())

# p1 = 0xffff0000ffff
# p2 = f1(0xffff, o1[4:], N)
# p3 = f1(0xffff, o2[4:], N)
# p4 = f1(0xffff, o3[4:], N)

o = [0]*4
key = [0]*4

sleep(0.5)
p.sendline(b'1')

sleep(0.5)
p.sendline(b'ffff0000ffff')

sleep(0.5)
line = p.recvline()
log.info(line)
o[0] = int(line[line.rfind(b':')+1:], 16)
key[0] = int(line[-5:], 16)
log.success(f'o0: {o[0]:#x}')
log.success(f'key0: {key[0]:#x}')
log.info(p.clean())

for i in range(1, 4):
    sleep(0.5)
    p.sendline(b'1')

    sleep(0.5)
    pl = f1(0xffff.to_bytes(2), key[i-1].to_bytes(2), N)
    log.info(f'Sending 00000000{pl.hex()}')
    p.sendline(f'{pl.hex()}'.encode('utf-8'))

    sleep(0.5)
    line = p.recvline()
    log.info(line)
    o[i] = int(line[line.rfind(b':')+1:], 16)
    key[i] = int(line[-5:], 16)
    log.success(f'o{i}: {o[i]:#x}')
    log.success(f'key{i}: {key[i]:#x}')
    log.info(p.clean())

key = int(''.join(map(lambda x: f'{x:x}', key)), 16)
log.success(f'KEY: {hex(key)}')

flag_d = decrypt(f'{flag:x}', key.to_bytes(8), N)
log.success(f'FLAG: {flag_d}')

sleep(0.5)
p.interactive()
