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

     Based on previous ctf experience I can assume this is used for flag encryption/decryption, I named it accordingly
   - After this we hit another code block:
     ![image](https://github.com/user-attachments/assets/e738d713-b280-4760-94e8-c17c10e1ad6a)

     Again, based on the name we can say this checks if a debugger is present, I named the function accordingly.
     We can patch this intruction from JZ to JNZ, so that this check will fail:
     ![image](https://github.com/user-attachments/assets/628f5658-b6fa-4d04-9374-85f5a660dd78)

     
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

    - Now I renamaed this big function accordingly and went back to the main fucntion, where we hit 6`thunk_FUN_00403290(param_1);`.
      Looking into tis, this just seems to draw some stuff, probably gui purposes, so I named it accordingly.

    - After this we get to ```c  bVar1 = thunk_FUN_00403310(param_1,param_4);
  if (CONCAT31(extraout_var,bVar1) == 0) {
    local_34.wParam = 0;
  }``` 

    
    




     

