import numpy
class KeyError_Of_DES(Exception):
	pass
class Error_IllegalNumber_Of_DES(Exception):
    pass
class DES:
	ErrorString_KeyInputIsNot64bits = '请输入64比特的密钥'
	ErrorString_CipertextLengthNotMultipleOf64bit = '密文长度不合法,不是64bit的倍数'
	__Ebox = [32,  1,  2,  3,  4,  5
			,  4,  5,  6,  7,  8,  9
			,  8,  9, 10, 11, 12, 13
			, 12, 13, 14, 15, 16, 17
			, 16, 17, 18, 19, 20, 21
			, 20, 21, 22, 23, 24, 25
			, 24, 25, 26, 27, 28, 29
			, 28, 29, 30, 31, 32,  1]

	__Sbox = [
		numpy.array([  
			[14,4,13,1,2,15,11,8,3,10,6,12,5,9,0,7],  
			[0,15,7,4,14,2,13,1,10,6,12,11,9,5,3,8],  
			[4,1,14,8,13,6,2,11,15,12,9,7,3,10,5,0], 
			[15,12,8,2,4,9,1,7,5,11,3,14,10,0,6,13] 
		], dtype = numpy.int8)
		, numpy.array([  
			[15,1,8,14,6,11,3,4,9,7,2,13,12,0,5,10],  
			[3,13,4,7,15,2,8,14,12,0,1,10,6,9,11,5], 
			[0,14,7,11,10,4,13,1,5,8,12,6,9,3,2,15],  
			[13,8,10,1,3,15,4,2,11,6,7,12,0,5,14,9]  
		], dtype = numpy.int8)
		, numpy.array([  
			[10,0,9,14,6,3,15,5,1,13,12,7,11,4,2,8],  
			[13,7,0,9,3,4,6,10,2,8,5,14,12,11,15,1],  
			[13,6,4,9,8,15,3,0,11,1,2,12,5,10,14,7],  
			[1,10,13,0,6,9,8,7,4,15,14,3,11,5,2,12]  
		], dtype = numpy.int8)
		, numpy.array([  
			[7,13,14,3,0,6,9,10,1,2,8,5,11,12,4,15],  
			[13,8,11,5,6,15,0,3,4,7,2,12,1,10,14,9],  
			[10,6,9,0,12,11,7,13,15,1,3,14,5,2,8,4],  
			[3,15,0,6,10,1,13,8,9,4,5,11,12,7,2,14]  
		], dtype = numpy.int8)
		, numpy.array([  
			[2,12,4,1,7,10,11,6,8,5,3,15,13,0,14,9],  
			[14,11,2,12,4,7,13,1,5,0,15,10,3,9,8,6],  
			[4,2,1,11,10,13,7,8,15,9,12,5,6,3,0,14],  
			[11,8,12,7,1,14,2,13,6,15,0,9,10,4,5,3]  
		], dtype = numpy.int8)
		, numpy.array([  
			[12,1,10,15,9,2,6,8,0,13,3,4,14,7,5,11],  
			[10,15,4,2,7,12,9,5,6,1,13,14,0,11,3,8],  
			[9,14,15,5,2,8,12,3,7,0,4,10,1,13,11,6],  
			[4,3,2,12,9,5,15,10,11,14,1,7,6,0,8,13]  
		], dtype = numpy.int8)
		, numpy.array([  
			[4,11,2,14,15,0,8,13,3,12,9,7,5,10,6,1],  
			[13,0,11,7,4,9,1,10,14,3,5,12,2,15,8,6],  
			[1,4,11,13,12,3,7,14,10,15,6,8,0,5,9,2],  
			[6,11,13,8,1,4,10,7,9,5,0,15,14,2,3,12]  
		], dtype = numpy.int8)
		, numpy.array([   
			[13,2,8,4,6,15,11,1,10,9,3,14,5,0,12,7],  
			[1,15,13,8,10,3,7,4,12,5,6,11,0,14,9,2],  
			[7,11,4,1,9,12,14,2,0,6,10,13,15,3,5,8],  
			[2,1,14,7,4,10,8,13,15,12,9,0,3,5,6,11]  
		], dtype = numpy.int8)
	]

	__Pbox = [16,  7, 20, 21
			, 29, 12, 28, 17
			,  1, 15, 23, 26
			,  5, 18, 31, 10
			,  2,  8, 24, 14
			, 32, 27,  3,  9
			, 19, 13, 30,  6
			, 22, 11,  4, 25]
	
	__IP = [  58, 50, 42, 34, 26, 18, 10,  2
			, 60, 52, 44, 36, 28, 20, 12,  4
			, 62, 54, 46, 38, 30, 22, 14,  6
			, 64, 56, 48, 40, 32, 24, 16,  8
			, 57, 49, 41, 33, 25, 17,  9,  1
			, 59, 51, 43, 35, 27, 19, 11,  3
			, 61, 53, 45, 37, 29, 21, 13,  5
			, 63, 55, 47, 39, 31, 23, 15,  7]

	__IPrev = [ 40, 8, 48, 16, 56, 24, 64, 32
			  , 39, 7, 47, 15, 55, 23, 63, 31
			  , 38, 6, 46, 14, 54, 22, 62, 30
			  , 37, 5, 45, 13, 53, 21, 61, 29
			  , 36, 4, 44, 12, 52, 20, 60, 28
			  , 35, 3, 43, 11, 51, 19, 59, 27
			  , 34, 2, 42, 10, 50, 18, 58, 26
			  , 33, 1, 41,  9, 49, 17, 57, 25]
	
	__key64to56 = [   57, 49, 41, 33, 25, 17,  9
					,  1, 58, 50, 42, 34, 26, 18
					, 10,  2, 59, 51, 43, 35, 27
					, 19, 11,  3, 60, 52, 44, 36
					, 63, 55, 47, 39, 31, 23, 15
					,  7, 62, 54, 46, 38, 30, 22
					, 14,  6, 61, 53, 45, 37, 29
					, 21, 13,  5, 28, 20, 12,  4]

	__key56to48 = [   14, 17, 11, 24,  1,  5
					,  3, 28, 15,  6, 21, 10
					, 23, 19, 12,  4, 26,  8
					, 16,  7, 27, 20, 13,  2
					, 41, 52, 31, 37, 47, 55
					, 30, 40, 51, 45, 33, 48
					, 44, 49, 39, 56, 34, 53
					, 46, 42, 50, 36, 29, 32]

	__keyShift = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

	def __init__(self, key = 0xabcdef0123456789):
		self.__loopTimes = 16
		self.__keys = self.setKey(key)

	# 把数据origin通过映射表prjmap做变换
	def __Project(self, origin, prjmap, originLen):
		re, nowbit = 0, (1 << (len(prjmap) - 1))
		for each in prjmap:
			if ((origin >> (originLen - each)) & 1) == 1: re |= nowbit
			nowbit >>= 1
		return re

	# 生成轮密钥
	def __GenerateKey(self, key64):
		key56 = self.__Project(key64, self.__key64to56, 64)
		left, right, keys = key56 >> 28, key56 % (1 << 28), []

		def __leftshift(value, shift, maxbit):
			return ((value << shift) + (value >> (maxbit - shift))) % (1 << maxbit)
		
		for i in range(self.__loopTimes):
			left = __leftshift(left, self.__keyShift[i], 28)
			right = __leftshift(right, self.__keyShift[i], 28)
			key56 = (left << 28) + right
			key48 = self.__Project(key56, self.__key56to48, 56)
			keys.append(key48)
		
		return keys
		
	def setKey(self, key):
		if type(key) == str:
			if len(key) > 8:
				raise KeyError_Of_DES(DES.ErrorString_KeyInputIsNot64bits)
			keyint = 0
			for each in key:
				keyint = (keyint << 8) + ord(each)
			key = keyint
		if key >> 64 != 0:
			raise KeyError_Of_DES(DES.ErrorString_KeyInputIsNot64bits)
		return self.__GenerateKey(key)

	# 轮函数
	def __F(self, data32, key):

		# E盒扩展
		data48 = self.__Project(data32, self.__Ebox, 32)
		# 数据与key进行xor
		data48 ^= key

		# S盒压缩变换
		lst, ans, re = [], [], 0
		for i in range(8):
			lst.append(data48 & 0b111111)
			data48 >>= 6
		lst.reverse()

		def __SboxChange(data, index):
			col = (data >> 1) & 0b1111
			row = (data & 1) + ((data >> 4) & 0b10)
			return self.__Sbox[index][row][col]

		for i, each in enumerate(lst):
			ans.append(__SboxChange(each, i))
		for each in ans:
			re = (re << 4) + each

		#P盒换位
		re = self.__Project(re, self.__Pbox, 32)

		return re

	# 初始置换
	def __IPfunction(self, data, rev = False):
		if rev == False: 
			data = self.__Project(data, self.__IP, 64)
		else: 
			data = self.__Project(data, self.__IPrev, 64)
		return data
		
	def __work(self, data, workType = 'C2P'):
		if workType not in ['C2P', 'P2C']: return
		# 初始置换
		data = self.__IPfunction(data, False)

		#加密主体, 类似Feistel
		left, right = data >> 32, data % (1 << 32)
		keys = self.__keys.copy()
		if workType == 'P2C': keys.reverse()

		######################################################
		# 打开下方2行以及下面for循环的一行debug注释,以显示中间过程
		# 	注意16轮循环完后会有一次左右互换操作, 所以
		# 	debug输出的是互换前的数据, 故第16轮的debug数据与结果相反
		#######################################################
		#debug_ = True
		#if debug_ == True: print(0, hex(left), hex(right))
		for i in range(self.__loopTimes):
			left1 = right
			right1 = left ^ self.__F(right, keys[i])
			left, right = left1, right1
			#if debug_ == True: print(i + 1, hex(left), hex(right))
		left, right = right, left
		
		# 拼接与逆初始置换
		return self.__IPfunction((left << 32) + right, True)

	def __Str2Num(self, data):
		re = 0
		for each in data:
			re = (re << 8) + ord(each)
		return re

	def __Num2Str(self, data, charNum = 8):
		re = ''
		for _ in range(charNum):
			re = chr(data & 0b11111111) + re
			data >>= 8
		return re 
			

	# 加密 
	# plaintext 类型为字符串
	def encrypt(self, plaintext):
		# 填充明文使得明文长度为64bit的倍数
		if len(plaintext) % 8 != 0:
			cnt, tmp = 8 - (len(plaintext) % 8), ''
			while len(tmp) < cnt: tmp += plaintext[ : cnt << 1: 2]
			tmp = tmp[ : cnt]
			plaintext += tmp
		lst, cipertext = [plaintext[i : i + 8] for i in range(0, len(plaintext), 8)], ''
		for each in lst:
			data = self.__Str2Num(each)
			data = self.__work(data, 'C2P')
			cipertext += self.__Num2Str(data)

		return cipertext
			
	def decrypt(self,cipertext):
		if len(cipertext) % 8 != 0:
			raise Error_IllegalNumber_Of_DES(DES.ErrorString_CipertextLengthNotMultipleOf64bit)
		
		lst, plaintext = [cipertext[i : i + 8] for i in range(0, len(cipertext), 8)], ''
		for each in lst:
			data = self.__Str2Num(each)
			data = self.__work(data, 'P2C')
			plaintext += self.__Num2Str(data)
		
		return plaintext


