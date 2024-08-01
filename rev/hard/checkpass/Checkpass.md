SOLUTION:

1) Run file normally (random input)
   - Get "invalid length"
   - Bruteforce length with brute.py script -> 41 characters
     
   ![brutepy](https://github.com/user-attachments/assets/1d2c8d41-0d9f-414a-a39f-e67d5d02f1df)

   - Get "invalid password"
  
2) Open up ghidra and go to main function
   - Main function:
     
 ```c
     void FUN_001066f0(void)

{
  code *local_8;
  
  local_8 = FUN_00105960;
  FUN_001226c0(&local_8,0x3482a8);
  return;
}
```
- See what first function does (`FUN_00105960`)
- Lots of variables get declared and then we see:
```c
  pppuVar16 = &local_128;
  pppuVar18 = &local_128;
  FUN_0011f000((undefined4 *)&local_a8);
  uStack_110 = uStack_90;
  uStack_10c = uStack_8c;
  plVar20 = local_88;
  FUN_00106a00(plVar20,&local_128);
  if (local_78 == 2) {
    if (*(long *)(local_88[0] + 0x28) == 0x29) {
      plVar4 = *(long **)(local_88[0] + 0x18);
      if ((plVar4 == (long *)&DAT_00139d78) || (*plVar4 == 0x7b4654436f636970)) {
        plVar1 = plVar4 + 5;
        in_RCX = &DAT_00139d94;
        if ((plVar1 == (long *)&DAT_00139d94) || (*(char *)plVar1 == '}')) {
          if (*(char *)(plVar4 + 1) < -0x40) {
            FUN_00134220((long)plVar4,0x29,8,0x29,&PTR_s_src/main.rs_00348260);
          }
```
- `0x7b4654436f636970` translates to picoCTF{, this part of the code probably does an initial check
- Since picoctf{} is 9 chars the actual stuff we want to find is 32 characters
- Lets analyze further:
  ```c
                FUN_001054e0((undefined (*) [16])local_70,(byte *)&local_128,0);
              uStack_110 = uStack_58;
              uStack_10c = uStack_54;
              FUN_001054e0((undefined (*) [16])local_50,(byte *)&local_128,1);
              uStack_110 = uStack_38;
              uStack_10c = uStack_34;
              FUN_001054e0((undefined (*) [16])&local_a8,(byte *)&local_128,2);
              uStack_110 = uStack_90;
              uStack_10c = uStack_8c;
              FUN_001054e0((undefined (*) [16])&local_e0,(byte *)&local_128,3);
              puVar19 = (undefined *)CONCAT71((int7)((ulong)pppuVar18 >> 8),local_e0);
              local_e9 = local_dd;
              local_e3 = local_dc;
              local_ec = local_db;
              local_e1 = local_da;
              local_f0 = local_d9;
              local_e7 = local_d8;
              uVar14 = (undefined7)((ulong)lVar12 >> 8);
              puVar13 = (undefined *)CONCAT71(uVar14,local_d7);
              local_e2 = local_d6;
              local_ee = local_d5;
              local_e5 = local_d3;
              local_f1 = local_d1;
              local_ed = local_d0;
              local_e6 = local_cf;
              local_e4 = local_ce;
              local_ea = local_cc;
              local_eb = local_cb;
              local_ef = local_ca;
              uVar15 = CONCAT71((int7)((ulong)extraout_RDX_00 >> 8),local_c8);
              local_e8 = local_c4;
              local_f2 = local_c2;
              local_128 = (undefined **)0x19;
              uVar17 = 0x19;
              local_f5 = local_de;
              local_f4 = local_c8;
              local_f3 = local_d7;
              if (local_c7 == -0x1a) {
                local_128 = (undefined **)0x0;
                uVar17 = 0;
                puVar19 = &DAT_00139d95;
                if (local_e0 == '\x1f') {
                  puVar19 = (undefined *)CONCAT71(0x139d,local_d2);
                  local_128 = (undefined **)0xe;
                  uVar17 = 0xe;
                  if (local_d2 == -7) {
                    puVar19 = (undefined *)CONCAT71(0x139d,local_cd);
                    local_128 = (undefined **)0x13;
                    uVar17 = 0x13;
                    if (local_cd == 't') {
                      puVar19 = (undefined *)CONCAT71(0x139d,local_c9);
                      local_128 = (undefined **)0x17;
                      uVar17 = 0x17;
                      if (local_c9 == '\"') {
                        puVar13 = (undefined *)CONCAT71(uVar14,local_df);
                        local_128 = (undefined **)0x1;
                        uVar17 = 1;
                        puVar19 = &DAT_00139d95
  ```
  - The function `FUN_001054e0` is called 4 times and then a bunch of characters get checked
  - This probably means that the input is getting encrypted by this function and then compared to some predetermined values.
  - Lets inspect `FUN_001054e0` to be sure:
```c
  lVar2 = param_3 * 0x100;
  local_20[0] = (&DAT_00139560)[(ulong)*param_2 + lVar2];
  local_20[1] = (&DAT_00139560)[(ulong)param_2[1] + lVar2];
  local_20[2] = (&DAT_00139560)[(ulong)param_2[2] + lVar2];
  local_20[3] = (&DAT_00139560)[(ulong)param_2[3] + lVar2];
  local_1c = (&DAT_00139560)[(ulong)param_2[4] + lVar2];
  local_1b = (&DAT_00139560)[(ulong)param_2[5] + lVar2];
  local_1a = (&DAT_00139560)[(ulong)param_2[6] + lVar2];
  local_19 = (&DAT_00139560)[(ulong)param_2[7] + lVar2];
  local_18 = (&DAT_00139560)[(ulong)param_2[8] + lVar2];
  local_17 = (&DAT_00139560)[(ulong)param_2[9] + lVar2];
  local_16 = (&DAT_00139560)[(ulong)param_2[10] + lVar2];
  local_15 = (&DAT_00139560)[(ulong)param_2[0xb] + lVar2];
  local_14 = (&DAT_00139560)[(ulong)param_2[0xc] + lVar2];
  local_13 = (&DAT_00139560)[(ulong)param_2[0xd] + lVar2];
  local_12 = (&DAT_00139560)[(ulong)param_2[0xe] + lVar2];
  local_11 = (&DAT_00139560)[(ulong)param_2[0xf] + lVar2];
  local_10 = (&DAT_00139560)[(ulong)param_2[0x10] + lVar2];
  local_f = (&DAT_00139560)[(ulong)param_2[0x11] + lVar2];
  local_e = (&DAT_00139560)[(ulong)param_2[0x12] + lVar2];
  local_d = (&DAT_00139560)[(ulong)param_2[0x13] + lVar2];
  local_c = (&DAT_00139560)[(ulong)param_2[0x14] + lVar2];
  local_b = (&DAT_00139560)[(ulong)param_2[0x15] + lVar2];
  local_a = (&DAT_00139560)[(ulong)param_2[0x16] + lVar2];
  local_9 = (&DAT_00139560)[(ulong)param_2[0x17] + lVar2];
  local_8 = (&DAT_00139560)[(ulong)param_2[0x18] + lVar2];
  local_7 = (&DAT_00139560)[(ulong)param_2[0x19] + lVar2];
  local_6 = (&DAT_00139560)[(ulong)param_2[0x1a] + lVar2];
  local_5 = (&DAT_00139560)[(ulong)param_2[0x1b] + lVar2];
  local_4 = (&DAT_00139560)[(ulong)param_2[0x1c] + lVar2];
  local_3 = (&DAT_00139560)[(ulong)param_2[0x1d] + lVar2];
  local_2 = (&DAT_00139560)[(ulong)param_2[0x1e] + lVar2];
  local_1 = (&DAT_00139560)[(ulong)param_2[0x1f] + lVar2];
  param_1[1] = ZEXT816(0);
  *param_1 = ZEXT816(0);
  uVar1 = *(ulong *)(&DAT_001399b0 + lVar2);
  if (uVar1 < 0x20) {
    (*param_1)[8] = local_20[uVar1];
    uVar1 = *(ulong *)(&DAT_00139a38 + lVar2);
    if (uVar1 < 0x20) {
      param_1[1][9] = local_20[uVar1];
      uVar1 = *(ulong *)(&DAT_00139a48 + lVar2);
      if (uVar1 < 0x20) {
        param_1[1][0xb] = local_20[uVar1];
        uVar1 = *(ulong *)(&DAT_00139a50 + lVar2);
        if (uVar1 < 0x20) {
          param_1[1][0xc] = local_20[uVar1];
```
- Looks like encryption to me, I'm not 100 % sure how it works but it just about does this:
  1) Create a new "word" based on `DAT_00139560`, where the character is chosen from `DAT_00139560` based on `(ulong)param_2[0x1f] + lVar2`.
     We can assume either param_2 or lVar2 depent on our input since there wouldnt be encryption otherwise.
     Local20 will thus store our encrypted input.
  2) Save our encrypted input in a new array `param_1` at a random index ([8], [1][9]...)
  3) Assign the index of the next character from out encrypted input by means of `uVar1 = *(ulong *)(&DAT_00139a38 + lVar2)`
