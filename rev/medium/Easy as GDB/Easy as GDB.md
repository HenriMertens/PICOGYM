1) Run file normally
  - It asks us for a flag, when a wrong input is given the program closes.
    
  ![brutestart](https://github.com/HenriMertens/PICOGYM/assets/149707229/1d9948ed-d73e-4a9a-8b2d-f7d31305297a)

2) Spin up ghidra and analyze the "main" function.
   - Since there isn't a literal "main" function we can try find it using the "entry" function.
   
   ![entryfunc](https://github.com/HenriMertens/PICOGYM/assets/149707229/96b85e3f-09a4-4948-a527-d30760e87eac)

  - The first argument of the entry function is the "main" function (most of the time)
```c
   undefined4 FUN_000109af(void)

{
  char *__s;
  size_t sVar1;
  undefined4 uVar2;
  int iVar3;
  
  __s = (char *)calloc(0x200,1);
  printf("input the flag: ");
  fgets(__s,0x200,_stdin);
  sVar1 = strnlen(&DAT_00012008,0x200);
  uVar2 = FUN_0001082b(__s,sVar1);
  FUN_000107c2(uVar2,sVar1,1);
  iVar3 = FUN_000108c4(uVar2,sVar1);
  if (iVar3 == 1) {
    puts("Correct!");
  }
  else {
    puts("Incorrect.");
  }
  return 0;
}
```
  - We see our input gets saved via the `fgets` function
    ```c
    fgets(__s, 0x200, _stdin);
    ```
 - This line reads up to 0x200 bytes and saves it in __s
 - We know that our input (flag) will be a max of 0x200 (256) bytes (characters)
 - Further we see it prints either "correct" or "incorrect" based on the input.
   This feels like a prime example to use angr on
   
3) Solution:
   - I solved this challenge via angr again with the solve.py script.
   - The code is explained in the script itself
   - Runtime was around 5 mins and it is worth noting that when running the code it will look like its stuck around here:
     
     ![stuck](https://github.com/HenriMertens/PICOGYM/assets/149707229/0230a418-d969-49e5-be8f-db8de1930245)

     After a few minutes however, the programm will provide the flag
     
      ![flagbrute](https://github.com/HenriMertens/PICOGYM/assets/149707229/922a960e-14aa-4d4a-b90a-69af752c2811)
