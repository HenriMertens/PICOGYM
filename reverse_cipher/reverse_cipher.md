1) Run file normally
   - We get some weird errors
     
    ![error](https://github.com/HenriMertens/PICOGYM/assets/149707229/f3451c41-c07a-4dc8-9cbe-251fd9fabc97)
    

   - txt file just contains an encrypted flag
     picoCTF{w1{1wq8/7376j.:}
     
2) Open file ghidra
   - We can see what causes these weird errors, we dont have a flag.txt file.
```c
    void main(void)

{
  size_t sVar1;
  char local_58 [23];
  char local_41;
  int local_2c;
  FILE *local_28;
  FILE *local_20;
  uint local_14;
  int local_10;
  char local_9;
  
  local_20 = fopen("flag.txt","r");
  local_28 = fopen("rev_this","a");
  if (local_20 == (FILE *)0x0) {
    puts("No flag found, please make sure this is run on the server");
  }
  if (local_28 == (FILE *)0x0) {
    puts("please run this on the server");
  }
  sVar1 = fread(local_58,0x18,1,local_20);
  local_2c = (int)sVar1;
  if ((int)sVar1 < 1) {
                    /* WARNING: Subroutine does not return */
    exit(0);
  }
  for (local_10 = 0; local_10 < 8; local_10 = local_10 + 1) {
    local_9 = local_58[local_10];
    fputc((int)local_9,local_28);
  }
  for (local_14 = 8; (int)local_14 < 0x17; local_14 = local_14 + 1) {
    if ((local_14 & 1) == 0) {
      local_9 = local_58[(int)local_14] + '\x05';
    }
    else {
      local_9 = local_58[(int)local_14] + -2;
    }
    fputc((int)local_9,local_28);
  }
  local_9 = local_41;
  fputc((int)local_41,local_28);
  fclose(local_28);
  fclose(local_20);
  return;
}
```
- We can solve this error by just creating a flag.txt ourselves.
- Its improtant to note that ```c sVar1 = fread(local_58,0x18,1,local_20 ``` read the contents of the flag.txt file and puts it in the local_58 variable. sVar1 is assigned a value absed on if the file was read succesfully.
- The errors also tell us some important information:
  The flag.txt was on the server and contained the actual flag, when the programm was run on the server it opened the flag.txt, encrypted it contents and put the encrypted flag in rev_this.
  Knowing this I changed some of the variable names to make it easier to understand:

 ```c
void main(void)

{
  size_t sVar1;
  char flag.txt_contents [23];
  char local_41;
  int local_2c;
  FILE *rev_this.txt;
  FILE *flag.txt;
  uint j;
  int i;
  char temp_storage;
  
  flag.txt = fopen("flag.txt","r");
  rev_this.txt = fopen("rev_this","a");
  if (flag.txt == (FILE *)0x0) {
    puts("No flag found, please make sure this is run on the server");
  }
  if (rev_this.txt == (FILE *)0x0) {
    puts("please run this on the server");
  }
  sVar1 = fread(flag.txt_contents,0x18,1,flag.txt);
  local_2c = (int)sVar1;
  if ((int)sVar1 < 1) {
                    /* WARNING: Subroutine does not return */
    exit(0);
  }
  for (i = 0; i < 8; i = i + 1) {
    temp_storage = flag.txt_contents[i];
    fputc((int)temp_storage,rev_this.txt);
  }
  for (j = 8; (int)j < 0x17; j = j + 1) {
    if ((j & 1) == 0) {
      temp_storage = flag.txt_contents[(int)j] + '\x05';
    }
    else {
      temp_storage = flag.txt_contents[(int)j] + -2;
    }
    fputc((int)temp_storage,rev_this.txt);
  }
  temp_storage = local_41;
  fputc((int)local_41,rev_this.txt);
  fclose(rev_this.txt);
  fclose(flag.txt);
  return;
}
  
```
  