- If that didnt make sense to you, good. I dont know wtf is going on either tbh.
- In conclusion: input get encrypted character by character, encrypted input get stored away randomly (I think lol, idk).
  
3) Lets look at this stuff in gdb, perhaps this will create a better picture
   - First lets just set up gdb, we know the password must start with "picoCTF{", end with "}" and must contain 41 char -> picoCTF{aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa}
     1) ```(gdb) checkpass```
     2) ```(gdb) start``` -> ```(gdb) piebase``` to see offset -> ```(gdb) run picoCTF{aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa}``` -> "invalid password": Everything looks good.
   - Lets set a breakpoint where our encrypted input gets compared to the predetermined variables (the first comparison):
     
     ``` if (local_c7 == -0x1a) ``` or in the assembly:  ``` 00105d12 3a 1c 2f        CMP        BL,byte ptr [RDI + RBP*0x1]=>DAT_00139dae        = E6h ```
   - ```(gdb) breakrva 0x5d12```: this calcultas the offset for us.
   - Lets examine the predetermined registers first:
     1) ```byte ptr [RDI + RBP*0x1]``` -> this means 1 byte is accesed at adress RDI + RBP*0x1.
     2) RDi is 0x19 = 25 but lets just examine everything from rbp
     3) ```(gdb) x/64xb $rbp```
     4) We can indeed see that the 25th byte is 0xe6 (-0x1a = 0xe6 for some reason, dont ask why)
        
      ![regrbp](https://github.com/user-attachments/assets/4403f455-fda4-464b-a8cf-100c2df148c8)

   - Now for our encrypted input register (more difficult):
     1) in ghidra we see that ```local_c7``` is stored at 
        ![c7](https://github.com/user-attachments/assets/06373f66-29f5-4b83-8d10-539c06f0188f)
     2) Normally  this mean sthat its just stored 0xc7 places above $rbp ($rbp - 0xc7) in the stack, however rbp has been assigned a new value and doesnt point to the stack anymore:
        ![rbp-wrong](https://github.com/user-attachments/assets/cd600da0-5f5f-4cb3-90b6-4f26f879223c).

     3) Lets find this adress based of $rsp then, when the stack is getting created we see: ```0010596a   SUB   RSP,0xf8``` (0xf8 = 248)
     4) Since local_c7 is stored 0xc7 (=199) places above $rbp, it will be placed 248-199 under $rsp (providing $rsp didnt change).
        
     5) This means that our variables our getting stored close to $rsp so lets just examine a big part of it:
      ![rspbiga](https://github.com/user-attachments/assets/ff40761e-8b12-4019-99a5-1a5c57849a0c)

     6) What is our input now exactly? Lets run teh programm again but now with picoCTF{baaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa}, to see if anything changes (it should)
         ![change](https://github.com/user-attachments/assets/e85b5ab7-77a9-4aaa-bbe6-fba90d0f579a)

     7) We see 1 byte changed (at a random location)! This is thus for sure our input and were also sure that changing 1 char affects only 1 byte.
        
   4) Actually solving the challenge:
      - I will be using a tool called valgrind to solve this challenge
      - Shout out to https://www.youtube.com/watch?v=HPmAzLMkENk for being my guidline here.
      - Since we know changing one character will change one byte in a random location that gets checked, we can brute force this challenge.
      - The first if statement will be fullfilled if one of our chars is correct. We can bruteforce all chars on every location and the first if-statement will have to be true for one of these combinations (40 chars for 32 pos -> 1280 combinations).
      - KEEP IN MIND: WE ARE NOTE BRUTEFORCING THE PASSWORD, JUST EACH CHARACTER INDIVIDUALLY
      - We can use valgrid to check if this if-statement has been fulfilled based on the amount of instructions it counts. When a right character at the right place gets added the machine will have to do extra instructions to get to the second if-statement.
      - I changed the python script from his video to something the I can understand better, but I made it very inefficient lol.
      - runtime: 2,5 hrs
      - Explanation of script is added to the script itself
      - If I am bothered enough I will upload a better one.




  




