import sys
import json
from functools import lru_cache


def read_jolts(filename):
    with open(filename, "r", encoding="utf-8") as f:
        raw = f.read()
    
    nums = []
    
    for line in raw.split("\n"):
        nums.append(int(line.strip()))
    
    return nums


def build_chain(nums):
    
    lead = [0] + sorted(nums)
    lead.append(max(lead) + 3)
    
    return tuple(lead)


@lru_cache
def count_variations(t_chain):
    chain = list(t_chain)
    
    if len(chain) == 1:
        return 1
    else:
        
        # what other ways can we split from our lead
        root = chain[0]
        counts = 0
        
        for idx_up in range(1, 4):
            
            # short circuit
            if idx_up >= len(chain):
                continue
                
            # grab item
            candidate = chain[idx_up]
            if (candidate - root) <= 3:
                counts = counts + count_variations(tuple(chain[idx_up:]))
            else:
                break
        return counts
        

if __name__ == "__main__":
    chain = build_chain(read_jolts(sys.argv[-1]))
    print(chain)
    variants = count_variations(chain)
    print("chk: %d" % (variants))