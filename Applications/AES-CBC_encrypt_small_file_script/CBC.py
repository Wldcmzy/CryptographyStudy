from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from base64 import b64encode, b64decode
from typing import Union, Optional
import hashlib
import os
import getpass

__version__ = '221002.01'

LEN_HEAD = len('md5_') + len("be156139ca476ea31d941f4d4f3e2ae2")

def encrypt_CBC(
    filename: str, 
    targetname: str, 
    key: Union[str, bytes], 
    iv: Union[str, bytes], 
    add_md5: bool = True
):
    '''md5内置于文件头部用于检验文件是否被更改'''
    if type(key) == str: key = key.encode('utf-8')
    if type(iv) == str: iv = iv.encode('utf-8')
    with open(filename, 'rb') as fin: origintext = fin.read()
    origintext = pad(origintext, AES.block_size, style='pkcs7')
    cipher = AES.new(key, AES.MODE_CBC, iv = iv)
    ciphertext = cipher.encrypt(origintext)
    if add_md5:
        md5 = 'md5_' + hashlib.md5(ciphertext).hexdigest()
        # targetname += '_md5_' + md5
        ciphertext = md5.encode('utf-8') + ciphertext
    with open(targetname, 'wb') as fout: fout.write(ciphertext)
        
def decrypt_CBC(
    filename: str, 
    targetname: str, 
    key: Union[str, bytes], 
    iv: Union[str, bytes], 
    del_md5: bool = True
):
    if type(key) == str: key = key.encode('utf-8')
    if type(iv) == str: iv = iv.encode('utf-8')
    with open(filename, 'rb') as fin: ciphertext = fin.read()
    cipher = AES.new(key, AES.MODE_CBC, iv = iv)
    if del_md5:
        print(f'md5: {ciphertext[ : LEN_HEAD]}')
        ciphertext = ciphertext[LEN_HEAD : ]
    plaintext = cipher.decrypt(ciphertext)
    plaintext = unpad(plaintext, AES.block_size, style='pkcs7')
    with open(targetname, 'wb') as fout: fout.write(plaintext)

def batch(
    mode: int, 
    foldername: str, 
    key: Union[str, bytes], 
    iv: Union[str, bytes], 
    has_md5: bool = True, 
    suffix: str = '.EAX',
    newfolder: Optional[str] = None
):
    assert len(suffix) >= 1
    if mode == 3:
        for P, D, F in os.walk(foldername):
            for f in F:
                if newfolder != None: P2 =  newfolder + '\\' + P
                if not os.path.exists(P2): os.makedirs(P2)
                filename = P + '\\' + f
                targetname = P2 + '\\' + f + suffix
                print(filename)
                encrypt_CBC(filename, targetname, key, iv, has_md5)
    elif mode == 4:
        for P, D, F in os.walk(foldername):
            for f in F:
                if f[- len(suffix) : ] == suffix:
                    if newfolder != None: P2 =  newfolder + '\\' + P
                    if not os.path.exists(P2): os.makedirs(P2)
                    filename, targetname = P + '\\' + f, P2 + '\\' + f[ : - len(suffix)]
                    print(filename)
                    decrypt_CBC(filename, targetname, key, iv, has_md5)


if __name__ == '__main__':
    while True:
        op = int(input('''
0. 退出
1. 文件加密
2. 文件解密
3. 子目录文件批量加密(相对路径)
4. 子目录文件批量解密(相对路径)
 >>> '''))
        
        if op == 0:
            break

        elif op in [1, 2]:
            filename = input('filename:')
            targetname = input('targetname:')
            key = getpass.getpass('key:')
            iv = getpass.getpass('iv:')

            if op == 1:
                encrypt_CBC(filename, targetname, key, iv)
            else:
                decrypt_CBC(filename, targetname, key, iv)
        
        elif op in [3, 4]:
            foldername = input('foldername:')
            key = getpass.getpass('key:')
            iv = getpass.getpass('iv:')
            newfolder = input('newfolder:')

            batch(op, foldername, key, iv, newfolder = newfolder)



