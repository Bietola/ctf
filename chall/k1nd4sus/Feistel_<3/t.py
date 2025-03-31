from l import *

ctx = encrypt('ffffff', 0xffffffffffff.to_bytes(6), 1024)
ptx = decrypt(ctx,      0xffffffffffff.to_bytes(6), 1024)

print(ctx)
print(bytes.fromhex(ptx).decode('utf-8'))
