from django.conf import settings
from Crypto.Cipher import AES

import base64


def __pad(raw):
    if (len(raw) % 16 == 0):
        return raw
    padding_required = 16 - (len(raw.encode('utf-8')) % 16)
    data = raw + '0' * padding_required
    return data


def encode(raw):
    aes = AES.new(settings.AES_ENCRIPTION_KEY, AES.MODE_ECB)
    encoded = base64.urlsafe_b64encode(aes.encrypt(__pad(raw))).decode("utf-8")
    encoded = encoded.replace("+", "%2B")
    return encoded


def decode(raw):
    aes = AES.new(settings.AES_ENCRIPTION_KEY, AES.MODE_ECB)
    raw = base64.urlsafe_b64decode(raw)
    raw = aes.decrypt(raw).decode('utf-8')
    raw = raw.rstrip("0")
    return raw
