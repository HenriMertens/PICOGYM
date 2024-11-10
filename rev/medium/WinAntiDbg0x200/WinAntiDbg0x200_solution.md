This challenge is basically the same one as before but the description tells us to run the debugger as administrator.

The challenge was very annoying for me since for some reason my breakpoints weren hitting in windbg, so after struggling for a while and trying to debug the debugger (lol), I gave up and insatlled x64 dbg (I should have installed this in the beginning since it looks way better)
https://x64dbg.com/ 

1) Run x32dbg as admin and press "continue untill user input":
   ![image](https://github.com/user-attachments/assets/f49ac2f5-37b8-4fdc-83b5-129859811937)

2) Again if we run normally it will say debugger is detected, we can see this in the log files:
   ![image](https://github.com/user-attachments/assets/060758da-5a2b-445e-b6f9-136b700f8d48)
   For some reason everythin is getting printed twice (idk why)

3) To find the right adress to set breakpoint, I again used ghidra:
   ![image](https://github.com/user-attachments/assets/127293fe-fb5d-4737-8374-c5c6b5ce4393)

4) I tried setting the breakpoint at 0x961828 (offset of x32dbg is 9610000) and running the programm, however this doesnt hit the breakpoint.
   This means that one of the cmp statements fails, by looking at the log again we see `DebugString: "### Oops! The debugger was detected. Try to bypass this check to get the flag!"`is getting printed. This gets printed when `cVar1 != '\0'`, which means this condition fails and we need to set a breakpoint here.
   
5) Now we need to set the breakpoint: `bp 0x9611828` and change the value of the edx register to 0:
   ![image](https://github.com/user-attachments/assets/0f03dda6-6e14-48c4-8ffa-2f39e28c5289)

6) After this we just step until the "deubggerispresent" function, step one more time to call this function and  change the eax register to zero:
   ![image](https://github.com/user-attachments/assets/f0cf0b3b-cf67-4508-8162-c308285f0248)

7) Then just continue the programm and in your logs you should have the flag: picoCTF{0x200_debug_f0r_Win_cec13522}





