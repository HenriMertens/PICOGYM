from pwn import *
for i in range(64):
    #Run binary with increasing length argument.
    p = process(['./checkpass', i *'A'])
    print('character length {}'.format(i) + p.recvline().decode())
