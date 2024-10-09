# SOLUTION:

Even though this challenge is classified as hard, it actually isn’t that difficult if you have the right tool installed. Anyway, I downloaded the Windows game and ran it. Immediately, you can see it’s a Unity game, and after playing around for a bit and seeing what we were supposed to do, it became clear we needed to get to the big white flag.

Now for the reversing process, it was actually quite simple. Before anything, I tried some Ghidra, but it wasn’t helpful and was really confusing. Since Unity uses C#, we can use a way better tool for decompiling C# (and .NET stuff in general): dnSpy (https://github.com/dnSpyEx/dnSpy/releases). After installing, it’s important to note that we don’t really care about the .exe file itself, but more so about the `assembly-csharp.dll`, since this will be the file containing all the scripts (for example, the script to move the character).

Opening this up in dnSpy gives:

A lot of stuff clearly, now where are the juicy parts? Well, we’re interested in the "-" folder since this indicates the root folder, and then by just looking around for a bit, we find `PlayerController`.

![pc](https://github.com/user-attachments/assets/0a0c94c5-40d6-4340-baec-3e65574f469b)

You don’t have to go this route since there are probably one million ways to hack the game, but this one is the easiest, in my opinion.

First, I tried just changing speed values, but for some reason, it did absolutely nothing. Next, I decided to change the permission for jumping; normally you need to be on the ground and whatnot, but I just deleted that part, which left me with:

![jump](https://github.com/user-attachments/assets/f9d699f8-587f-4f5e-b23a-ae8ec5f5bd2d)

Now you can just hold the spacebar to fly. Use this to fly over the invisible wall and get towards the flag.

![flag](https://github.com/user-attachments/assets/3668524c-b976-4da5-949d-b3b38a4a8f85)



