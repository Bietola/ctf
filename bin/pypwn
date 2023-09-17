#!/usr/bin/env python

import fire
from pwn import *
import sys

def write(bs):
    sys.stdout.buffer.write(bs)

def cli(cmd, interactive=False, p_file=None):
    if p_file:
        p = process(p_file)

    exec(cmd)

    if interactive:
        if not p_file:
            raise Exception('You need to specify a process file (--p_file) to use interactive mode.')
        
        p.interactive()


fire.Fire(cli)
