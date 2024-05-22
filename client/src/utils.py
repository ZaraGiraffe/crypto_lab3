import requests
import time
from .settings import SERVER
from .aes import encrypt, decrypt
import json
import hashlib

def send_message(from_name, to_name, message, hash_data):
    timestamp = time.time()
    url = SERVER + "send/"
    data = {
        "from": from_name,
        "to": to_name,
        "timestamp": timestamp,
        "message": message,
        "hash": hashlib.sha256(message).hexdigest()
    }
    headers = {"Content-Type": "application/json"}

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        return {"status": "error code: {}".format(response.status_code)}


def get_message(from_name, to_name):
    url = SERVER + "get/"
    data = {
        "from": from_name,
        "to": to_name,
    }
    headers = {"Content-Type": "application/json"}

    response = requests.get(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        return {"status": "error code: {}".format(response.status_code)}


def int_to_bytearray(integer):
    hex_string = format(integer, 'x').zfill(64)  # Format as hex, zero-pad to 64 characters
    return bytearray.fromhex(hex_string)


def encrypt_message(key: int, message: str):
    key_bytes = int_to_bytearray(key)
    enc = encrypt(key_bytes, message)
    return str(list(enc))


def decrypt_message(key: int, message_enc: str):
    key_bytes = int_to_bytearray(key)
    message_list_bytes = json.loads(message_enc)
    message_enc_bytes = bytearray(message_list_bytes)
    message_bytes = decrypt(key_bytes, message_enc_bytes)
    return message_bytes.decode()
