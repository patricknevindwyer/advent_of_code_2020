import sys


def read_inputs(filename, preamble=25):
    all_nums = []
    
    with open(filename, "r", encoding="utf-8") as f:
        raw = f.read()
    
    for line in raw.split("\n"):
        if line.strip() != "":
            all_nums.append(int(line.strip()))
    
    pre = all_nums[:preamble]
    pos = all_nums[preamble:]
    return pre, pos


def first_error(preamble, inputs):
    
    while len(inputs) > 0:
        # get our next input
        candidate = inputs.pop(0)
        
        if has_sum(preamble, candidate):
            preamble.append(candidate)
            preamble = preamble[1:]
        else:
            return candidate
    return None


def has_sum(current, val):
    for idx_a in range(len(current) - 1):
        for idx_b in range(idx_a + 1, len(current)):
            if current[idx_a] + current[idx_b] == val:
                return True
    return False
    

if __name__ == "__main__":
    preamble_size = 25
    filename = None
    
    if len(sys.argv) > 2:
        # filename.dat preamble_size
        preamble_size = int(sys.argv[-1])
        filename = sys.argv[-2]
    else:
        filename = sys.argv[-1]
    
    preamble, inputs = read_inputs(filename, preamble=preamble_size)
    error_term = first_error(preamble, inputs)
    print("Error term is [%d] with preamble size [%d]" % (error_term, preamble_size))