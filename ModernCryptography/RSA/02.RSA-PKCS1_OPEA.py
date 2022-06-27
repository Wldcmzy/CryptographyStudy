from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

with open('RSA-Private_key1_protected.pem', 'rb') as fin:
    private_key = RSA.import_key(
        fin.read(),
        passphrase = 'Galama!',
    )
with open('RSA-Public_key1.pem', 'rb') as fin:
    public_key = RSA.import_key(fin.read())
with open('test.txt', 'rb') as fin:
    origintext = fin.read()


cipher_rsa = PKCS1_OAEP.new(public_key)
ciphertext = cipher_rsa.encrypt(origintext)

cipher_rsa2 = PKCS1_OAEP.new(private_key)
plaintext = cipher_rsa2.decrypt(ciphertext)

with open('PKCS1_OPEA_encrypted.txt', 'wb') as fout:
    fout.write(ciphertext)
with open('PKCS1_OPEA_decrypted.txt', 'wb') as fout:
    fout.write(plaintext)


name = b'MyName'
hashdata = SHA256.new(name)
signature = pkcs1_15.new(private_key).sign(hashdata)
signature_fake = signature[ : -1] + chr((signature[-1] + 1) % 255).encode('utf-8')

sigScheme = pkcs1_15.new(public_key)

try:
    sigScheme.verify(hashdata, signature)
    print('1认证成功')
except (ValueError, TypeError):
    print('1认证失败')

try:
    sigScheme.verify(hashdata, signature_fake)
    print('2认证成功')
except (ValueError, TypeError):
    print('2认证失败')

with open('PKCS1_v1.5-Signature.txt', 'wb') as fout:
    fout.write(signature)