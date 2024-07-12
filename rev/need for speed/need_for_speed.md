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
As for as I understand `__sysv_signal(0xe,alarm_handler)` sets up a listener. It listens for 0xe (14), which corresponds to `SIGALRM`. If it receives a signal it calls `alarm_handler`, this function just prints "boom" and closes the programm.
alarm(1) sends this `SIGALRM` after 1 second.

```
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
At the moment we also do not care how this is decrypted

 ```
