Just as before we get an apk file and are tasked to get the flag.

1) Like before, I just unzipped the apk and opened it in jadx-gui. The main function leads us to the FlagstaffHill clas where we can see:

![image](https://github.com/user-attachments/assets/b9402e09-4fd4-48a8-a331-adf2ef020a8b)
  We can see that our input will be compared gainst R.string.password, this should be a hardcoded value and with a bit of help from chatgpt help I knew that it would be stored in /res/values/strings.xml.
  If the input equals password, the fenugreek(input) will be called, which mostly likely decrypts and prints the flag based on our input.

2) For some reason however, I did not look at the /res/values folder in jadx-gui, but instead looked at in the unzipped apk file. Unsprisingly I did not find the password, so I had to find the flag in another way.
   After solving the challenge I went back to this approach and found the flag stored in jadx-gui:
   ![image](https://github.com/user-attachments/assets/9b27e08f-c6fc-4c06-b4da-c19e63f502b9)

3) Since I did not look into the jadx-gui res files I had to find the flag in another way, because fenugreek is native I decided to again look into the so files with ghidra.
   We see that the funegreek function calls the anise function with the user input (presumably):
```java
undefined4
Java_com_hellocmu_picoctf_FlagstaffHill_fenugreek
          (int *param_1,undefined4 param_2,undefined4 param_3)

{
  byte bVar1;
  undefined4 uVar2;
  char *local_48;
  
  uVar2 = (**(code **)(*param_1 + 0x2a4))(param_1,param_3,0);
  bVar1 = nutmeg(uVar2);
  (**(code **)(*param_1 + 0x2a8))(param_1,param_3,uVar2);
  if ((bVar1 & 1) == 0) {
    local_48 = "try again";
  }
  else {
    local_48 = (char *)anise(uVar2);
  }
  uVar2 = (**(code **)(*param_1 + 0x29c))(param_1,local_48);
  free(local_48);
  return uVar2;
}
```
  The anise function calls the unscramble function, with a data-segemnt, "30", the input and the size of the input:
```java
void anise(char *param_1)

{
  char *pcVar1;
  size_t sVar2;
  
  pcVar1 = strdup(param_1);
  sVar2 = strlen(param_1);
  unscramble(&DAT_00011bfa,0x1e,pcVar1,sVar2);
  return;
}

```
  Finally the unscramble function looks like this:

```java
void * unscramble(int data,size_t len_data,int input,int param_4)

{
  void *pvVar1;
  int local_20;
  int i;
  
  pvVar1 = calloc(len_data,1);
  local_20 = 0;
  for (i = 0; i < (int)len_data; i = i + 1) {
    *(byte *)((int)pvVar1 + i) = *(byte *)(data + i) ^ *(byte *)(input + local_20 % param_4);
    local_20 = local_20 + 1;
  }
  return pvVar1;
}
```
4) Now to start reversing, for a detailed explanation of the unscramble function I refer you to my Droids0 write-up since its basically the same function.
   
   In short, its a basic xor encryption however unlike droids0 we dont know the encryption password (this is our input to the programm, in droids 0 this was hard coded in ghidra). This means that we have two unknowns: the flag and the password, while only having one equation: `data^password=flag`.

   Fortunately we know the flag will start with "picoCTF{", therefore we can solve the the equation for the value of password (atleast for the first 7 characters).
   
6) I created a python script that brute-forces the password based the first 7 characters of the flag being "picoCTF{". I copied over the data segment and for the first seven characters I try to find the chracacter that that solves: `data[1] ^ char[i] = picoCTF[1]`.
   After running the script we get: `opossumo`
7) I knew opossum was an animal and I also noticed that the "o" appened to to it the staring character. This lead me to believe that the password was just `opossumopossumopossumopossumopossumopossumo`
8) Now solving the equation `data^password=flag` for "flag" with previously discovered password gives: `picoCTF{pining.for.the.fjords}`
   
  
   
