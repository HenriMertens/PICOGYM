
import angr
import logging
logging.getLogger('angr').setLevel(logging.INFO) #Not needed just for more info
import claripy

# all printable characters
printable = (
       " !\"#$%&@'()*+,-./0123456789:;<=>?ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~"
    )

# using normal printable characters gave weird results so I removed unlikely characters
printable_changed = (
       " !+,-0123456789:;<=>?ABCDEFGHIJKLMNOPQRSTUVWXYZ_abcdefghijklmnopqrstuvwxyz"
    )

# Also not entirely neccessary
# Creates functions that will interrupt the programm an give us Ipython interfaces to work with the variables
def hook(l=None):
    if l:
        locals().update(l)
    import IPython
    IPython.embed(banner1='', confirm_exit=False)
    exit(0)

# Adresses from ghidra
# Angr by default uses 0x4000000 offset so make sure it starts with that

# Print sample falg adress
FIND = 0x401382

# Print FAILED!adress
AVOID = 0x40138e

# Amount of bytes for our input -> ATLEAST 50 (ghidra), more also works from my testing
LENGTH = 50

# Create input for angr, convert bytes to bits
user_data = claripy.BVS("user_data", LENGTH*8)

# Start project with path to executable file
p = angr.Project("/home/kali/pico/rev/crackme100")

# Create entry state -> use the input created above
# Unicorn options make angr go brr (not neccessary)
entry = p.factory.entry_state(stdin = user_data, add_options = angr.options.unicorn)

# Add constraint that each byte is in "printable_changed"
for i in range(LENGTH):
    entry.solver.add(
        claripy.Or(*(
        user_data.get_byte(i) == x
        for x in printable_changed

        ))
    )


# Start sim manager
sm = p.factory.simgr(entry)

# Tell simmanger to find our print flag adress
sm.explore(find= FIND, avoid= AVOID)

# Print the input angr gave the programm to get to the found adress
for s in sm.found:
       print(s.posix.stdin.concretize())

# allows us to examine the simulation states in ipython, not really needed, because we print the flag in the line above but helpfull for debugging
hook(locals())
