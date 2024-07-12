1) Run file normally
   - We explode -> not good
     
     ![explode](https://github.com/user-attachments/assets/0006bcc8-d72b-4ed4-8a18-14560d39ac83)
     

2) Open file in ghidra and examine the main function:
   
```c
undefined8 main(void)

{
  header();
  set_timer();
  get_key();
  print_flag();
  return 0;
}
 ```
- header() just prints the first lines we see:
```c
  
void header(void)

{
  uint local_c;
  
  puts("Keep this thing over 50 mph!");
  for (local_c = 0; local_c < 0x1c; local_c = local_c + 1) {
    putchar(0x3d);
  }
  puts("\n");
  return;
}


```
- set_timer() sets an alarm the calls the function alarm_handler after one second:
```c
  void set_timer(void)

{
  __sighandler_t p_Var1;
  
  p_Var1 = __sysv_signal(0xe,alarm_handler);
  if (p_Var1 == (__sighandler_t)0xffffffffffffffff) {
    puts("\n\nSomething bad happened here. ");
                    /* WARNING: Subroutine does not return */
    exit(0);
  }
  alarm(1);
  return;
}
```
As far as I understand `__sysv_signal(0xe,alarm_handler)` sets up a listener. It listens for 0xe (14), which corresponds to `SIGALRM`. If it receives a signal it calls `alarm_handler`, this function just prints "boom" and closes the programm.
 `alarm(1)` sends this `SIGALRM` after 1 second.


- get_key gets a key (= encrypted flag):
```c
void get_key(void)

{
  puts("Creating key...");
  key = calculate_key();
  puts("Finished");
  return;
}
```
At the moment we dont really care how.

- print_flag decrypts the key and prints the decrypted key:
```c

void print_flag(void)

{
  puts("Printing flag:");
  decrypt_flag(key);
  puts(flag);
  return;
}

 ```
At the moment we also do not care how this is decrypted
SOLUTION:
- If we can avoid the timer we can just print teh flag withouth it vlosing the programm.
- There are numerous ways to do this:
  1) Change set_timer to NOP instructions in ghidra
     
   ![patch](https://github.com/user-attachments/assets/ebef33f2-29a6-4bf4-b7a5-a0527e6a11f0)

   ![nop1](https://github.com/user-attachments/assets/423efe53-3c83-4c2f-9f10-4ef6dea60eb9)
   ![nop2](https://github.com/user-attachments/assets/771c2b79-9a57-4256-992e-0e1d1ae1ca02)
   ![nop3](https://github.com/user-attachments/assets/4985b1b9-0d7d-46b5-86c1-ccc834c15400)

  2) Change set_timer to get_key (or something else) in ghidra
     
     ![get_key1](https://github.com/user-attachments/assets/b988b683-1af3-4120-89d2-7127298706ae)
     ![get_key2](https://github.com/user-attachments/assets/25788acc-dbcd-42f8-831f-a1dfa90f1144)

  4) Set breakpoint just before set_timer is called in gdb and manually set $rip to the addres of get_flag
     ![gdb1](https://github.com/user-attachments/assets/88a5e50d-6da0-4f78-acdf-bf5132fba105)
     ![gdb2](https://github.com/user-attachments/assets/1778d991-3bba-4e7b-ba6c-e5bf0412aaa5)
     ![gdb3](https://github.com/user-attachments/assets/f3fa76bd-8ba4-4708-ba8f-cd5e03f655a4)

  5) .....
