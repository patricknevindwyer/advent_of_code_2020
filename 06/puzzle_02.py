import sys
import json


def read_surveys(filename):
    with open(filename, "r", encoding="utf-8") as f:
        raw = f.read()
    
    # break out answeres by line into keys, track for the overall groups
    groups = []
    group = {}
    group_size = 0
    
    for line in raw.split("\n"):
        
        # group is done
        if line.strip() == "":
            group["group_size"] = group_size
            group_size = 0
            groups.append(group)
            group = {}
            continue
        
        # parse line and add answers
        group_size += 1
        for q in line.strip():
            if q not in group:
                group[q] = 0
            group[q] += 1
            
    
    # pick up trailing group
    if len(group) > 0:
        group["group_size"] = group_size
        groups.append(group)
    
    return groups


def count_sums(groups):
    s = 0
    
    for group in groups:
        
        g_size = group["group_size"]
        for k, count in group.items():
            if k == "group_size":
                continue
            
            if count == g_size:
                s += 1
    
    return s


if __name__ == "__main__":
    groups = read_surveys(sys.argv[-1])
    sums = count_sums(groups)
    print("%d groups, survey sum is %d" % (len(groups), sums))
