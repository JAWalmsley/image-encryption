from PIL import Image
import io

import hmac
import hashlib
import base64

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend


def image_to_bytes(img):
    p_img = Image.open(img)
    img_b_arr = io.BytesIO()
    p_img.save(img_b_arr, format=p_img.format)
    print("Image: ", img_b_arr.getvalue())
    return (img_b_arr.getvalue())


def bytes_to_image(bytes):
    stream = io.BytesIO(bytes)
    img = Image.open(stream).convert('RGBA')
    img.show()


def encrypt_data(data, given_password):
    password = given_password.encode()
    kdf = PBKDF2HMAC(
        algorithm=hashlib.sha512(),
        length=32,
        salt=b'',
        iterations=1000000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    print("Derived key: ", key)

    aes = Fernet(key)
    return aes.encrypt(data)


def decrypt_data(data, given_password):
    password = given_password.encode()
    kdf = PBKDF2HMAC(
        algorithm=hashlib.sha512(),
        length=32,
        salt=b'',
        iterations=1000000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))

    aes = Fernet(key)
    return aes.decrypt(data)


def encrypt_image(img, password):
    bytes = image_to_bytes(img)
    return encrypt_data(bytes, password)


def decrypt_image(data, password):
    img = decrypt_data(data, password)
    return bytes_to_image(img)


def create_signature(key, data):
    byte_key = key.encode()
    message = data.encode()
    return hmac.new(byte_key, data, hashlib.sha3_512).hexdigest().upper()
