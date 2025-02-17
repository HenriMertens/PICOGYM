This challenge is a little different from before, we get an executable with some files attached but this time it has a gui.

1) First thing to do is notice that the file is upx compressed, so we need to uncompress it: `upx -d  WinAntiDbg0x300.exe`

2) After this I opened the binary in ghidra, so I can alalyse/patch it:
   - First thing I did was search for the string that pops ups when you just run it normally with a debugger attached, after finding this we can see it gets called in this function:
     ![image](https://github.com/user-attachments/assets/a4660ab8-1e3c-4244-bf1e-469ef59ec6fb)

   - I followed the call three of this function and saw that this was basically the "main" function, so I named it accordingly.
  
   - The first three functions dont seem that interesting and seem to just initialize/load some stuff, so we can ignore them for now.
  
   - Next we get to the this code block:
     
     ![image](https://github.com/user-attachments/assets/2f76bcc3-bb5b-4cbd-abbf-fefbba76c205)

     Based on the message in the if block, we can say that this just tries to open and read the config file, I named it accordingly
   - Next up we have: `thunk_FUN_00402bc0(3);`:
     ![image](https://github.com/user-attachments/assets/d5c2f863-71f3-40ba-a58f-d5f245b5225d)

     Based on previous ctf experience I can assume this is used for flag encryption/decryption, I named it accordingly
   - After this we hit another code block:
     ![image](https://github.com/user-attachments/assets/e738d713-b280-4760-94e8-c17c10e1ad6a)

     Again, based on the name we can say that this checks if a debugger is present, I named the function accordingly.
     We can patch this instruction from JZ to JNZ, so that this check will fail:
     ![image](https://github.com/user-attachments/assets/628f5658-b6fa-4d04-9374-85f5a660dd78)

     
   - Next we hit another flag decrypt function followed by: `thunk_FUN_00402f10();`:
     ![image](https://github.com/user-attachments/assets/b4d3968a-cf7c-46cc-b7f2-3a0df249ab6b)

     Again based on the comments we can see that this just checks if the program is being run with admin privileges.

   - After this we hit:
       ```c
        flag_decrypt(2);
        local_c = GetCommandLineW();
        local_10 = CommandLineToArgvW(local_c,&local_14);
      ```
     The last two functions dont decompile and so we cant do anything to analyze them, but you can guess what they do based on the name, or you can search them up on google.

  - Next we get to `thunk_FUN_00403050(local_14,(int)local_10);`:
    ```c
                  void __cdecl FUN_00403050(int param_1,int param_2)
                  
                  {
                    DWORD DVar1;
                    LPSTR _Str;
                    BOOL BVar2;
                    int iVar3;
                    HANDLE hProcess;
                    
                    flag_decrypt(1);
                    DAT_0040c3c8 = CreateMutexW((LPSECURITY_ATTRIBUTES)0x0,0,(LPCWSTR)&DAT_0040c3e0);
                    if (DAT_0040c3c8 == (HANDLE)0x0) {
                      MessageBoxW((HWND)0x0,L"[FATAL ERROR] Failed to create the Mutex. Challenge aborted.",
                                  (LPCWSTR)&DAT_0040c3e0,0x10);
                      thunk_FUN_00402e00(0xff);
                    }
                    DVar1 = GetLastError();
                    if (DVar1 == 0xb7) {
                      if (param_1 != 2) {
                        OutputDebugStringW(
                                          L"[ERROR] Exactly two arguments expected by the Child process. Exiting...\n"
                                          );
                        MessageBoxW((HWND)0x0,L"Check if the program is already running.",(LPCWSTR)&DAT_0040c3e0,0x10)
                        ;
                        CloseHandle(DAT_0040c3c8);
                        thunk_FUN_00402e00(0xff);
                      }
                      _Str = thunk_FUN_00402d80(*(LPCWSTR *)(param_2 + 4));
                      if (_Str == (LPSTR)0x0) {
                        OutputDebugStringW(L"Error converting WChar to Char.\n");
                        CloseHandle(DAT_0040c3c8);
                        thunk_FUN_00402e00(0xff);
                      }
                      DVar1 = atoi(_Str);
                      BVar2 = DebugActiveProcess(DVar1);
                      if (BVar2 == 0) {
                        iVar3 = atoi(_Str);
                        DVar1 = thunk_FUN_00402e60(iVar3);
                        hProcess = OpenProcess(1,0,DVar1);
                        if (hProcess == (HANDLE)0x0) {
                          CloseHandle(DAT_0040c3c8);
                          free(_Str);
                          OutputDebugStringW(L"Error opening a handle to debuggerPID.\n");
                          thunk_FUN_00402e00(0xff);
                        }
                        BVar2 = TerminateProcess(hProcess,0);
                        if (BVar2 == 0) {
                          OutputDebugStringW(L"Failed to terminate the debugger process.\n");
                          free(_Str);
                          CloseHandle(DAT_0040c3c8);
                          thunk_FUN_00402e00(0xfe);
                        }
                        else {
                          OutputDebugStringW(L"Debugger process terminated successfully.\n");
                          free(_Str);
                          CloseHandle(DAT_0040c3c8);
                          thunk_FUN_00402e00(0xfd);
                        }
                      }
                      else {
                        OutputDebugStringW(L"No debugger was present. Exiting successfully.\n");
                        DVar1 = atoi(_Str);
                        DebugActiveProcessStop(DVar1);
                        CloseHandle(DAT_0040c3c8);
                        free(_Str);
                        thunk_FUN_00402e00(0);
                      }
                      thunk_FUN_00402e00(0);
                    }
                    flag_decrypt(1);
                    return;
                  }
      ```
    Again we can see what everything is supposed to do based of the comments. You would think we want to hit "No debugger was present. Exiting successfully.\n", but notice that every function calls: `thunk_FUN_00402e00(0)`, which in return calls the exit function. This means we never want to enter this if block. To make sure we never enter it I patched the if-statement to a non existent value:
    
    ![image](https://github.com/user-attachments/assets/30f7f187-6f1d-4711-89c3-e7021d12c50b)

    - Now I renamed this big function accordingly and went back to the main function, where we hit `thunk_FUN_00403290(param_1);`.
      Looking into this, this just seems to draw some stuff, probably gui purposes, so I named it accordingly.

    - After this we get to:
         ```c  bVar1 = thunk_FUN_00403310(param_1,param_4);
           if (CONCAT31(extraout_var,bVar1) == 0) {
             local_34.wParam = 0;
           }
         ```
      This also doesnt seems to important since it just opens a window or something, I named it accordingly.

    - After this no function are able to be decompiled, so were stuck lol. Where is the flag?
      When searching for strings we also saw a flag string in the program, navigating to the function that calls it is gives: `FUN_00403740`
         ```c
                  /* WARNING: Removing unreachable block (ram,0x004038e0) */
                  /* WARNING: Removing unreachable block (ram,0x00403911) */
                  /* WARNING: Removing unreachable block (ram,0x00403929) */
                  
                  undefined4 FUN_00403740(void)
                  
                  {
                    WCHAR local_384 [260];
                    CHAR local_17c [272];
                    _STARTUPINFOA local_6c;
                    BOOL local_24;
                    DWORD local_20;
                    _PROCESS_INFORMATION local_1c;
                    DWORD local_8;
                    
                    memset(&local_6c,0,0x44);
                    local_6c.cb = 0x44;
                    local_1c.hProcess = (HANDLE)0x0;
                    local_1c.hThread = (HANDLE)0x0;
                    local_1c.dwProcessId = 0;
                    local_1c.dwThreadId = 0;
                    local_8 = 0;
                    local_20 = GetCurrentProcessId();
                    GetModuleFileNameW((HMODULE)0x0,local_384,0x104);
                    thunk_FUN_00403e50(local_17c,0x110,"%ws %d",(char)local_384);
                    flag_decrypt(2);
                    do {
                      local_24 = CreateProcessA((LPCSTR)0x0,local_17c,(LPSECURITY_ATTRIBUTES)0x0,
                                                (LPSECURITY_ATTRIBUTES)0x0,0,0,(LPVOID)0x0,(LPCSTR)0x0,&local_6c,
                                                &local_1c);
                      if (local_24 == 0) {
                        MessageBoxW(DAT_0040c704,
                                    L"[FATAL ERROR]  Unable to create the child process. Challenge aborted.",
                                    (LPCWSTR)&DAT_0040c3e0,0x10);
                        thunk_FUN_00402e00(0xff);
                      }
                      WaitForSingleObject(local_1c.hProcess,0xffffffff);
                      GetExitCodeProcess(local_1c.hProcess,&local_8);
                      if (local_8 == 0xff) {
                        MessageBoxW(DAT_0040c704,L"Something went wrong. Challenge aborted.",(LPCWSTR)&DAT_0040c3e0,
                                    0x10);
                        thunk_FUN_00402e00(0xff);
                      }
                      else if (local_8 == 0xfe) {
                        MessageBoxW(DAT_0040c704,
                                    L"The debugger was detected but our process wasn\'t able to fight it. Challenge ab orted."
                                    ,(LPCWSTR)&DAT_0040c3e0,0x10);
                        thunk_FUN_00402e00(0xff);
                      }
                      else if (local_8 == 0xfd) {
                        MessageBoxW(DAT_0040c704,
                                    L"Our process detected the debugger and was able to fight it. Don\'t be surprised if the debugger crashed."
                                    ,(LPCWSTR)&DAT_0040c3e0,0x10);
                      }
                      CloseHandle(local_1c.hProcess);
                      CloseHandle(local_1c.hThread);
                      Sleep(5000);
                    } while( true );
                  }
                  
         ```

         We can see some more debugger stuff, but more importantly where is the flag text?
         It seems it doesnt get called, inspecting the function we can see that this is just an infinite loop since "while true" will always be true.
         Looking at the assembly we can see:
      
         ![image](https://github.com/user-attachments/assets/cc47faff-cb45-4745-9d8c-1ce805d2c8a8)
      
         The infinite loop is because of this jump statement, which brings us back to the top. What if instead of jumping to that lab we jump to the next LAB block (note jumping directly to the flag block doesnt work, I tried):
      
         ![image](https://github.com/user-attachments/assets/541ba57d-94f8-46cf-8ff7-bf505f8c5962)



         Patching it:

         ![image](https://github.com/user-attachments/assets/11eb4f77-5d10-4d17-b7aa-a7267d95385c)


      - Okay nice what now? Last thing we need to do is make sure we reach the flag function, which we can achieve by just doing some non-existent exit codes at the if statements.
        ![image](https://github.com/user-attachments/assets/f2f0791d-19b5-4fcd-888e-f85f633848b3)

      - One last thing to do is to remove the sleep function, I just set it to 0x1.
     
   
3) Now we should be able to just run this in a debugger and get the flag:
   ![image](https://github.com/user-attachments/assets/ec2f40bd-a2e7-454e-ac95-dfbbbdf35fdc)

   picoCTF{Wind0ws_antid3bg_0x300_da7fdd01}

    
    




     

