import sys
import itertools


def read_mmap(filename):
    with open(filename, "r", encoding="utf-8") as f:
        raw = f.read()
    
    insts = []
    
    for line in raw.split("\n"):
        if line.startswith("mem"):
            bits = line.split(" = ")
            addr = bits[0].replace("mem[", "").replace("]", "")
            dec = int(bits[1].strip())
            
            # write instruction
            insts.append(("write", addr, dec))
            
        elif line.startswith("mask"):
            insts.append(("mask", "", line.split(" = ")[1].strip()))
    
    return insts


def process_memory(insts):
    mem = {}
    mask = "X" * 36
    
    for op, dst, value in insts:
        
        if op == "mask":
            mask = value
        elif op == "write":
            
            # find all addresses to write our value
            for addr in apply_mask(dst, mask):
                mem[addr] = value
    
    return mem


def apply_mask(value, mask):
    """
    Yield the memory address variations
    """
    
    # convert the value to binary and extract digits
    b_value = bin(int(value))[2:]
    
    # grab the lists of values and reverse them
    b_value_rev = [c for c in b_value]
    b_value_rev.reverse()
    
    m_value_rev = [c for c in mask]
    m_value_rev.reverse()
    
    # build out our new masking
    masked_rev = []
    
    for idx in range(len(m_value_rev)):
        
        if m_value_rev[idx] == "0":
            # unchanged - use original
            if idx < len(b_value_rev):
                masked_rev.append(b_value_rev[idx])
            else:
                masked_rev.append("0")
        
        elif m_value_rev[idx] == "1":
            masked_rev.append("1")
        
        elif m_value_rev[idx] == "X":
            masked_rev.append("X")
            
    
    masked_rev.reverse()
    
    # now find any X entries, and we need all variations of 1/0 for these
    x_indices = []
    for idx in range(len(masked_rev)):
        if masked_rev[idx] == "X":
            x_indices.append(idx)
            
    for replacement in itertools.product("01", repeat=len(x_indices)):
        rep = list(replacement)
        for idx in range(len(x_indices)):
            masked_rev[x_indices[idx]] = replacement[idx]
        yield int("0b" + "".join(masked_rev), 2)
    

if __name__ == "__main__":
    
    insts = read_mmap(sys.argv[-1])
    mem = process_memory(insts)
    print(mem)
    print(sum(mem.values()))