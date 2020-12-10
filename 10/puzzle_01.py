import sys
import json


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
    
    return lead


def diff_hist(nums):
    
    hist = {}
    
    for idx in range(len(nums) - 1):
        a = nums[idx]
        b = nums[idx + 1]
        diff = b - a
        if diff not in hist:
            hist[diff] = 0
        
        hist[diff] += 1
    
    return hist


if __name__ == "__main__":
    chain = build_chain(read_jolts(sys.argv[-1]))
    hist = diff_hist(chain)
    print(json.dumps(hist))
    print("chk: %d" % (hist[1] * hist[3],))