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
   
4) Easy fix lol, just use an alrady initialised state
   - Open up gdb
   - Set breakpoint at main
   - Run programm
   - Hit breakpoint
   - Dump the "state" with "generate-core-file"
   - use this file in angr script instead of "enter_password"
   - Get error
   - Cry

       
