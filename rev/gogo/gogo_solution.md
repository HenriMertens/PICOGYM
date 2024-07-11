Solution:

1) run file normally and seet it just asks for a password
   
  ![start](https://github.com/HenriMertens/PICOGYM/assets/149707229/5112d921-f963-4627-a717-ab03270d49c9)

2) Open file in ghidra
   - Examine the main.main function:
     
 ```c
     void main.main(void)
{
  int iVar1;
  int *in_GS_OFFSET;
  undefined4 *in_stack_ffffffac;
  undefined4 *puVar2;
  char cVar3;
  undefined *local_30;
  undefined **local_2c;
  undefined *local_28;
  undefined **local_24;
  undefined *local_20;
  undefined **local_1c;
  undefined *local_18 [2];
  undefined *local_10;
  undefined **local_c;
  undefined *local_8;
  undefined4 *local_4;
  undefined **ppuVar4;
  
  while (&stack0x00000000 <= *(undefined **)(*(int *)(*in_GS_OFFSET + -4) + 8)) {
    local_4 = (undefined4 *)0x80d4a7b;
    runtime.morestack_noctxt();
  }
  runtime.newobject(&DAT_080e8860);
  fmt.Printf(&DAT_080fea50,0x10,0,0,0);
  local_18[0] = &DAT_080e1300;
  ppuVar4 = local_18;
  fmt.Scanf(&DAT_080fd1b6,3,ppuVar4,1,1);
  cVar3 = (char)ppuVar4;
  main.checkPassword(*in_stack_ffffffac,in_stack_ffffffac[1]);
  if (cVar3 == '\0') {
    local_10 = &DAT_080e8860;
    local_c = &main.statictmp_3;
    fmt.Println(&local_10,1,1);
  }
  else {
    local_20 = &DAT_080e8860;
    local_1c = &main.statictmp_0;
    fmt.Println(&local_20,1,1);
    local_28 = &DAT_080e8860;
    local_24 = &main.statictmp_1;
    fmt.Println(&local_28,1,1);
    local_30 = &DAT_080e8860;
    local_2c = &main.statictmp_2;
    puVar2 = (undefined4 *)0x1;
    fmt.Println(&local_30,1,1);
    runtime.newobject(&DAT_080e8860);
    local_8 = &DAT_080e1300;
    local_4 = puVar2;
    fmt.Scanf(&DAT_080fd1b6,3,&local_8,1,1);
    main.ambush(*puVar2,puVar2[1]);
    iVar1 = runtime.deferproc(0,&PTR_main.get_flag_081046a0);
    if (iVar1 != 0) {
      runtime.deferreturn();
      return;
    }
  }
  runtime.deferreturn();
  return;
}
 ```
  - The code doesnt look like its 100% C and its also very janky
  - We can try to figure out how the file works now :
    
    1) It prints a line ("Enter password:")
    2) It scans our input and presumably puts it in ppuvar4
    3) A checkpassword function is called, we can assume that atleast one of the params will be our scanned input.
    4) We get to an if-else-block, in the else block we see
       
       ```c
       iVar1 = runtime.deferproc(0,&PTR_main.get_flag_081046a0);
       ```
       We can assume that cvar3 will store the result of the checkpassword function and the else-block will be called if the passsword is correct.
       The else block also scans some new input and calls the main.ambush function, this is a problem for later

    -Examine the checkpassword function:
 ```c
          
void main.checkPassword(int param_1,uint param_2)

{
  uint uVar1;
  int iVar2;
  int *in_GS_OFFSET;
  undefined4 local_40;
  undefined4 local_3c;
  undefined4 local_38;
  undefined4 local_34;
  undefined4 local_30;
  undefined4 local_2c;
  undefined4 local_28;
  undefined4 local_24;
  byte local_20 [28];
  undefined4 uStack_4;
  
  while (&stack0x00000000 <= *(undefined **)(*(int *)(*in_GS_OFFSET + -4) + 8)) {
    uStack_4 = 0x80d4b72;
    runtime.morestack_noctxt();
  }
  if ((int)param_2 < 0x20) {
    os.Exit(0);
  }
  FUN_08090b18();
  local_40 = 0x38313638;
  local_3c = 0x31663633;
  local_38 = 0x64336533;
  local_34 = 0x64373236;
  local_30 = 0x37336166;
  local_2c = 0x62646235;
  local_28 = 0x39383338;
  local_24 = 0x65343132;
  FUN_08090fe0();
  uVar1 = 0;
  iVar2 = 0;
  while( true ) {
    if (0x1f < (int)uVar1) {
      if (iVar2 == 0x20) {
        return;
      }
      return;
    }
    if ((param_2 <= uVar1) || (0x1f < uVar1)) break;
    if ((*(byte *)(param_1 + uVar1) ^ *(byte *)((int)&local_40 + uVar1)) == local_20[uVar1]) {
      iVar2 = iVar2 + 1;
    }
    uVar1 = uVar1 + 1;
  }
  runtime.panicindex();
  do {
    invalidInstructionException();
  } while( true );
}
 ```
-We see that some random values are initialised in local40.
- Each byte (character) of Local40 is XORD with each byte of param2 (presumably our input) and compared against local20.
  
Soltution:
-I first tried with angr, however I had some difficulties:
1) When running basic angrscript with just sm.run() angr was making a ton of active states

