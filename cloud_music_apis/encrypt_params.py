
import os
import json
import codecs
import base64
from Crypto.Cipher import AES


class EncryptParams:

    def __init__(self):
        self.modulus = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
        self.nonce = '0CoJUm6Qyw8W8jud'
        self.pubKey = '010001'

    def get(self, text) -> map:
        text = json.dumps(text)
        sec_key = (''.join(
            map(lambda xx: (hex(ord(xx))[2:]), str(os.urandom(16)))))[0:16]

        # 加密两次
        enc_text = self._aes_encrypt(self._aes_encrypt(text, self.nonce), sec_key)

        encsec_key = self._rsa_encrypt(sec_key, self.pubKey, self.modulus)

        # 生成 网易云 body payload
        post_data = {
            'params': enc_text,
            'encSecKey': encsec_key
        }

        return post_data

    def _aes_encrypt(self, text, sec_key):
        pad = 16 - len(text) % 16
        if isinstance(text, bytes):
            text = text.decode('utf-8')
        text = text + str(pad * chr(pad))
        sec_key = sec_key.encode('utf-8')
        encryptor = AES.new(sec_key, 2, b'0102030405060708')
        text = text.encode('utf-8')
        ciphertext = encryptor.encrypt(text)
        ciphertext = base64.b64encode(ciphertext)
        return ciphertext

    def _rsa_encrypt(self, text, pubKey, modulus):
        text = text[::-1]
        rs = int(codecs.encode(text.encode('utf-8'), 'hex_codec'), 16) ** int(
            pubKey, 16) % int(modulus, 16)
        return format(rs, 'x').zfill(256)


def generate_encrypt_params(params) -> map:
    return EncryptParams().get(params)
