# CRACKME100 SOLUTION

## Steps to Solution

1. **Open the executable in Ghidra**

2. **Navigate to the `main` function**
   ![Schermafbeelding 2024-07-08 162257](https://github.com/HenriMertens/PICOGYM/assets/149707229/5c8ba64b-3cc6-465f-bedc-58b5179ddc72)

3. **Examine the initialized local variables**
   - Attempting to convert from hex to ASCII results in mumbo jumbo.
   ![mumbojumbo](https://github.com/HenriMertens/PICOGYM/assets/149707229/6fcd9ec6-75c6-47b4-9f4d-672f4dfcd819)

4. **Identify the input storage**
   - By examining the scanf function we can see that our input is stored in `locala8` and has the format `%50s` (50 characters).
     
    ![50s](https://github.com/HenriMertens/PICOGYM/assets/149707229/6bbc0820-e15f-44fa-ba5d-71d16031ed41)

   - Rename the variable for easier future reference.


5. **Analyze remaining code**
   - Observe a bunch of math stuff (aint reading all that).
   - Notice the `memcmp` function comparing the modified input against the initialized variable (from step 3).
     
   ![Schermafbeelding 2024-07-08 162527](https://github.com/HenriMertens/PICOGYM/assets/149707229/02147adf-eda5-4fb7-b7ca-05c2abed58a4)

   
### Intermediate Conclusion
- The encrypted password is initialized in the `main` function (mumbo_jumbo).
- Our input gets encrypted and is then compared against this encrypted password.
- If they match, a sample flag is printed.

### Solution
- I solved this using angr (see python script)
- Here you see the adresses we are trying to find/avoid.
   ![adresses](https://github.com/HenriMertens/PICOGYM/assets/149707229/ccc2f415-240e-4234-a2dd-ef126dd216b1)

- The rest is explained in the python script


  
