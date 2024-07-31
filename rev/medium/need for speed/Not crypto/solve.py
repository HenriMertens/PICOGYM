

import angr

#gives more info not actually needed
import logging
logging.getLogger('angr').setLevel(logging.INFO)

import claripy

#good for debugging but can be lef out
def hook(l=None):
    if l:
        locals().update(l)
    import IPython
    IPython.embed(banner1='', confirm_exit=False)
    exit(0)


p = angr.Project("/home/kali/pico/rev/not-crypto")

entry = p.factory.entry_state()

sm = p.factory.simgr()

#find adress using ghidra -> angr uses ofset 0x4000000 by default so change the 1 in ghidra to 4 for angr (0x101aac -> 0x401aac)
AVOID = 0x401aac

FIND = 0x4013d0

sm.explore(find = FIND, avoid = AVOID)

# print the required input to get to the found adress
print(sm.found[0].posix.stdin.concretize())

#Call hook for debugging
hook(locals())

