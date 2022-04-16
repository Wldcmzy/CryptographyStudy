# 本仅对每一分组单独使用Feistel
# 未使用SP盒, 轮函数使用简单的异或运算
# 也就是说本算法没有错误传播,无雪崩效应

class Error_IllegalNumber_Of_Feistel(Exception):
    pass
class Feistel:
    
    ErrorString_groupLengthIsOddNumber = '分组长度为奇数'
    ErrorString_CipertextLengthNotMultipleOfGrouplenght = '密文长度不合法,不是groupLength的倍数'
    ModBitAdd1, ModNumber1, ModNumber2 = 257, 1e9 + 7, 998244353
    def __init__(self, seed = '777', groupLength = 64, loopTimes = 16):
        if (groupLength & 1) == 1: 
            raise Error_IllegalNumber_Of_Feistel(Feistel.ErrorString_groupLengthIsOddNumber)
        self.__seed = seed
        self.__groupLength = abs(groupLength)
        self.__loopTimes = abs(loopTimes)
        self.__keys = self.__generateKey()

    #瞎编了一种密钥构造的方法, 利用seed斐波那契不断延长密钥直到打到要求, 继续利用seed和斐波那契构造每一轮的密钥
    def __generateKey(self):
        a, b, temp_key = 1, 1, ''
        while len(temp_key) < (self.__groupLength >> 1):
            a, b, tmp = b, (a + b) % Feistel.ModNumber2, ''
            for each in self.__seed:
                tmp += chr((ord(each) * a + b) % Feistel.ModBitAdd1)
            temp_key += tmp
        temp_key = temp_key[- (self.__groupLength >> 1) : ]
        
        keys = []
        for _ in range(self.__loopTimes):
            tmp = ''
            for each in temp_key:
                a, b = b, (a + b) % Feistel.ModNumber2
                tmp += chr((ord(each) * a + b) % Feistel.ModBitAdd1)
            temp_key = tmp
            keys.append(temp_key)
        return keys

    def setSeed(self, seed):
        self.__seed = seed
        self.__keys = self.__generateKey()
    
    def setGroupLength(self, length):
        if (length & 1) == 1: 
            raise Error_IllegalNumber_Of_Feistel(Feistel.ErrorString_groupLengthIsOddNumber)
        self.__groupLength = abs(length)
        self.__keys = self.__generateKey()
    
    def setLoopTimes(self, times):
        self.__loopTimes = abs(times)
        self.__keys = self.__generateKey()

    def __work(self, text, workType):
        if workType not in ['P2C', 'C2P']: return
        lst, re = [], ''
        for i in range(0, len(text), self.__groupLength):
            lst.append(text[i : i + self.__groupLength])
        keys = self.__keys if workType == 'C2P' else self.__keys[ : : -1]
        def __F(txt):
            left, right, left1, right1 = txt[ : len(txt) >> 1], txt[len(txt) >> 1 : ], '', ''
            if workType == 'C2P': left, right = right, left
            for eachKey in keys:
                left1, right1 = right, ''
                for i in range(self.__groupLength >> 1):
                    right1 += chr(ord(left[i]) ^ ord(right[i]) ^ ord(eachKey[i]))
                left, right = left1, right1
            if workType == 'C2P': left, right = right, left
            return left + right
        for each in lst: re += __F(each)
        return re
        
    def encrypt(self, plaintext):
        if len(plaintext) % self.__groupLength != 0:
            cnt, tmp = self.__groupLength - (len(plaintext) % self.__groupLength), ''
            while len(tmp) < cnt: tmp += plaintext[ : cnt << 2 : 2]
            plaintext += tmp[ : cnt]
        return self.__work(plaintext, 'P2C')

    def decrypt(self, cipertext):
        if len(cipertext) % self.__groupLength != 0:
            raise Error_IllegalNumber_Of_Feistel(Feistel.ErrorString_groupLengthIsOddNumber)
        return self.__work(cipertext, 'C2P')

def test(plain):
    print('plain:',plain)
    print('\n\n')
    a = Feistel('1437')
    a.setGroupLength(32)
    t = a.encrypt(plain)
    print('密文:',t, end = '\n\n\n')
    print('解密:',a.decrypt(t))

if __name__ == '__main__':
    import io
    import sys
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding = 'utf-8') #改变标准输出的默认编码
    a1 = 'long long ago a bird ate a snake and say:\" LONG LONG AGO A SNAKE ATE A BIRD AND SAY \' WTF? I just wanna play Hollow Knight: Silk Song ! But ! I CAN\'T !! When can i play it !? I\'ll go mad!!!!!!!!!\' \"'
    a2 = 'abcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*()'
    a3 = 'abcdefghijkxmnopzrstuvwxyz1234567890!@#$%^&*()'
    test(a1)
    test(a2)
    test(a3)

