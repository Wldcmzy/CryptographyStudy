from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

# CTR 可以不填充原文
__Mode__ = 'CTR'

with open('test.txt', 'rb') as fin:
    origintext = fin.read()

key = get_random_bytes(16)
cipher = AES.new(key, AES.MODE_CTR) # nonce 随机生成

ciphertext = cipher.encrypt(origintext)

cipher2 = AES.new(key, AES.MODE_CTR, nonce=cipher.nonce) # 填入固定的nonce
plaintext = cipher2.decrypt(ciphertext)

with open(f'{__Mode__}_encrypted.txt', 'wb') as fout:
    fout.write(ciphertext)
with open(f'{__Mode__}_decrypted.txt', 'wb') as fout:
    fout.write(plaintext)
