from Crypto.PublicKey import RSA

key = RSA.generate(2048)
private_key = key.export_key()
private_key_protected = key.export_key(
    passphrase='Galama!',
    pkcs = 8, # 默认值是1
    protection="scryptAndAES256-CBC", # pkcs8只有SHA1And + 一种DES和三种(128 192 256)AES, pkcs1只有DES 
)
private_key_import = RSA.import_key(
    private_key_protected,
    passphrase = 'Galama!',
).export_key()
public_key = key.publickey().export_key()


with open("RSA-Private_key1.pem", "wb") as fout:
    fout.write(private_key)

with open("RSA-Private_key1_protected.pem", "wb") as fout:
    fout.write(private_key_protected)

with open("RSA-Private_key1_import.pem", "wb") as fout:
    fout.write(private_key_import)

with open("RSA-Public_key1.pem", "wb") as fout:
    fout.write(public_key)
