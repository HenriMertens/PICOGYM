
from string import printable

data = [ 0x1f, 0x19, 0x0c, 0x1c, 0x30, 0x21, 0x2b, 0x14, 0x00, 0x06, 0x1d, 0x1a, 0x1b, 0x0a, 0x41, 0x16, 0x00, 0x01, 0x5d, 0x01, 0x05, 0x0a, 0x5e, 0x09, 0x19, 0x1c, 0x07, 0x09, 0x1c, 0x0d, 0x00 ]


flag = ""
pre = "picoCTF{"



for i in range(len(pre)):
    for c in printable:

        if(data[i]^ord(c) == ord(pre[i])):
            flag += c
            print(flag)


def unscramble(password):
    testpass = ""
    for i in range(len(data)):
        testpass += chr(data[i]^ord(password[i]))
        print(testpass)

unscramble("opossumopossumopossumopossumopossumopossumopossumopossum")




