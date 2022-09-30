from MyCipher import decrypt_AES_ECB, encrypt_AES_ECB
from os import system
from time import time
from typing import Union

def parse_time(value : Union[int, float]) -> str:
    '''把时间从秒转化为hh:mm:ss的形式'''
    
    value = int(value)
    hh = value // (60 ** 2)
    value %= (60 ** 2)
    mm = value // 60
    ss = value % 60

    return f'{hh}:{mm}:{ss}'

def print_menu() -> None:
    '''打印菜单的函数'''
    data = '''
=========================
=> 0. exit
=========================
=> 1. encrypt(AES ECB)
=========================
=> 2. decrypt(AES ECB)
=========================
'''
    print(data)

if __name__ == '__main__':

    op = 0

    while True:
        system('cls')
        print_menu()

        try:
            op = int(input('input your operation:'))
        except Exception as e:
            print(type(e), str(e))
            system('pause')
            continue

        if op == 0:
            break

        elif op == 1:
            start_time = time()
            filename = input('input origin file name:')
            targetname = input('input target file name:')
            key = input('input key:').encode('utf-8')
            encrypt_AES_ECB(key, filename, targetname)
            print(f'OK, cost time: {parse_time(time() - start_time)}')
            system('pause')

        elif op == 2:
            start_time = time()
            filename = input('input cipher file name:')
            targetname = input('input target file name:')
            key = input('input key:').encode('utf-8')
            decrypt_AES_ECB(key, filename, targetname)
            print(f'OK, cost time: {parse_time(time() - start_time)}')
            system('pause')