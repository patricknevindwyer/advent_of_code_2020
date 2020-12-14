import sys


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
            
            # update the value with the mask
            w_value = apply_mask(value, mask)
            
            # write
            mem[dst] = w_value
    
    return mem


def apply_mask(value, mask):
    
    # convert the value to binary and extract digits
    b_value = bin(value)[2:]
    
    # grab the lists of values and reverse them
    b_value_rev = [c for c in b_value]
    b_value_rev.reverse()
    
    m_value_rev = [c for c in mask]
    m_value_rev.reverse()
    
    # build out our new masking
    masked_rev = []
    
    for idx in range(len(m_value_rev)):
        if m_value_rev[idx] != "X":
            masked_rev.append(m_value_rev[idx])
        else:
            if idx < len(b_value_rev):
                masked_rev.append(b_value_rev[idx])
            else:
                masked_rev.append("0")
    
    masked_rev.reverse()
    masked = "0b" + "".join(masked_rev)
    return int(masked, 2)


if __name__ == "__main__":
    
    insts = read_mmap(sys.argv[-1])
    mem = process_memory(insts)
    print(mem)
    print(sum(mem.values()))