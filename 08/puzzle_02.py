import sys
import copy


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
        

def run_until_term(program):
    
    acc = 0
    pc = 0
    visited = set()
    term_by = None
    
    while True:
        
        # loop break
        if pc in visited:
            term_by == "loop"
            break
        visited.add(pc)
        
        # jump past end
        if pc >= len(program):
            term_by = "overflow"
            break
            
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
        "term_at": pc,
        "term_by": term_by
    }


def mutate_program(program):
    """
    Find all NOP or JMP instructions and flip to the opposite, yielding
    the mutated program
    """
    for inst_idx in range(len(program)):
        inst = program[inst_idx][0]
        arg = program[inst_idx][1]
        
        if inst == "jmp":
            prog_copy = copy.deepcopy(program)
            prog_copy[inst_idx] = ("nop", arg)
            yield prog_copy
        elif inst == "nop":
            prog_copy = copy.deepcopy(program)
            prog_copy[inst_idx] = ("jmp", arg)
            yield prog_copy

if __name__ == "__main__":
    program = read_program(sys.argv[-1])
    
    for mutation in mutate_program(program):
        state = run_until_term(mutation)
        if state["term_by"] == "overflow":
            print("Overflow acc == %d" % (state["acc"],))
