from hashlib import sha256
from Crypto.Cipher import AES
from base64 import standard_b64decode
from Crypto.Util.number import bytes_to_long, long_to_bytes
from Crypto.Random.random import randint
from Crypto.Util.Padding import pad, unpad
import subprocess

def long_to_base64(n):
    return standard_b64encode(long_to_bytes(n)).decode()

def encrypt(cipher, msg):
    return standard_b64encode(cipher.encrypt(pad(msg, 16))).decode()

def base64_to_long(e):
    return bytes_to_long(standard_b64decode(e))

def decrypt(cipher, e):
    return unpad(cipher.decrypt(standard_b64decode(e)), 16)

cipher = None

def handle(j):
    global cipher
    if cipher is None:
        p = base64_to_long(j['p'])
        print("p:", p)
        g = base64_to_long(j['g'])
        print("g:", g)
        A = base64_to_long(j['A'])
        print("A:", A)
        b = randint(1, p)
        shared = pow(A, b, p)
        shared = sha256(long_to_bytes(shared)).digest()
        cipher = AES.new(shared, AES.MODE_ECB)
        return {
            'B': long_to_base64(pow(g, b, p))
        }

    cmd = decrypt(cipher, j['rpc'])
    return {
        'return': encrypt(cipher, subprocess.check_output(cmd))
    }

p = "h3rl/Q=="
g = "Ag=="
A = "QpFOyA=="

B = "Ph6IeA=="

p_int = base64_to_long(p)
print("p:", p_int)
g_int = base64_to_long(g)
print("g:", g_int)
A_int = base64_to_long(A)
print("A:", A_int)

B_int = base64_to_long(B)
print("B:", B_int)

b_int = 620620105

shared = pow(A_int, b_int, p_int)
shared = sha256(long_to_bytes(shared)).digest()
cipher = AES.new(shared, AES.MODE_ECB)

print(decrypt(cipher, "GkSU2VwQyFe5Jt0Vd0cfxw=="))
print(decrypt(cipher, "TMxn+S2kBNd/4YsXYhtH0qgvBmUZiArgyTNOCqPsuFQOwcAo4SjQ4T4K14JvHvBX"))
