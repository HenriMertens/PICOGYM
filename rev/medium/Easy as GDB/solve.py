
import angr
import logging


logging.getLogger('angr').setLevel(logging.INFO) #Not needed just for more info



#debugging purposes
def hook(l=None):
    if l:
        locals().update(l)
    import IPython
    IPython.embed(banner1='', confirm_exit=False)
    exit(0)

#Adress that prints "correct" in ghidra was 0x10a72 -> since ghidra uses 0x10000 offset, the print adress is at 'a72'.
#angr uses 0x400000 offset -> print "correct adress is at 0x400a72
FIND = 0x400a72
AVOID = 0x400a86

p = angr.Project("/home/kali/pico/rev/brute")


entry = p.factory.entry_state(add_options = angr.options.unicorn)



sm = p.factory.simgr(entry)


sm.explore(find=FIND, avoid = AVOID)


hook(locals())
