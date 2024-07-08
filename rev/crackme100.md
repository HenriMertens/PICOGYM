CRACKME100 SOLUTION

1) Open executable in ghidra

2) Navigate to the main function

3) Notice initiliased local variables, try to convert from hex to ascii but gives mumbo jumbo

3) Notice that our input is saved on locala8 and has format %50s (50 characters) -> rename the variable for easier future reference

4) See a lot math that modifies our input (aint reading all that)

5) Notice "memcmp" function that compares our_input (which has been modified) against initialised variable (same one from above)

Intermediate conclusion:
Encrypted password is initialised in the main function
Our input gets encrypted and compared agains this encrypted password

if match -> print sample flag

Solution:

I solved this using angr, see solve script