![veritesting](https://github.com/HenriMertens/PICOGYM/assets/149707229/ab3ae3da-7a45-49c8-b571-bfc8bd1f6800)

2) Easy fix lol, just add "veritesting = True" -> problem fixed but, angr still seems to get stuck on some init functions :(
   I let angr run for around 15 mins but it couldnt get past this

   ![init](https://github.com/HenriMertens/PICOGYM/assets/149707229/9223bc46-c4a0-4bd6-8385-76b0e2388fc7)
   
4) Easy fix lol, just use an already initialised state
   - Open up gdb
   - Set breakpoint at main
   - Run programm
   - Hit breakpoint
   - Dump the "state" with "generate-core-file"
  
     ![gdb](https://github.com/HenriMertens/PICOGYM/assets/149707229/2d021459-a3c9-4e70-8054-cd5c507713d9)

   - use this file in angr script instead of "enter_password"
   - Get error
     ![angrgdb](https://github.com/HenriMertens/PICOGYM/assets/149707229/85515fc3-eb83-4284-88d0-ec65a7a8d217)

   - Cry
5) Give up on angr and just do it with gdb

6) Set breakpoint at 0x80d4b28, at this adress we can see all the variables (our input (= param1), what we xor with (= local40) and what this xor must equal (=local20))
   ![xor](https://github.com/HenriMertens/PICOGYM/assets/149707229/e15f9c15-3da9-4f82-b3be-ca7bd384bce1)

   Note that in order to get here, param2 must equal 0x20 (=32). We can assume that this is the length of our input since param1 is our input itself.
   
7) From the assembly above and when examining the three variables in ghidra, we can see that:
   1) Param1 (our_input) is stored in "[ECX + EAX*0x1]", which is just ECX
   2) Local40 is stored in "[ESP + EAX*0x1 + 0x4]" which is just ESP + 0x4
   3) Local 20 is stored in "[ESP + EAX*0x1 + 0x24]" which is just $ESP +0x24

   We inspect these variables with following commands:
   ![regs](https://github.com/HenriMertens/PICOGYM/assets/149707229/6a1e717c-e5a6-4234-bee1-51c15c7ed141)

   Keep in mind that you will only hit the breakpoint when giving 32 characters as input!

8) Since our_input^local40 shoudl equal local20, we can deduce that local40^local20 sould equal our input!
   We can use cyberchef to easiliy compute the XOR:
   
   ![noswap](https://github.com/HenriMertens/PICOGYM/assets/149707229/d2523baf-b132-4d0a-b44e-346e0c93e5f0)

   hmmm, this almost looks correct. Lets tryswapping endianness:

   ![swap](https://github.com/HenriMertens/PICOGYM/assets/149707229/8400ad2c-5f79-4b19-ad6f-ea3b77e5c3f2)

   Nice! This looks like it will be the password.

9) Run the programm again and see whats next:
    
    ![pass](https://github.com/HenriMertens/PICOGYM/assets/149707229/5c83cb3a-ce2b-45bb-b18a-8093e7161bfd)

   The programm asks us for the unhashed key, remeber our input was xord with `3836313833366631336533643632376466613337356264623833383932313465`.
   Perhaps this is just the key it is asking for?

   Looking at ghidra we can see that after our input gets scanned the function main.ambush is called:
 ```c
   void main.ambush(undefined4 param_1,undefined4 param_2)

{
  char cVar1;
  uint uVar2;
  int *in_GS_OFFSET;
  int local_88;
  uint local_84;
  uint local_80;
  undefined local_70 [16];
  undefined4 local_60;
  undefined4 local_5c;
  undefined4 local_58;
  undefined4 local_54;
  undefined4 local_50;
  undefined4 local_4c;
  undefined4 local_48;
  undefined4 local_44;
  undefined local_40 [32];
  undefined local_20 [12];
  undefined local_14 [16];
  undefined4 uStack_4;
  
  while (local_14 <= *(undefined **)(*(int *)(*in_GS_OFFSET + -4) + 8)) {
    uStack_4 = 0x80d4e4b;
    runtime.morestack_noctxt();
  }
  runtime.stringtoslicebyte(local_40,param_1,param_2);
  crypto/md5.Sum(local_88,local_84,local_80);
  FUN_08091008();
  FUN_08090b18();
  local_60 = 0x38313638;
  local_5c = 0x31663633;
  local_58 = 0x64336533;
  local_54 = 0x64373236;
  local_50 = 0x37336166;
  local_4c = 0x62646235;
  local_48 = 0x39383338;
  local_44 = 0x65343132;
  uVar2 = 0;
  while( true ) {
    if (0xf < (int)uVar2) {
      return;
    }
    encoding/hex.EncodeToString(local_70,0x10,0x10);
    if (local_84 <= uVar2) break;
    cVar1 = *(char *)(uVar2 + local_88);
    local_88 = 0x20;
    runtime.slicebytetostring(local_20,&local_60,0x20);
    if (local_80 <= uVar2) break;
    if (cVar1 != *(char *)(local_84 + uVar2)) {
      os.Exit(0);
    }
    uVar2 = uVar2 + 1;
  }
  runtime.panicindex();
  do {
    invalidInstructionException();
  } while( true );
}
```
We notice:
`
  crypto/md5.Sum(local_88,local_84,local_80);
`

Is it as simple as decrypting the md5 hash from `3836313833366631336533643632376466613337356264623833383932313465`?
![md5](https://github.com/HenriMertens/PICOGYM/assets/149707229/3945f2da-d259-4410-9ce9-1aa117ce458d)

Looks like it is.

10) Run the programm again and see whats next:
    ![md5](https://github.com/HenriMertens/PICOGYM/assets/149707229/7bf06f40-3f85-4df9-b522-7c5f5b00d77e)

   Finally solved!!





       
