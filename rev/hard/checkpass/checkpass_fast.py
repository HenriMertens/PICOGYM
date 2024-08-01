#Same as checkpass_slow.py, but doesnt repeat alread guessed characters
#For example 30/32 characters guessed -> slow still replaces all 32 chars whereas fast only checks remaining 2 chars
import sys

import string

from pwn import *

flag_chars = string.digits + string.ascii_letters + '_'

context.log_level = 'error'

#save the indexes of all correctly guessed chars
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

#check if the current index is already correctly guessed
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

    # If the index is not already correctly guessed, try to guess it
    if not already_guessed(i):
        for c in flag_chars:
            new_guess = replace_char(password_guess, i, c)
            print('new guess = ' + new_guess)
            count = countinstructions(new_guess)
            if count > best_count:
               print("need a:" + c)
               password_guess = replace_char(password_guess, i, c)
                # if you guess correctly, append it to the guessed array
               guessed.append(i)
        if(i == 31):
            i = -1
        i+=1
    #if it is correctly guessed already just go to next index
    if already_guessed(i):
        if (i == 31):
            i = -1
        i+=1
