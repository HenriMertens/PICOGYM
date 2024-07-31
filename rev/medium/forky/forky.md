In this challenge we need to find out what the last integer was, that was passed in the doNothing function

1) Run file normally -> nothing happens.
2) Open file in ghidra and go to main function
   
```c
   undefined4 main(undefined1 param_1)

{
  int *piVar1;
  
  piVar1 = (int *)mmap((void *)0x0,4,3,0x21,-1,0);
  *piVar1 = 1000000000;
  fork();
  fork();
  fork();
  fork();
  *piVar1 = *piVar1 + 0x499602d2;
  doNothing(*piVar1);
  return 0;
}
```
- I didnt know what fork() did  so I read the manual: `fork()  creates  a  new process by duplicating the calling process.  The new process is referred to as the
       child process.  The calling process is referred to as the parent process.` Okay so it just duplicates the process?
- fork() gets called 4 times which means 2^4 (16) processes are being created, each one adds 0x499602d2 (1234567890) to 1000000000
- Final integer will be 1000000000 + (16*1234567890) = 20753086240
  
- The flag will be `picoCTF{20753086240}` obviously
  
  ![error](https://github.com/user-attachments/assets/854b4873-10f6-463a-8cc8-36c92a12beb3)

- Hmmm, I know my fork() logic is correct, so lets examine the other weird lien of code `piVar1 = (int *)mmap((void *)0x0,4,3,0x21,-1,0);`
- Manual : `void *mmap(void addr[.length], size_t length, int prot, int flags,
                  int fd, off_t offset);` and `mmap()  creates  a  new mapping in the virtual address space of the calling process.  The starting address
       for the new mapping is specified in addr.  The length argument specifies the length of the mapping  (which
       must be greater than 0).`
- We now know that the length of the mapping is 4 bytes, and 'int' is signed by defaulft in C. This means that instead of using all 32 bits to calculate the number, the first one will be used to indicate whether its a negative or positive number.
  There are thus 31 bits availible to create number or, number from (-2^31 -> 2^31) 2^31 is 2 147 486 348 which is less than 20 753 086 240. Some weird overflow is thus going to occur.
- Thankfully there is a handy python module called int32 that can help us, the exact solve script is in solve.py
- We now get `-721750240` ->picoCTF{-721750240}

  
