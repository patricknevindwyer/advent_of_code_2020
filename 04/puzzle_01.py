import sys


def load_passports(filename):
    """
    Parse the passport batch file, return a list of dicts
    """
    with open(filename, "r", encoding="utf-8") as f:
        raw = f.read()
    
    
    passports = []
    current = {}
    
    for line in raw.split("\n"):
        
        # pop a completed entry
        if line.strip() == "":
            passports.append(current)
            current = {}
            continue
        
        # parse the line
        for entry in line.split(" "):
            k,v = entry.strip().split(":")
            current[k.strip()] = v.strip()
    
    if len(current.keys()) > 0:
        passports.append(current)
    
    return passports


def is_valid(passport):
    req_fields = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]
    mapping = set([req_field in passport for req_field in req_fields])
    return False not in mapping
    

if __name__ == "__main__":
    passports = load_passports(sys.argv[-1])
    valid_passports = [p for p in passports if is_valid(p)]
    print("%d valid" % (len(valid_passports),))