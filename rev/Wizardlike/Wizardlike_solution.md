# WIZARDLIKE SOLUTION

## Steps to Explore and Modify the Game

1. **Run the game:**
   - Execute the game using `./game` and explore the first level.
   - Notice something on the other side of the wall in the first level. If only we could get there, hmmmm.
   ![start](https://github.com/HenriMertens/PICOGYM/assets/149707229/9c95f96c-acee-4465-804e-6dae7995650a)

2. **Open the game file in Ghidra:**
   - Use Ghidra to decompile and analyze the game file.

3. **Navigate to the main function:**
   - Find the main function in the decompiled code (I already renamed the functions).
   ![main](https://github.com/HenriMertens/PICOGYM/assets/149707229/c0143b37-4e21-4cd3-9a5a-8407476c0152)

4. **Contemplate life decisions:**

5. **Analyze the initial functions:**
   - The first function you encounter uses weird input that looks like part of the map.
   - Upon analyzing the function, we notice a big array is being set (100x100), likely creating the map.
     ![cerate](https://github.com/HenriMertens/PICOGYM/assets/149707229/f8b5dbab-36ab-4e19-8b4a-91699fd219fd)

   - The second function sets this big array to 0, probably clearing the map.
     ![clear](https://github.com/HenriMertens/PICOGYM/assets/149707229/cfc012c8-ae4f-497a-a5bd-b6c60de489a9)

   - The third function performs some black magic and can be safely ignored.
   
6. **Identify and modify the level comparison:**
   - Notice that `DAT_00533f7c` is compared to numbers 1-10, likely representing the level number.
     ![levels](https://github.com/HenriMertens/PICOGYM/assets/149707229/177445e1-643c-49e3-94c1-e57005dbb2a0)

   - Find some more black magic math stuff (we can safely ignore, probably not important anyways)
   - Further we find that `ivar5` is compared to "w", "a", "s", "d", "q", probably storing input (I changed these already to azerty lay out, since I use azerty keyboard).
     
     ![ivar5](https://github.com/HenriMertens/PICOGYM/assets/149707229/2cbb53cd-45eb-4905-80d0-06eddf944fe2)

   - Follow the function after the input is compared. Maybe we can do something with how the players moves, to go through walls (I already renamed the function)
     
     ![move](https://github.com/HenriMertens/PICOGYM/assets/149707229/fa1234fc-d5dc-4d43-88df-bad59ce9d665)

   - Find that the function does some math with stuff stored in DAT_ (this probably moves the player) BUT ONLY IF cVar1 !=0.
     
   - Trace the function that sets the value for `cVar1` and see it compares " " and "#", checking if you're moving through a wall or across a gap (I already modified the compare see below).
   ![bounds](https://github.com/HenriMertens/PICOGYM/assets/149707229/32bd7865-4e23-49ae-b63d-c125b01d87c5)

7. **Hexedit the comparison functions:**
   - Change the compare functions to values not encountered (e.g., "%") to allow movement through walls.
   ![patch](https://github.com/HenriMertens/PICOGYM/assets/149707229/ce8f3fda-e085-4114-9930-3e8191a78de6)

8. **Export the modified program:**
   - Export the modified program with the format set to "original file".
   ![export](https://github.com/HenriMertens/PICOGYM/assets/149707229/5d7fc1f4-c2f3-47d2-aed8-a55d59e07441)
   ![export2](https://github.com/HenriMertens/PICOGYM/assets/149707229/62e210fc-9f7f-414f-ae23-c46d50c11dab)

9. **Run the modified program:**
   - Execute the modified game and verify that you can move through walls.
   - Notice part of the flag on the other side.
   ![end](https://github.com/HenriMertens/PICOGYM/assets/149707229/26d82530-bb6f-435d-a225-a7ddd5096215)

10. **Find and construct the flag:**
    - Locate parts of the flag in each level (this can be annoying) and piece together the final flag.


    
