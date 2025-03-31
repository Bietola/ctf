from pwn import *
from time import sleep

from Crypto.Util.number import bytes_to_long, getPrime, long_to_bytes
from Crypto.Util.Padding import pad, unpad
import os, signal

def f1(output, round_key, modulus):
    output_long = bytes_to_long(output)
    round_key_value = pow(65537, bytes_to_long(round_key), modulus)
    inverted_result = (output_long - round_key_value) % (1 << 17 - 1)
    return long_to_bytes(inverted_result).ljust(2, b'\x00')

def xor_bytes(bytes_a, bytes_b):
    return bytes(a ^ b for a, b in zip(bytes_a, bytes_b)).ljust(2, b'\x00')

def f(sub_block, round_key, modulus):
    return long_to_bytes((bytes_to_long(sub_block) + pow(65537, bytes_to_long(round_key), modulus)) % (1<<17-1)).ljust(2, b'\x00')

def encrypt_block(block, key, modulus, rounds=8, shortcut=False):

    sub_block_1 = block[:2].ljust(2, b'\x00')
    sub_block_2 = block[2:4].ljust(2, b'\x00')
    sub_block_3 = block[4:].ljust(2, b'\x00')
    for i in range(0, rounds):
        round_key = key[i*2:i*2+2]
        new_sub_block_1 = xor_bytes(sub_block_1, sub_block_2) 
        new_sub_block_2 = f(sub_block_3, round_key, modulus)
        new_sub_block_3 = xor_bytes(sub_block_2, round_key)
        sub_block_1 = new_sub_block_1
        sub_block_2 = new_sub_block_2
        sub_block_3 = new_sub_block_3
        if shortcut and sub_block_1 == b"\xff\xff":
            break
    return sub_block_1 + sub_block_2 + sub_block_3

def encrypt(plaintext, key, modulus):
    iv = os.urandom(6)
    padded = pad(plaintext.encode(), 6)
    blocks = [padded[i:i+6] for i in range(0, len(padded), 6)] 
    res = []
    for i in range(len(blocks)):
        if i == 0: block = xor_bytes(blocks[i], iv)
        else: block = xor_bytes(blocks[i], bytes.fromhex(res[-1]))
        res.append(encrypt_block(block, key, modulus).hex())
    return iv.hex() + "".join(res)

def decrypt_block(block, key, modulus, rounds=8, shortcut=False):
    sub_block_1 = block[:2].ljust(2, b'\x00')
    sub_block_2 = block[2:4].ljust(2, b'\x00')
    sub_block_3 = block[4:].ljust(2, b'\x00')
    for i in range(rounds-1, -1, -1):
        round_key = key[i*2:i*2+2]
        new_sub_block_3 = xor_bytes(sub_block_3, round_key)
        new_sub_block_2 = f1(sub_block_2, round_key, modulus)
        new_sub_block_1 = xor_bytes(sub_block_1, new_sub_block_2)
        sub_block_1 = new_sub_block_1
        sub_block_2 = new_sub_block_2
        sub_block_3 = new_sub_block_3
        if shortcut and sub_block_1 == b"\xff\xff":
            break
    return sub_block_1 + sub_block_2 + sub_block_3

def decrypt(ciphertext, key, modulus):
    iv = bytes.fromhex(ciphertext[:12])
    encrypted_blocks = [ciphertext[i:i+12] for i in range(12, len(ciphertext), 12)]
    res = []
    for i in range(len(encrypted_blocks)):
        block = bytes.fromhex(encrypted_blocks[i])
        decrypted_block = decrypt_block(block, key, modulus)
        if i == 0:
            plaintext_block = xor_bytes(decrypted_block, iv)
        else:
            plaintext_block = xor_bytes(decrypted_block, bytes.fromhex(encrypted_blocks[i-1]))
        res.append(plaintext_block)
    # Join all blocks and unpad
    plaintext = b''.join(res)
    try:
        plaintext = unpad(plaintext, 6).decode('utf-8')
    except ValueError as e:
        print("Padding error:", e)
        print("Decrypted plaintext (hex):", plaintext.hex())
        raise
    return plaintext
