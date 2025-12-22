'''
Function:
    Implementation of SecretUtils
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import os
import base64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


'''SecretUtils'''
class SecretUtils():
    '''b64encode'''
    @staticmethod
    def b64encode(string: str):
        return base64.b64encode(string.encode("utf-8")).decode("ascii")
    '''b64decode'''
    @staticmethod
    def b64decode(b64_string: str):
        return base64.b64decode(b64_string).decode("utf-8")
    '''encryptaesgcm'''
    @staticmethod
    def encryptaesgcm(plaintext: str, key: bytes) -> str:
        aesgcm = AESGCM(key)
        nonce = os.urandom(12)
        ct = aesgcm.encrypt(nonce, plaintext.encode("utf-8"), associated_data=None)
        return base64.urlsafe_b64encode(nonce + ct).decode("ascii")
    '''decryptaesgcm'''
    @staticmethod
    def decryptaesgcm(token: str, key: bytes) -> str:
        data = base64.urlsafe_b64decode(token.encode("ascii"))
        nonce, ct = data[:12], data[12:]
        aesgcm = AESGCM(key)
        pt = aesgcm.decrypt(nonce, ct, associated_data=None)
        return pt.decode("utf-8")