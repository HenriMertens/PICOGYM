In this challenge we get an exe file and are tasked with debugging it. I have no prior experience with debugging exe files on windows so this walkthrough will be very basic.

1) Install and launch windbg https://learn.microsoft.com/en-us/windows-hardware/drivers/debugger/

2) Launch the exectubale:
   ![image](https://github.com/user-attachments/assets/7b3ee390-fdb9-471c-8d53-8676fb28c4bc)

3) After running it with "g" (go) we get a message telling us we failed:
   ![image](https://github.com/user-attachments/assets/ca51deb7-b615-4fa9-b49a-568873efbf5a)

4) Seems we need to find and patch the instruction that is detecting our debugger. To do this I opened the file in ghidra and tried looking for the function that is responsible:
   - Search for strings in ghidra
     ![image](https://github.com/user-attachments/assets/837861dc-6e27-4e0b-94c2-d0ac9af1b633)
   - Find where this string is used, it brings us to this function which I have renamed "main"
     ![image](https://github.com/user-attachments/assets/9a511bf0-97fc-4072-afb3-9d4bebd67ce8)
   - We find `BVar3 = IsDebuggerPresent();` at `0x4015fc`

  5) An easy way to solve this without using windgb would be to patch `if (BVar3 == 0)` to `if (BVar3 != 0)`. However since I'm doing this challenge to learn windbg I didnt do this.
  6) Now we want to set a breakpoint in windgb at offset 0x15fc (ghidra used base adress 0x40000), however windbg expects an absolute adress so wen need to find this.
     - using `lm` (list modules) we see:
       ![image](https://github.com/user-attachments/assets/8f58062d-f89c-4645-8bde-b047db0a50eb)
     - more specifically: `00920000 00928000   WinAntiDbg0x100 C (no symbols)`
     This tells use the exe starts at offset 0x920000, so our absolute adress is `0x920000 + 0x15fc = 0x9215fc`
  7) Now we first restart the program using `.restart` and then set the breakpoint using `bp 0x9215fc`, after this we can continue the programm with `g`:
     I also went to view>disassembly to get a nice list of all the next instrutions.
     ![image](https://github.com/user-attachments/assets/c798407f-cae8-4bd3-91c3-7bc3a1867617)
  8) In the disassembly view we can see `test eax eax`, this just checks if eax is zero, since we want to change the outcome we need to change what eax is.
     - First call the current instruction, since this is `IsDebuggerPresent()`: `p` (proceed)
     - Finding the value of eax: `r` (registers) -> `eax=00000001`
     - Setting eax to 0: `r eax=0`
     - Continuing the program: `g`
  9) This gives us:
      ![image](https://github.com/user-attachments/assets/98b8917e-9e6c-4311-a170-f51b4bb7006b)
     picoCTF{d3bug_f0r_th3_Win_0x100_cc0ff664}

     
  
    

     
       


   

