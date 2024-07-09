# WIZARDLIKE SOLUTION

## Steps to Explore and Modify the Game

1. **Run the game:**
   - Execute the game using `./game` and explore the first level.
   - Notice something on the other side of the wall in the first level. If only we could get there, hmmmm.

2. **Open the game file in Ghidra:**
   - Use Ghidra to decompile and analyze the game file.

3. **Navigate to the main function:**
   - Find the main function in the decompiled code.

4. **Contemplate life decisions:**

5. **Analyze the initial functions:**
   - The first function you encounter uses weird input that looks like part of the map.
   - Upon analyzing the function, we notice a big array is being set (100x100), likely creating the map.
   - The second function sets this big array to 0, probably clearing the map.
   - The third function performs some black magic and can be safely ignored.

6. **Identify and modify the level comparison:**
   - Notice that `DAT_00533f7c` is compared to numbers 1-10, likely representing the level number.
   - Find some more black magic math stuff (we can safely ignore, probably no important anyways)
   - Further we find that `ivar5` is compared to "w", "a", "s", "d", "q", probably storing input.
   - Follow the function after the input is compared (maybe we can do something with how the players moves, to go through walls)
   - Find that the function does some math with stuff stored in DAT_ (this probably moves the player) BUT ONLY IF cVar1 !=0.
   - Trace the function that sets the value for `cVar1` and see it compares " " and "#", checking if you're moving through a wall or across a gap.

7. **Hexedit the comparison functions:**
   - Change the compare functions to values not encountered (e.g., "%") to allow movement through walls.

8. **Export the modified program:**
   - Export the modified program with the format set to "original file".

9. **Run the modified program:**
   - Execute the modified game and verify that you can move through walls.
   - Notice part of the flag on the other side.

10. **Find and construct the flag:**
    - Locate parts of the flag in each level (this can be annoying) and piece together the final flag.


    
