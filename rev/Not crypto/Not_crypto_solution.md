# Solution

## Step-by-Step Guide

### 1) Run the file normally

- Execute the file and observe its behavior.
- Note that the input is not immediately stopped, and the output varies based on the input length.

### 2) Open file in Ghidra and navigate to main

- Navigate to the main function in Ghidra.
- The main function is very large and complex.
- Two key parts stand out:

  a) There's a comparison:
     ```c
     iVar19 = memcmp(memcmp1, our_input, 0x40);
     if (iVar19 != 0) {
         puts("Nope, come back later");
     } else {
         puts("Yep, that's it!");
     }
     ```

  b) There's a read operation:
     ```c
     fread(our_input, 1, 0x40, _stdin);
     ```

- Rename the input variable (`our_input`) for easier reference.
- From this, we deduce that our input must be 64 bytes (0x40 in hexadecimal) long and is then compared to some value.

### 3) Solution

- **Using Angr:**
  - Create an Angr script to analyze the binary and find the input that leads to the output "Yep, that's it!".
  - See solve.py
    
  ![angr](https://github.com/HenriMertens/PICOGYM/assets/149707229/85555b77-a0dc-43ef-ba9f-70e19a05168a)

- **Using GDB:**
  - When looking at how other people solved this challenge I noticed that its also possible with gdb. Initially I disregarded using gdb since i assumed the flag and our input would be encrypted in the main function.
  - Here are the steps to solve using gdb
  - Set a breakpoint at memcmp (memcmp get called at offset = 0x13c1, and gdb has offset = 0x555555554000 -> adress of memcmp in gdb is 0x13c1+0x555555554000)
  - You can already see the flag in the gdb version im using but you can also examine the stack incase you dont see the flag yet with "x/50s $rsp"

    
  ![gdb](https://github.com/HenriMertens/PICOGYM/assets/149707229/f137ab5a-ba10-448d-8cfe-0695684a7860)

