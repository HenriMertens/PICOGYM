SOLUTION:

1) Download the file and open with jd-gui (Java Decompiler - Graphical User Interface)
![jd](https://github.com/user-attachments/assets/c1fcb999-7122-4d00-bf2b-39caf01408b0)

2) The code was very chaotic so I copied it to my Intellij and cleaned it up a bit (also renamed some stuff):
```java
import java.util.*;
import javax.crypto.Cipher;
import javax.crypto.spec.SecretKeySpec;
import java.security.*;
class VaultDoor8 {public static void main(String args[]) {
    Scanner scan = new Scanner(System.in);
    System.out.print("Enter vault password: ");
    String input = scan.next();
    String f = input.substring(8,input.length()-1); 

    VaultDoor8 a = new VaultDoor8();
    if (a.checkPassword(f)) {
        System.out.println("Access granted.");
    }
    else {
        System.out.println("Access denied!");
    }
}
    public char[] scramble(String password) {
    /* Scramble a password by transposing pairs of bits. */
    char[] a = password.toCharArray();
    for (int i=0; i<a.length; i++) {
        char c = a[i];
        c = switchBits(c,1,2);
        c = switchBits(c,0,3); /* c = switchBits(c,14,3); c = switchBits(c, 2, 0); */
        c = switchBits(c,5,6);
        c = switchBits(c,4,7);
        c = switchBits(c,0,1); /* d = switchBits(d, 4, 5); e = switchBits(e, 5, 6); */
        c = switchBits(c,3,4);
        c = switchBits(c,2,5);
        c = switchBits(c,6,7);
        a[i] = c;
    } return a;
}
public char switchBits(char c, int p1, int p2) {/* Move the bit in position p1 to position p2, and move the bit
that was in position p2 to position p1. Precondition: p1 < p2 */
    char mask1 = (char)(1 << p1);
    char mask2 = (char)(1 << p2); /* char mask3 = (char)(1<<p1<<p2); mask1++; mask1--; */
    char bit1 = (char)(c & mask1);
    char bit2 = (char)(c & mask2); /* System.out.println("bit1 " + Integer.toBinaryString(bit1));
System.out.println("bit2 " + Integer.toBinaryString(bit2)); */
    char rest = (char)(c & ~(mask1 | mask2));
    char shift = (char)(p2 - p1);
    char result = (char)((bit1<<shift) | (bit2>>shift) | rest); return result;
}
public boolean checkPassword(String password) {
    char[] scrambled = scramble(password);
    char[] expected = {
        0xF4, 0xC0, 0x97, 0xF0, 0x77, 0x97, 0xC0, 0xE4, 0xF0, 0x77, 0xA4, 0xD0, 0xC5, 0x77, 0xF4, 0x86, 0xD0, 0xA5, 0x45, 0x96, 0x27, 0xB5, 0x77, 0xD2, 0xD0, 0xB4, 0xE1, 0xC1, 0xE0, 0xD0, 0xD0, 0xE0
    };
    return Arrays.equals(scrambled, expected);
}


}
```
  3) Now we can start analyzing the code:
     - Firstly a scanner object gets created ```Scanner scan = new Scanner(System.in);```

       If you dont know java, this will just reads user input
     - Next the first 8 characters and the last character get stripped ```String f = input.substring(8,input.length()-1);```, we can assume this will just be to account for "picoctf{}".
     - After this the "checkpassword" function gets called ```if (a.checkPassword(f))```, this function in return calls the "scramble" function, ```char[] scrambled = scramble(password);``` and compares the scarmbled input against some array.
     - The scramble function just iterates through every character and switches some bits, I assumed the switchbit function was actually working and correctly implemented.
       
  4) Summary:
     the script asks for a password, strips it, switches the bits of every character, compares to a predetermined array.
     
  5) How to solve:

     There are two main ways you can go about this problem, you can take each value in the predetermined array and do the bit switching in reverse, or you can just bruteforce every character and see for which one it equals to the value in the array.

     I went with the second route because it was slightly easier to implement imo (both are very easy though im just lazy lol).

     You can do this either in java (and just reuse the switchBits function) or copy into python and make your own function.

     I did it in python but looking back at it I should have done it in java, since if there was an mistake in the switchbits function the mistake would have also gotten reversed.

     Anyway I used chatgpt to make the switchBits logic part of the script and then I just implemented the rest of the logic.

      After running the script it returns the password as expected.

     ```s0m3_m0r3_b1t_sh1fTiNg_91c642112```

     Now just dont forget to add picoctf{}.

     ```picoctf{s0m3_m0r3_b1t_sh1fTiNg_91c642112}```
     
     
