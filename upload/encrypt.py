from PIL import Image
import io

import hmac
import hashlib
import base64

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend

KDF_ITERATIONS = 10000000


def image_to_bytes(img):
    """
    Converts an image file into a bytes object
    :param img: the uploaded file to convert
    :return: a bytes representation of img
    """
    p_img = Image.open(img)
    img_b_arr = io.BytesIO()
    p_img.save(img_b_arr, format=p_img.format)
    # print("Image: ", img_b_arr.getvalue())
    return (img_b_arr.getvalue())


def bytes_to_image(bytes):
    """
    Converts a bytes object into a PIL Image
    :param bytes: the bytes object to convert
    :return: a PIL Image object from bytes
    """
    stream = io.BytesIO(bytes)
    img = Image.open(stream).convert('RGB')
    return img


def encrypt_data(data, given_password):
    """
    Encrypts data using the given password, using PBKDF2
    :param data: the bytes object to encrypt
    :param given_password: the password to derive the key from, with PBKDF2
    :return: a bytes object of the encrypted data
    """
    key = key_derivation_function(given_password)
    aes = Fernet(key)
    return aes.encrypt(data)


def decrypt_data(data, given_password):
    """
    Decrypts data using the given password
    :param data: the bytes object to decrypt
    :param given_password: the password to derive the key from, with PBKDF2
    :return: a bytes object of the decrypted data
    """
    key = key_derivation_function(given_password)
    aes = Fernet(key)
    return aes.decrypt(data)


def key_derivation_function(given_password, iterations=KDF_ITERATIONS):
    """
    Derives a key from a password with PBKDF2
    :param given_password: the password to derive the key from
    :param iterations: the number of iterations to use in the key derivation, default KDF_ITERATIONS
    :return: a Base64 key
    """
    kdf = PBKDF2HMAC(
        algorithm=hashlib.sha512(),
        length=32,
        salt=b'',
        iterations=KDF_ITERATIONS,
        backend=default_backend()
    )
    return base64.urlsafe_b64encode(kdf.derive(given_password.encode()))


def encrypt_image(img, password):
    """
    Encrypts an image file
    :param img: the image file to encrypt
    :param password: the password to encrypt with
    :return: the encrypted data as bytes
    """
    img_bytes = image_to_bytes(img)
    return encrypt_data(img_bytes, password)


def decrypt_image(data, password):
    """
    Returns Base64 representation of decrypted image
    :param data: the encrypted bytes to decrypt
    :param password: the password to decrypt with
    :return: the decrypted image as Base64
    """
    img_bytes = decrypt_data(data, password)
    img = bytes_to_image(img_bytes)
    img_bytesIO = io.BytesIO()
    img.save(img_bytesIO, format='JPEG')
    b64 = base64.b64encode(img_bytesIO.getvalue())
    return b64


def create_signature(key, data):
    """
    Creates a HMAC signature of data
    :param key: the key to use with HMAC
    :param data: the data to create a signature of
    :return: the signature
    """
    byte_key = key.encode()
    message = data.encode()
    return hmac.new(byte_key, data, hashlib.sha3_512).hexdigest().upper()
