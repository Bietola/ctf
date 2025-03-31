import fire

def invert_f(output, round_key, modulus):
    output_long = bytes_to_long(output)
    round_key_value = pow(65537, bytes_to_long(round_key), modulus)
    inverted_result = (output_long - round_key_value) % (1 << 17 - 1)
    return long_to_bytes(inverted_result).ljust(2, b'\x00')

def cli(x, k, N):
    invert_f(int(x, 16).to_bytes(), int(k, 16).to_bytes(), int(N, 16).to_bytes())

fire.Fire(cli)
