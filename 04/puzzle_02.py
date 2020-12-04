import sys
import re


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
    """
    Extended validation
    """
    
    # Run our basic validation first - required fields
    req_fields = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]
    mapping = set([req_field in passport for req_field in req_fields])
    
    if False in mapping:
        return False
        
    # field based validation
    
    # byr
    byr = int(passport["byr"])
    if byr < 1920 or byr > 2002:
        return False
        
    # iyr
    iyr = int(passport["iyr"])
    if iyr < 2010 or iyr > 2020:
        return False
    
    # eyr
    eyr = int(passport["eyr"])
    if eyr < 2020 or eyr > 2030:
        return False
    
    # hgt
    hgt = passport["hgt"]
    if hgt.endswith("cm"):
        hgt_cm = int(hgt.replace("cm", ""))
        if hgt_cm < 150 or hgt_cm > 193:
            return False
    elif hgt.endswith("in"):
        hgt_in = int(hgt.replace("in", ""))
        if hgt_in < 59 or hgt_in > 76:
            return False
    else:
        return False
    
    # hcl
    hcl_match = re.match(r'^#[a-fA-F0-9]{6}$', passport["hcl"])
    if hcl_match is None:
        return False
    
    # ecl
    valid_ecl = set(["amb", "blu", "brn", "gry", "grn", "hzl", "oth"])
    if passport["ecl"] not in valid_ecl:
        return False
    
    # pid
    pid_match = re.match(r'^[0-9]{9}$', passport["pid"])
    if pid_match is None:
        return False
        
    return True
    

if __name__ == "__main__":
    passports = load_passports(sys.argv[-1])
    valid_passports = [p for p in passports if is_valid(p)]
    print("%d valid" % (len(valid_passports),))