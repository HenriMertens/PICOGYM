Same task as usual

1) I unzipped the apk and opened it in jadx-gui, navigating to the Flagstaffhill class gives:
```java
package com.hellocmu.picoctf;

import android.content.Context;

/* JADX WARN: Classes with same name are omitted:
  classes.dex
 */
/* loaded from: /home/kali/ctf/pico/rev/four/classes.dex */
public class FlagstaffHill {
    public static native String cardamom(String str);

    public static String getFlag(String input, Context ctx) {
        StringBuilder ace = new StringBuilder("aaa");
        StringBuilder jack = new StringBuilder("aaa");
        StringBuilder queen = new StringBuilder("aaa");
        StringBuilder king = new StringBuilder("aaa");
        ace.setCharAt(0, (char) (ace.charAt(0) + 4));
        ace.setCharAt(1, (char) (ace.charAt(1) + 19));
        ace.setCharAt(2, (char) (ace.charAt(2) + 18));
        jack.setCharAt(0, (char) (jack.charAt(0) + 7));
        jack.setCharAt(1, (char) (jack.charAt(1) + 0));
        jack.setCharAt(2, (char) (jack.charAt(2) + 1));
        queen.setCharAt(0, (char) (queen.charAt(0) + 0));
        queen.setCharAt(1, (char) (queen.charAt(1) + 11));
        queen.setCharAt(2, (char) (queen.charAt(2) + 15));
        king.setCharAt(0, (char) (king.charAt(0) + 14));
        king.setCharAt(1, (char) (king.charAt(1) + 20));
        king.setCharAt(2, (char) (king.charAt(2) + 15));
        String password = "".concat(queen.toString()).concat(jack.toString()).concat(ace.toString()).concat(king.toString());
        return input.equals(password) ? "call it" : "NOPE";
    }
}

```
  2) We can see some kind of password being generated here, I copied it to my InteliJ and changed it slightly so it just prints the flag:
```java


public class droids4 {
    public static native String cardamom(String str);

    public static String getFlag() {
        StringBuilder ace = new StringBuilder("aaa");
        StringBuilder jack = new StringBuilder("aaa");
        StringBuilder queen = new StringBuilder("aaa");
        StringBuilder king = new StringBuilder("aaa");
        ace.setCharAt(0, (char) (ace.charAt(0) + 4));
        ace.setCharAt(1, (char) (ace.charAt(1) + 19));
        ace.setCharAt(2, (char) (ace.charAt(2) + 18));
        jack.setCharAt(0, (char) (jack.charAt(0) + 7));
        jack.setCharAt(1, (char) (jack.charAt(1) + 0));
        jack.setCharAt(2, (char) (jack.charAt(2) + 1));
        queen.setCharAt(0, (char) (queen.charAt(0) + 0));
        queen.setCharAt(1, (char) (queen.charAt(1) + 11));
        queen.setCharAt(2, (char) (queen.charAt(2) + 15));
        king.setCharAt(0, (char) (king.charAt(0) + 14));
        king.setCharAt(1, (char) (king.charAt(1) + 20));
        king.setCharAt(2, (char) (king.charAt(2) + 15));
        String password = "".concat(queen.toString()).concat(jack.toString()).concat(ace.toString()).concat(king.toString());
        return password;
    }

    public static void main(String[] args) {
        System.out.println(getFlag());
    }
}

```
  -> alphabetsoup

3) Now the function would return "call it", I assume the auhtor wants us to change to code so that it calls the cardamon function with this string. I had no intention of doing this and just decided to reverse the lib.so file again since I figured the same encryption would be used as for the three previous challenges.
4) I was right and now we can use the solution from Droids0 or Droids3 again. I used the exact same pythons script and changed the values that were different, after running it I got:
   `picoCTF{not.particularly.silly}`
