import numpy

# Palyfair密码
class Palyfair:
    def __init__(self, key = 'Hello World', paddingRepeat = 'x', paddingTail = 'z'):
        self.setKey(key)
        self.__paddingRepeat = paddingRepeat.lower()
        self.__paddingTail = paddingTail.lower()
    
    #构造字母矩阵,该方法一般不直接调用而是当密钥改变时,在方法setKey(self, key)中调用
    #字母矩阵构造方式为由左至右边,由上至下,优先填充一行
    def __makeMatrix(self):
        matrix = numpy.zeros([5, 5], dtype = str)
        lstKey = ''
        for each in self.__key.lower().replace('j', 'i'): 
            if each not in lstKey: lstKey += each
        lstKey = list(lstKey)
        lstOther = [chr(i) for i in range(97, 97 + 26) if chr(i) != 'j' and chr(i) not in lstKey]
        idxK, idxO = 0, 0
        for i in range(5):
            for j in range(5):
                if idxK < len(lstKey):
                    matrix[i][j] = lstKey[idxK]
                    idxK += 1
                else:
                    matrix[i][j] = lstOther[idxO]
                    idxO += 1
        return matrix

    #在字母矩阵中找到某一个字母的位置
    def __findPosition(self, ch):
        if ch == 'j': ch = 'i'
        re = (-1, -1)
        for i in range(5):
            if re != (-1, -1): break
            for j in range(5):
                if self.__matrix[i][j] == ch:
                    re = (i, j)
                    break
        return re

    #设置密钥
    def setKey(self, key):
        self.__key = ''.join(filter(str.isalpha, key)).lower()
        self.__matrix = self.__makeMatrix()

    #设置明文长度为奇数时的末尾补全字母
    def setPaddingTail(self, ch):
        self.__paddingTail = ch
    
    #设置出现两个相同字母时的填充字母
    def setPaddingRepeat(self, ch):
        self.__paddingRepeat = ch

    #加密, 返回密文
    #参数plaintext为要加密的明文
    def encrypt(self, plaintext):
        plaintext = ''.join(filter(str.isalpha, plaintext)).lower()
        if (len(plaintext) & 1) == 1: plaintext += self.__paddingTail
        ciphertext, idx = '', 0
        while idx < len(plaintext):
            a, b = plaintext[idx], plaintext[idx + 1]
            if a == b: ciphertext += a + self.__paddingRepeat + b
            else:
                pa, pb= self.__findPosition(a), self.__findPosition(b)
                if pa[0] == pb[0]:
                    ciphertext += self.__matrix[pa[0]][(pa[1] + 1) % 5]
                    ciphertext += self.__matrix[pb[0]][(pb[1] + 1) % 5]
                elif pa[1] == pb[1]:
                    ciphertext += self.__matrix[(pa[0] + 1) % 5][pa[1]]
                    ciphertext += self.__matrix[(pb[0] + 1) % 5][pb[1]]
                else:
                    ciphertext += self.__matrix[pa[0]][pb[1]]
                    ciphertext += self.__matrix[pb[0]][pa[1]]
            idx += 2
        return ciphertext

    #解密, 返回明文(列表), 计算过程中使用dfs
    #参数ciphertext为要解密的密文
    #参数mutiAnster：
    #   为True时, 使用dfs返回所有可能的密文, 返回列表, 时间复杂度为指数级, 重复字母多时慎用
    #   为False时, 不考虑加密时的重复字母, 在dfs中砍掉相应的的分支, 时间复杂度相当于线性, 若密文长度为奇数返回空列表[]
    def decrypt(self, ciphertext, mutiAnster = False):
        global plaintext, answer
        plaintext, answer = '', []
        ciphertext = ''.join(filter(str.isalpha, ciphertext)).lower()
       
        def __dfs(idx):
            global plaintext, answer
            if idx == len(ciphertext): 
                answer.append(plaintext)
                return
            elif idx + 1 >= len(ciphertext): return

            a , b = ciphertext[idx], ciphertext[idx + 1]
            if mutiAnster == True:
                if b == self.__paddingRepeat and idx + 2 < len(ciphertext) and ciphertext[idx + 2] == a:
                    plaintext += a + a
                    __dfs(idx + 3)
                    plaintext = plaintext[ : -2]

            pa, pb = self.__findPosition(a), self.__findPosition(b)
            if pa[0] == pb[0]:
                plaintext += self.__matrix[pa[0]][(pa[1] - 1) % 5]
                plaintext += self.__matrix[pb[0]][(pb[1] - 1) % 5]
            elif pa[1] == pb[1]:
                plaintext += self.__matrix[(pa[0] - 1) % 5][pa[1]]
                plaintext += self.__matrix[(pb[0] - 1) % 5][pb[1]]
            else:
                plaintext += self.__matrix[pa[0]][pb[1]]
                plaintext += self.__matrix[pb[0]][pa[1]]
                
            __dfs(idx + 2)
            plaintext = plaintext[ : -2]

        __dfs(0)
        return answer

def test():
    a = Palyfair()
    a.setKey('PlayFAiR iS a DIgRAM CIphEr')
    t = a.encrypt('playfair cipher abc')
    print(t)
    print(a.decrypt(t))

    t = a.encrypt('playfair cipher aaabaaa')
    print(t)
    print(a.decrypt(t, True))

if __name__ == '__main__':
    test()