import sys

import string

from pwn import *

#initialize all characters we want to check
flag_chars = string.digits + string.ascii_letters + '_'

context.log_level = 'error'

#Use valgrind to count the amount of instructions instrcutions that were parsed by the programm
def countinstructions(flag):
    valgrind_stderr = process(['valgrind', '--tool=cachegrind', './checkpass', 'picoCTF{' + flag + '}'])
    valgrind_stderr.recvuntil("I   refs:")
    answer = int(valgrind_stderr.recvline().decode().replace(',', ''))
    print(answer)
    valgrind_stderr.close()
    return answer

#Quick way to change "~" to characters when a correct character has been found
def replace_char(s, i, new_char):
    if i < 0 or i >= len(s):
        raise IndexError("Index out of range")
    return s[:i] + new_char + s[i + 1:]

"initial guess"
password_guess = '~' * 32

# I did a manual for loop heer for some reason lol
i = 1

while any(x == '~' for x in password_guess):
    # As long as there any "~" left, count the amount of instructions from the previous best guess
    best_count = countinstructions(password_guess)
    print("guess so far is: " + password_guess)

    for c in flag_chars:
        #count the amount of instructions if we were to chenge a character
        new_guess = replace_char(password_guess, i, c)
        print('new guess = ' + new_guess)
        count = countinstructions(new_guess)
        print(i)
        
        # if we have more instructions when we change a character, this becomes our new best guess
        if count > best_count:
            print("need a:" + c)
            password_guess = replace_char(password_guess, i, c)
    #if you reach the last character of the current best password guess, start from index 0 again        
    if (i == 31):
        i = -1
    # go to the next index (character)
    i+=1
