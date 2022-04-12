import numpy
class Error_NotASquareMatrix_Of_Hill(Exception):
    pass
class Error_MatrixUnreversible_Of_Hill(Exception):
    pass
class Error_IllegalCipertext(Exception):
    pass
class Hill:
    ErrorString_MatrixUnreversible = '该密钥矩阵不可逆'
    ErrorString_NotASquareMatrix = '该密钥矩阵不是方阵'
    ErrorString_IllegalCipertext_NotMultiple = '密文长度不是矩阵大小的倍数,无法解密'
    def __init__(self, key = numpy.array([[1, 0, 0]
                                        , [0, 1, 0]
                                        , [0, 0, 1]], dtype = numpy.int32)):
        self.setKey(key)

    def setKey(self, key):
        if key.shape[0] != key.shape[1]:
            raise Error_NotASquareMatrix_Of_Hill(Hill.ErrorString_NotASquareMatrix)
        if numpy.linalg.det(key) == 0:
            raise Error_MatrixUnreversible_Of_Hill(Hill.ErrorString_MatrixUnreversible)
        self.__key = key
        self.__keyInv = numpy.linalg.inv(self.__key) % 26
        self.__matrixSize = key.shape[0]
        print(self.__keyInv)
        print(numpy.dot(self.__keyInv , self.__key) % 26)

    def encrypt(self, plaintext):
        plaintext = ''.join(filter(str.isalpha, plaintext)).lower()
        if len(plaintext) % self.__matrixSize != 0:
            plaintext += 'x' * (self.__matrixSize - (len(plaintext) % self.__matrixSize))
        cipertext, idx = '', 0
        while idx < len(plaintext):
            array = numpy.array([ord(each) - 97 for each in list(plaintext[idx : idx + self.__matrixSize])], dtype = numpy.int32)
            array = numpy.dot(array, self.__key) % 26
            print(array)
            for each in array.tolist():
                cipertext += chr(each + 97)
            idx += self.__matrixSize
        return cipertext


    def decrypt(self, cipertext):
        cipertext = ''.join(filter(str.isalpha, cipertext)).lower()
        if len(cipertext) % self.__matrixSize != 0:
            raise Error_IllegalCipertext(Hill.ErrorString_IllegalCipertext_NotMultiple)
        plaintext, idx = '', 0
        while idx < len(cipertext):
            array = numpy.array([ord(each) - 97 for each in list(cipertext[idx : idx + self.__matrixSize])], dtype = numpy.int32)
            array = numpy.dot(array, self.__keyInv) % 26
            print(array)
            for each in array.tolist():
                plaintext += chr(round(each) % 26 + 97)
            idx += self.__matrixSize
        return plaintext