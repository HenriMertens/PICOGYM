This challenge is a little different from before, we get an executable with some files attached but this time it has a gui.

1) First thing to do is notice tha the file is upx compressed, so we need to uncompress is: `upx -d  WinAntiDbg0x300.exe`

2) After this I opened the binary in ghidra, so I can alalyse it:
   - First thing I did was search for the string that pop ups when you just run it normally with a debugger attached, after finding this we can see it gets called in this function:
     ![image](https://github.com/user-attachments/assets/a4660ab8-1e3c-4244-bf1e-469ef59ec6fb)

   - I followed the call three of this function and saw that this was basically the "main" function so I named it accordingly.
  
   - The first three functions dont seems that ineteresting and seem to be used to initialize and load some stuff, so we can ignore them for now
  
   - Next we get to the next code block:
     ![image](https://github.com/user-attachments/assets/2f76bcc3-bb5b-4cbd-abbf-fefbba76c205)

     Based on the message in the if block we can say this just tries to open and read the config file, I named it accordingly
   - Next up we have: `thunk_FUN_00402bc0(3);`:
     ![image](https://github.com/user-attachments/assets/d5c2f863-71f3-40ba-a58f-d5f245b5225d)

     Based on prvious ctf experience I can assume this is used for flag encryption/decryption, I named it accordingly
   - After this we hit another code block:
     ![image](https://github.com/user-attachments/assets/e738d713-b280-4760-94e8-c17c10e1ad6a)

     Again, based on the name we can say this checks if a debugger is present, I named the function accordingly.
   - Next we hit another flag decrypt function follewed by: `thunk_FUN_00402f10();`:
     ![image](https://github.com/user-attachments/assets/b4d3968a-cf7c-46cc-b7f2-3a0df249ab6b)

     Again based of the comments we can see that this just checks if the programm is being run with admin priviliges.

   - After this we hit:
       ```c
        flag_decrypt(2);
        local_c = GetCommandLineW();
        local_10 = CommandLineToArgvW(local_c,&local_14);
      ```
     The last two functions dont decompile and so we cant do anything ot analyze them, but you cna guess what they do based on the name, or you can search them on google.

  - 
    
    




     

