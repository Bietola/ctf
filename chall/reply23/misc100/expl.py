import subprocess
import string
import os

def esc(chrs):
    def f(c):
        if c == "'":
            return "'\\''"
        # if c == '`':
        #     return '\\`'
        else:
            return c

    return map(f, chrs)

for a in esc(string.printable[62:]):
    print(f'e: {a}')
    for b in esc(string.printable):
        print(f'i: {b}')
        for c in esc(string.printable):
            # print(f'ii: {c}')
            cmd = f"7z x -aoa -p'900802jfeng@veryrealmail.com{a + b + c}R3ply!' important_dental_information.zip"

            output = subprocess.run(
                cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
            ).stdout

            # print(output)

            if 'ERROR: Wrong password' not in output and 'ERROR: CRC Failed in encrypted file' not in output:
                print(cmd)
                print('found!!!')
                exit()
