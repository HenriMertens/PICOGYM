For this challenge we get an apk file and need to find the flag within it.

1) First thing I did was unzip the apk file `unzip zero.apk`, this doesnt create a folder for you so I put everything in a folder called "zero"

2) After this I looked around and didtn find anything interesting by just trying to grep stuff, so I decided to use jadx-gui to analyze further: `jadx-gui` -> select the "zero" folder.

3) Now we can see the decompiled java code, to start of I went to the `MainActivity`class since this is probably were all the code-flow starts.
```java
   package com.hellocmu.picoctf;

import android.content.Context;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import androidx.appcompat.app.AppCompatActivity;

/* JADX WARN: Classes with same name are omitted:
  /home/kali/pico/rev/droids/zero/classes.dex
 */
/* loaded from: classes.dex */
public class MainActivity extends AppCompatActivity {
    Button button;
    Context ctx;
    TextView text_bottom;
    EditText text_input;
    TextView text_top;

    /* JADX INFO: Access modifiers changed from: protected */
    @Override // androidx.appcompat.app.AppCompatActivity, androidx.fragment.app.FragmentActivity, androidx.core.app.ComponentActivity, android.app.Activity
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        this.text_top = (TextView) findViewById(R.id.text_top);
        this.text_bottom = (TextView) findViewById(R.id.text_bottom);
        this.text_input = (EditText) findViewById(R.id.text_input);
        this.ctx = getApplicationContext();
        System.loadLibrary("hellojni");
        this.text_top.setText(R.string.hint);
    }

    public void buttonClick(View view) {
        String content = this.text_input.getText().toString();
        this.text_bottom.setText(FlagstaffHill.getFlag(content, this.ctx));
    }
}
```
  Looks like this gets some user input and then calls the getFlag function with that same input.
  4) After this I went to the `FlagstaffHill`class since this class contains the `getFlag` method (function).
```java
package com.hellocmu.picoctf;

import android.content.Context;
import android.util.Log;

/* JADX WARN: Classes with same name are omitted:
  /home/kali/pico/rev/droids/zero/classes.dex
 */
/* loaded from: classes.dex */
public class FlagstaffHill {
    public static native String paprika(String str);

    public static String getFlag(String input, Context ctx) {
        Log.i("PICO", paprika(input));
        return "Not Today...";
    }
}
```
This looks very interesting, a weird native paprika function is called with our input `public static native String paprika(String str);` and it then logs the result.
A native function in java basically means that the function is actually written in C and called via a shared library.

  5) Next I wanted to find this library, I just went to the zero folder and did `grep -r paprika`. This gave the following:
![image](https://github.com/user-attachments/assets/bafa9c44-4c99-4ff1-b8b4-5dc6e4d381bd)

  6) After this I navigated to one of the so files (doesnt really matter which one I chose x86), and opend it in ghidra. After ghidra's is done analysing we can see our paprika function:
```c
undefined4
Java_com_hellocmu_picoctf_FlagstaffHill_paprika(int *param_1,undefined4 param_2,undefined4 param_3)

{
  byte bVar1;
  undefined4 uVar2;
  char *local_48;
  
  uVar2 = (**(code **)(*param_1 + 0x2a4))(param_1,param_3,0);
  bVar1 = dill(uVar2);
  (**(code **)(*param_1 + 0x2a8))(param_1,param_3,uVar2);
  if ((bVar1 & 1) == 0) {
    local_48 = "try again";
  }
  else {
    local_48 = (char *)marjoram();
  }
  uVar2 = (**(code **)(*param_1 + 0x29c))(param_1,local_48);
  free(local_48);
  return uVar2;
}
```
  7) I honsetly cant explain some of the stuff thats happening, but the most important thing will be the if block. Ghidra also has some trouble since it tells me that `dill(uVar2)` will just always return 1, while the assembly looks very very weird:
```c
undefined4 dill(void)

{
  return 1;
}

```
  This would mean that the marjoram function is always called so there would be no need for an if block. Also the paprika function has 4 parameters while we only provide one in the java function.
  8) Anyway, the next logical step is to look at this marjoram function (I already renamed some stuff):
```c
void marjoram(void)

{
  undefined **ppuVar1;
  char *not_exist;
  size_t 8;
  undefined *data_segment;
  
  ppuVar1 = &__DT_PLTGOT;
  data_segment = &DAT_00011bd6;
  not_exist = strdup("notexist");
  8 = strlen("notexist");
  unscramble(data_segment,0x23,not_exist,8,not_exist,data_segment,ppuVar1);
  return;
}
```
  This already looks way clearer, some stuff is intialised and then called by "unscramble". This is very exciting since "unscramble usually means unscrambling the flag in ctf challenges".
  Note: data_segment is just 36 random hex chars.

  9) Opening the unscramble function we can see:
```c
void * unscramble(int data_segment,size_t 35,int notexist,int 8)

{
  void *pvVar1;
  int local_20;
  int i;
  
  pvVar1 = calloc(35,1);
  local_20 = 0;
  for (i = 0; i < (int)35; i = i + 1) {
    *(byte *)((int)pvVar1 + i) = *(byte *)(data_segment + i) ^ *(byte *)(notexist + local_20 % 8);
    local_20 = local_20 + 1;
  }
  return pvVar1;
}

```
  I  renamed the parameters here to what was supplied by the marjoram function. 
  This just seems like very standard xor encryption to me:
  - `pvVar1 = calloc(35,1)` -> allocate some space so we can put stuff here
  - `for (i = 0; i < (int)35; i = i + 1)` -> we're going to iterate 35 times
  - `*(byte *)((int)pvVar1 + i)` -> we're going to put byte (aka hex chars) in our empty space at index i (not putting anything in there yet, just declaring what is going to be here)
  - `*(byte *)(data_segment + i) ^ *(byte *)(notexist + local_20 % 8)` -> this is the stuff we're going to put in the empty space, in more detail:
      - `*(byte *)(data_segment + i)` -> take byte (hex value) of data_segment at position local20
      - `^ *(byte *)(notexist + local_20 % 8)` -> xor it with the character of "notexist" at index local_20%8 (bascically just go through all characters of "notexist" over and over again)
  - `local_20 = local_20 + 1` -> just add one to local_20, since local_20 was initialised to be 0 this is the same thing as it being i.


