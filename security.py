# Simple reversible "encryption" for the lab demo (not secure in real life)
# Uses XOR with a fixed key + Base64. Meets the "encrypted in file, decrypted on login" requirement.
# For real applications, use proper cryptography.

import base64
from itertools import cycle

_KEY = b"checkmygrade-key"  # you can change this key

def _xor_bytes(data: bytes, key: bytes) -> bytes:
    return bytes(d ^ k for d, k in zip(data, cycle(key)))

def encrypt_password(plain: str) -> str:
    raw = plain.encode("utf-8")
    xored = _xor_bytes(raw, _KEY)
    return base64.urlsafe_b64encode(xored).decode("ascii")

def decrypt_password(cipher_b64: str) -> str:
    xored = base64.urlsafe_b64decode(cipher_b64.encode("ascii"))
    raw = _xor_bytes(xored, _KEY)
    return raw.decode("utf-8")
