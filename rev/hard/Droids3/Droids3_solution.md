This challenge is the same as the other ones, we get an apk file and need to find the flag. To emulate the programm I use the online tool https://appetize.io.


1) As usual I went to the FlagstaffHil class in jadx-gui and inspected the code:
```java
package com.hellocmu.picoctf;

import android.content.Context;

/* loaded from: /home/kali/ctf/pico/rev/three/classes.dex */
public class FlagstaffHill {
    public static native String cilantro(String str);

    public static String nope(String input) {
        return "don't wanna";
    }

    public static String yep(String input) {
        return cilantro(input);
    }

    public static String getFlag(String input, Context ctx) {
        String flag = nope(input);
        return flag;
    }
}
```
From here on you can assume that calling the yep function will result in the flag being decrypted. You can also see this with ghidra, in the decompiled lib.so file the clilantro function actually doesnt take in a string as input (it uses a hardcoded password "missingagain"). Therefore we can assume that this will just decrypt the flag.
  

1) The solution is very straight forward, this challenge is can be solved using the exact same method from droids0, I changed the python script a bit to fit this challenge but theres no difference in logic.
   The scrip gives: `picoCTF{tis.but.a.scratch}`

3) The intended solution is to do this (https://picoctf2019.haydenhousen.com/reverse-engineering/droids3):
   - Decompile the source code: `apktool d three.apk --no-res`
   - Change nope function to yes
   - Recompile `apktool b three -o recompiled/recompiled_three.apk`
   - Sign it `wget https://github.com/patrickfav/uber-apk-signer/releases/download/v1.1.0/uber-apk-signer-1.1.0.jar` and `java -jar uber-apk-signer-1.1.0.jar --apks recompiled`
   - I ran it using https://appetize.io and just pressed the button with a random input:
     
     ![image](https://github.com/user-attachments/assets/ac386344-a88b-4022-9ea5-fe10076403a3)
