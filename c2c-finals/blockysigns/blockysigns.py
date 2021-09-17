import io
import sys
from pathlib import Path

# pip install pillow cryptography
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from PIL import Image

SALT = b"13371337133713371337133713371337"


def encrypt(key: bytes, plaintext: bytes) -> bytes:
    """
    Symmetric encrypt bytes
    """
    encryptor = Cipher(algorithms.AES(key), mode=modes.ECB()).encryptor()
    padder = padding.PKCS7(128).padder()
    padded_plaintext = padder.update(plaintext) + padder.finalize()
    return encryptor.update(padded_plaintext) + encryptor.finalize()


def decrypt(key: bytes, ciphertext: bytes) -> bytes:
    """
    Symmetric decrypt bytes
    """
    decryptor = Cipher(algorithms.AES(key), mode=modes.ECB()).decryptor()
    return decryptor.update(ciphertext) + decryptor.finalize()


def convert_image(src_path: str) -> bytes:
    """
    Read image from path and convert into bytes in PPM image format
    """
    im = Image.open(src_path)
    # Weird hack to get to save as bytes rather than to disk
    bb = io.BytesIO()
    im.save(bb, "ppm")
    return bb.getvalue()


def main_encrypt():
    image_bytes = convert_image(sys.argv[1])
    password = input("Encryption Password: ")
    # This key derivation process should genuinely be strong.
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=SALT, iterations=100000)
    key = kdf.derive(password.encode())

    encrypted_bytes = encrypt(key, image_bytes)

    # Determine output path name
    img_path = Path(sys.argv[1]).resolve()
    file_name = img_path.name
    name_without_ext = ".".join(file_name.split(".")[:-1])
    output_name = f"{name_without_ext}.ppm.enc"
    output_path = img_path.parent / output_name

    with output_path.open("wb") as f:
        f.write(encrypted_bytes)
    print(f"Saved encrypted image to {output_path}")


def main_decrypt():
    print("Unfortunately we don't yet support decryption")
    raise NotImplementedError()


def main():
    if not 2 <= len(sys.argv) <= 3:
        print(
            "Usage: python blockysigns.py myimage.png OR python blocksigns.py -d myimage.ppm.enc"
        )
        sys.exit(1)
    if "-d" in sys.argv:
        main_decrypt()
    else:
        main_encrypt()


if __name__ == "__main__":
    main()
