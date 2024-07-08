# CRACKME100 SOLUTION

## Steps to Solution

1. **Open the executable in Ghidra**

2. **Navigate to the `main` function**

3. **Examine the initialized local variables**
   - Attempting to convert from hex to ASCII results in mumbo jumbo.

4. **Identify the input storage**
   - Our input is stored in `locala8` and has the format `%50s` (50 characters).
   - Rename the variable for easier future reference.

5. **Analyze the code**
   - Observe a series of mathematical operations modifying our input (aint reading all that).
   - Notice the `memcmp` function comparing the modified input against the initialized variable (from step 3).

### Intermediate Conclusion
- The encrypted password is initialized in the `main` function.
- Our input gets encrypted and is then compared against this encrypted password.
- If they match, a sample flag is printed.
