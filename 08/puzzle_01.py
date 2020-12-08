import sys


def read_program(filename):
    with open(filename, "r", encoding="utf-8") as f:
        raw = f.read()
    
    prog = []
    
    for line in raw.split("\n"):
        inst, val = line.split(" ")
        prog.append(
            (inst, decode_number(val))
        )
    return prog
    

def decode_number(ns):
    if ns.startswith("+"):
        return int(ns[1:])
    elif ns.startswith("-"):
        return int(ns[1:]) * -1
    else:
        print("! Improperly encoded number [%s]" % (ns,))
        return 0
        

def run_until_loop(program):
    
    acc = 0
    pc = 0
    visited = set()
    
    while True:
        
        # loop break
        if pc in visited:
            break
        visited.add(pc)
        
        # inst decode
        inst, arg = program[pc]
        #print("%02d %s %d" % (pc, inst, arg))
        
        # NOP
        if inst == "nop":
            pc += 1
        
        # ACC
        elif inst == "acc":
            pc += 1
            acc += arg
        
        # JMP
        elif inst == "jmp":
            pc += arg
    
    return {
        "acc": acc,
        "loop_at": pc
    }


if __name__ == "__main__":
    program = read_program(sys.argv[-1])
    state = run_until_loop(program)
    print("Looped at instruction %(loop_at)d acc(%(acc)d)" % state)