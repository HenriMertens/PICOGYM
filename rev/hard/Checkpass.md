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
- `0x7b4654436f636970` translates to picoCTF{, this part of teh code probably does an initial check
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
  - The function `FUN_001054e0` is called 4 times and then a bunch of characters gets checked
  - This probably means that the input is getting encrypted by this function and the ncompared to some predetermined values.
  - Lets inspect `FUN_001054e0` to be sure:
```c
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
          uVar1 = *(ulong *)(&DAT_001399f8 + lVar2);
          if (uVar1 < 0x20) {
            param_1[1][1] = local_20[uVar1];
            uVar1 = *(ulong *)(&DAT_001399e0 + lVar2);
```
- Looks like encryption to me
  
