from pwn import *

data = bytes.fromhex('233f6b67232a2e12266b386c3f2a6b326a2c2a272d')
print(bytes(map(lambda b: b ^ 0x4b, data))[::-1])

data = bytes.fromhex('6a2c2a272d6b32266b386c3f2a233f6b67232a2e12')
print(bytes(map(lambda b: b ^ 0x4b, data))[::-1])

data = bytes.fromhex('233f6b67232a2e12')
print(bytes(map(lambda b: b ^ 0x4b, data))[::-1])

data = bytes.fromhex('233f6b67232a2e12')[::-1] + bytes.fromhex('266b386c3f2a')[::-1] + bytes.fromhex('6b32')[::-1] + bytes.fromhex('6a2c2a272d')[::-1]
print(bytes(map(lambda b: b ^ 0x4b, data)))