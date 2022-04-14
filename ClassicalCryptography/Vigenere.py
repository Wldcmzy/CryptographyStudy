class Vigenere:
    def __init__(self, key = 'hello World'):
        super().__init__()
        self.setKey(key)

    #加密
    def setKey(self, key):
        self.__key = ''.join(filter(str.isalpha, key)).lower()
        self.__shift = [ord(i) - 97 for i in self.__key]

    def encrypt(self, plaintext):
        plaintext = plaintext.lower()
        ciphertext, idx = '', 0
        for each in plaintext:
            ciphertext += chr((ord(each) - 97 + self.__shift[idx]) % 26 + 97)
            idx = (idx + 1) % len(self.__shift)
        return ciphertext
    
    def decrypt(self, cipertext):
        cipertext = cipertext.lower()
        plaintext, idx = '', 0
        for each in cipertext:
            plaintext += chr((ord(each) - 97 - self.__shift[idx]) % 26 + 97)
            idx = (idx + 1) % len(self.__shift)
        return plaintext


def test():
    a = Vigenere()
    a.setKey('ABCDEF AB CDEFA BCD EFABCDEFABCD')
    t = a.encrypt('CRYPTO IS SHORT FOR CRYPTOGRAPHY')
    print(t)
    print(a.decrypt(t))

if __name__ == '__main__':
    test()