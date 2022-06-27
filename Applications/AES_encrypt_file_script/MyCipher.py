from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from os import system

ONE_GB_TIME = (1 << 5)
READ_SIZE = (1 << 25)
MULTI = (READ_SIZE >> 20)

# ONE_GB_TIME = (1 << 10)
# READ_SIZE = (1 << 20)
# MULTI = (READ_SIZE >> 20)

def encrypt_AES_ECB(key : str, origin_file : str, target_file : str) -> None:
    '''
    使用密钥key, 以ECB模式使用AES加密origin_file文件, 输出为target_file
    key : 密钥
    origin_file : 源文件路径
    target_file : 输出文件路径
    '''
    cipher = AES.new(key, AES.MODE_ECB)
    with open(origin_file, 'rb') as fin:
        fout, MBcounter = open(target_file, 'wb'), 0
        while True:
            MBcounter += 1

            block = fin.read(READ_SIZE - 1)
            if not len(block): break
            block = pad(block, AES.block_size, style='pkcs7')

            fout.write(cipher.encrypt(block))

            system('cls')
            GBs = (MBcounter * MULTI) >> 10
            MBs = (MBcounter * MULTI) % (1 << 10)
            print(f'{GBs}GB {MBs}MB datas encrypted.')

            if MBcounter % ONE_GB_TIME == 0:
                fout.close()
                fout = open(target_file, 'ab')

def decrypt_AES_ECB(key : str, cipher_file : str, target_file : str) -> None:
    '''
    使用密钥key, 以ECB模式使用AES解密cipher_file文件, 输出为target_file
    key : 密钥
    origin_file : 加密文件路径
    target_file : 输出文件路径
    '''
    cipher = AES.new(key, AES.MODE_ECB)
    with open(cipher_file, 'rb') as fin:
        fout, MBcounter = open(target_file, 'wb'), 0
        while True:
            MBcounter += 1

            block = fin.read(READ_SIZE)
            if not len(block): break
            block = cipher.decrypt(block)

            fout.write(unpad(block, AES.block_size, style='pkcs7'))

            system('cls')
            GBs = (MBcounter * MULTI) >> 10
            MBs = (MBcounter * MULTI) % (1 << 10)
            print(f'{GBs}GB {MBs}MB datas decrypted.')

            if MBcounter % ONE_GB_TIME == 0:
                fout.close()
                fout = open(target_file, 'ab')



