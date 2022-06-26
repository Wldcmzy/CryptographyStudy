from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

__Mode__ = 'ECB'

with open('test.txt', 'rb') as fin:
    origintext = fin.read()
    origintext = pad(origintext, AES.block_size, style='pkcs7')

key = get_random_bytes(16)
cipher = AES.new(key, AES.MODE_ECB)

ciphertext = cipher.encrypt(origintext)

plaintext = cipher.decrypt(ciphertext)
plaintext = unpad(plaintext, AES.block_size, style='pkcs7')

with open(f'{__Mode__}_encrypted.txt', 'wb') as fout:
    fout.write(ciphertext)
with open(f'{__Mode__}_decrypted.txt', 'wb') as fout:
    fout.write(plaintext)

