This challenge is very similar two droids0, we get an apk file and are asked to get the flag. For some reason this challenge was very easy, this shouldnt be in the hard category.

1) Unzip the apk file: `unzip two.apk` and open it up in jadx-gui, the main function again leads us to this Flagstaffhill class:
   ![image](https://github.com/user-attachments/assets/068f0f67-a5b9-4d0c-883c-7f891d98db22)

2) Just like in the prvious challenge some native string is initialised. We can also see a weird return statement: `return input.equals(password) ? sesame(input) : "NOPE";`
   This is like a compacted if-else block: if the input.equals(password) is true then sesame(password) is called, else "NOPE" is returned.
3) We can assume that if enter the correct password then sesame(password) will probably return the flag.
4) The password is not very wel hidden is just calculated based on concatenating `String[] witches = {"weatherwax", "ogg", "garlick", "nitt", "aching", "dismass"};`in some weird order.
   I just copied this java code in my IntelliJ and printed out the password:
   
```java
   public class Main {
    public static String getFlag() {
        String[] witches = {"weatherwax", "ogg", "garlick", "nitt", "aching", "dismass"};
        int second = 3 - 3;
        int third = (3 / 3) + second;
        int fourth = (third + third) - second;
        int fifth = 3 + fourth;
        int sixth = (fifth + second) - third;
        String password = "".concat(witches[fifth]).concat(".").concat(witches[third]).concat(".").concat(witches[second]).concat(".").concat(witches[sixth]).concat(".").concat(witches[3]).concat(".").concat(witches[fourth]);
        return password;
    }


    public static void main(String[] args) {
        System.out.println(getFlag());
    }

}
```
-> dismass.ogg.weatherwax.aching.nitt.garlick
5) I ran the apk via an online emulator https://appetize.io and entered in the password.
   As expected it returned the flag: `picoCTF{what.is.your.favourite.colour}`
   This challenge was so easy I think I might have done something wrong in the previous one lol

   