def test():
	des = DES(0xaabb09182736ccdd)
	origintext = (des._DES__Num2Str(0x123456abcd132536))
	print('origintext :', origintext)
	cipertext = des.encrypt(origintext)
	print('cipertext :', cipertext)
	plaintext = des.decrypt(cipertext)	
	print('plaintext :', plaintext)
	print()
	print('本测试用例为《应用密码学(第四版)》(胡向东, 魏琴芳, 胡蓉 编著) P102例子')
	print('想看详细中间过程请打开__work方法中注释掉的debug语句, 本语句下方注释的三条语句')
	print('中间过程包括: 加密前和16轮加密中的left right, 以及16轮加密的密钥')
	#print('密钥:')
	#for each in des._DES__keys:
	#	print(hex(each))
	print()
	print()

def test2():
	a = DES()
	a.setKey(0xabcdef1234567890)
	ori = 'DE135AD1ABCDS'
	print('origintext: ', ori)
	t = a.encrypt(ori)
	print('C :', t)
	tt = a.decrypt(t)
	print('P :', tt)

	# error, because of length(key) > 64bit 
	a.setKey('asdfqwerzx')


if __name__ == '__main__':
	import sys
	import io 
	sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding = 'utf-8') #改变标准输出的默认编码
	test()
	test2()
