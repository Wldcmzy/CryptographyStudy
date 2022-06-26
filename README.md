# codes （time order）

## ClassicalCryptography

#### I.Playerfair.py

#### II.Vigenere.py

#### III.Hill.py



## ModernCryptography

#### IV.Feistel.py

#### V.DES.py(ECB)

### VI.AES

#### 01.AES-ECB_Mode.py

电子密码本模式，密钥固定，相同明文对应的密文相同，对长报文可能不安全。

#### 02.AES-CBC_Mode.py

密码分组链接模式，明文分组于上一个密文分组亦或后再加密，首个明文分组与初始向量iv亦或。

传播错误会雪崩。

#### 03.AES-CTR_Mode.py

计数器模式，流密码，适合对实时性和速度要求高的场景。

可自定义复杂计数。

#### 04.AES-OFB_Mode.py

输出反馈模式，加密函数输出与寄存器值(开始为初始向量iv)亦或，寄存器值为其本身左移j位+加密函数输出高j位。（但是文档里好像没写指定j的接口）

#### 05.AES-CFB_Mode.py

密码反馈模式，加密函数输出与寄存器值(开始为初始向量iv)亦或，寄存器值为其本身左移j位+上一个密文分组低j位。（但是文档里好像没写指定j的接口）

