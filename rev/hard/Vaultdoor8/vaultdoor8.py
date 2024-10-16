
from string import printable

def switchBits(n, pos1, pos2):

    if (n >> pos1) & 1 != (n >> pos2) & 1:

        n ^= (1 << pos1) | (1 << pos2)
    return n


def encrypt(c):
    c = switchBits(c, 1, 2)
    c = switchBits(c, 0, 3)
    c = switchBits(c, 5, 6)
    c = switchBits(c, 4, 7)
    c = switchBits(c, 0, 1)
    c = switchBits(c, 3, 4)
    c = switchBits(c, 2, 5)
    c = switchBits(c, 6, 7)
    return c

character_expected =[
0xF4, 0xC0, 0x97, 0xF0, 0x77, 0x97, 0xC0, 0xE4, 0xF0, 0x77, 0xA4, 0xD0, 0xC5, 0x77, 0xF4, 0x86, 0xD0, 0xA5, 0x45, 0x96, 0x27, 0xB5, 0x77, 0xD2, 0xD0, 0xB4, 0xE1, 0xC1, 0xE0, 0xD0, 0xD0, 0xE0
]

password = ""
for i in range(character_expected.__len__()):
    for c in printable:
        enc = encrypt(ord(c))
        if(enc == character_expected[i]):
            password += c

print(password)