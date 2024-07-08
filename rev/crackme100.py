import angr
import logging
logging.getLogger('angr').setLevel(logging.INFO)
import claripy

printable = (
       " !\"#$%&@'()*+,-./0123456789:;<=>?ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~"
    )
    
printable_changed = (
       " !+,-0123456789:;<=>?ABCDEFGHIJKLMNOPQRSTUVWXYZ_abcdefghijklmnopqrstuvwxyz"
    )


def hook(l=None):
    if l:
        locals().update(l)
    import IPython
    IPython.embed(banner1='', confirm_exit=False)
    exit(0)


FIND = 0x401382
AVOID = 0x40138e

LENGTH = 50

user_data = claripy.BVS("user_data", LENGTH*8)


p = angr.Project("/home/kali/pico/rev/crackme100")

entry = p.factory.entry_state(stdin = user_data, add_options = angr.options.unicorn)

for i in range(LENGTH):
    entry.solver.add(
        claripy.Or(*(
        user_data.get_byte(i) == x
        for x in printable_changed

        ))
    )



sm = p.factory.simgr(entry)

sm.explore(find= FIND, avoid= AVOID)

hook(locals())
