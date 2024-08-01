import sys

import string

from pwn import *

flag_chars = string.digits + string.ascii_letters + '_'

context.log_level = 'error'


guessed = []

def countinstructions(flag):
    valgrind_stderr = process(['valgrind', '--tool=cachegrind', './checkpass', 'picoCTF{' + flag + '}'])
    valgrind_stderr.recvuntil("I   refs:")
    answer = int(valgrind_stderr.recvline().decode().replace(',', ''))
    print(answer)
    valgrind_stderr.close()
    return answer


def replace_char(s, i, new_char):
    if i < 0 or i >= len(s):
        raise IndexError("Index out of range")
    return s[:i] + new_char + s[i + 1:]

def already_guessed(i):
    if guessed.__contains__(i):
        return True
    else:
        return False

password_guess = '~' * 32
i = 11
while any(x == '~' for x in password_guess):

    best_count = countinstructions(password_guess)
    print("guess so far is: " + password_guess)
    print('guessed so far are: ')
    print(guessed)
    print("i is {}".format(i))
    if not already_guessed(i):
        for c in flag_chars:
            new_guess = replace_char(password_guess, i, c)
            print('new guess = ' + new_guess)
            count = countinstructions(new_guess)
            if count > best_count:
               print("need a:" + c)
               password_guess = replace_char(password_guess, i, c)
               guessed.append(i)
        if(i == 31):
            i = -1
        i+=1
    if already_guessed(i):
        if (i == 31):
            i = -1
        i+=1
