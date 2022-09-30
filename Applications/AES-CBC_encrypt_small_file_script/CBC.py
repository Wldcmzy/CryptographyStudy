from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from base64 import b64encode, b64decode
from typing import Union
import hashlib

def encrypt_CBC(filename: str, targetname: str, key: Union[str, bytes], iv: Union[str, bytes], add_md5: bool = True):
    '''md5内置于文件头部用于检验文件是否被更改'''
    if type(key) == str: key = key.encode('utf-8')
    if type(iv) == str: iv = iv.encode('utf-8')
    with open(filename, 'rb') as fin: origintext = fin.read()
    origintext = pad(origintext, AES.block_size, style='pkcs7')
    cipher = AES.new(key, AES.MODE_CBC, iv = iv)
    ciphertext = cipher.encrypt(origintext)
    if add_md5:
        md5 = hashlib.md5(ciphertext).hexdigest()
        targetname += '_md5_' + md5
        ciphertext = md5.encode('utf-8') + ciphertext
    with open(targetname, 'wb') as fout: fout.write(ciphertext)
        
def decrypt_CBC(filename: str, targetname: str, key: Union[str, bytes], iv: Union[str, bytes], del_md5: bool = True):
    if type(key) == str: key = key.encode('utf-8')
    if type(iv) == str: iv = iv.encode('utf-8')
    with open(filename, 'rb') as fin: ciphertext = fin.read()
    cipher = AES.new(key, AES.MODE_CBC, iv = iv)
    if del_md5:
        print(f'md5: {ciphertext[ : len("be156139ca476ea31d941f4d4f3e2ae2")]}')
        ciphertext = ciphertext[len('be156139ca476ea31d941f4d4f3e2ae2') : ]
    plaintext = cipher.decrypt(ciphertext)
    plaintext = unpad(plaintext, AES.block_size, style='pkcs7')
    with open(targetname, 'wb') as fout: fout.write(plaintext)

if __name__ == '__main__':
    while True:
        op = int(input('''
0. 退出
1. 加密
2. 解密
 >>> '''))
        
        if op == 0:
            break

        elif op in [1, 2]:
            filename = input('filename:')
            targetname = input('targetname:')
            key = input('key:')
            iv = input('iv:')

            if op == 1:
                encrypt_CBC(filename, targetname, key, iv)
            else:
                decrypt_CBC(filename, targetname, key, iv)



