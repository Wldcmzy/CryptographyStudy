from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from base64 import b64encode, b64decode

__Mode__ = 'CBC'

with open('test.txt', 'rb') as fin:
    origintext = fin.read()
    origintext = pad(origintext, AES.block_size, style='pkcs7')

key = get_random_bytes(16)
cipher = AES.new(key, AES.MODE_CBC) # iv 自动生成
ciphertext = cipher.encrypt(origintext)
# iv = b64encode(cipher.iv).decode('utf-8')
# 解密需要一个新的AES对象
cipher2 = AES.new(key, AES.MODE_CBC, cipher.iv) # 需要填入对应的iv
plaintext = cipher2.decrypt(ciphertext)
plaintext = unpad(plaintext, AES.block_size, style='pkcs7')

with open(f'{__Mode__}_encrypted.txt', 'wb') as fout:
    fout.write(ciphertext)
with open(f'{__Mode__}_decrypted.txt', 'wb') as fout:
    fout.write(plaintext)
