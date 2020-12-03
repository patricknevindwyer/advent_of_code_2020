import sys

def is_valid_password(pwd_line):
    """
    Given a line of a password file, like:
    
        1-3 a: abcdef
    
    break it down and determine if the password meets the given criteria
    """
    
    # break apart our criteria and password
    r_crit, r_password = pwd_line.strip().split(":")
    
    # parse the criteria
    crit = parse_criteria(r_crit)
    
    # count letters in the password so we can analyse
    let_dict = {}
    for let in r_password.strip():
        if let not in let_dict:
            let_dict[let] = 0
        let_dict[let] += 1
    
    # analyze by our rules
    valid = True
    for crit_letter, crit_range in crit.items():
        
        # does the letter even exist?
        if crit_letter not in let_dict:
            valid = False
            break
        
        # does it meet our min/max requirements
        occurs = let_dict[crit_letter]
        if occurs < crit_range["min"] or occurs > crit_range["max"]:
            valid = False
            break
    
    return valid
    

def parse_criteria(crit):
    """
    Given a password criteria, parse it into a simple rule set by letter
    """
    occurs, letter = crit.split(" ")
    occ_min, occ_max = occurs.split("-")
    
    return {letter: {"min": int(occ_min), "max": int(occ_max)}}


if __name__ == "__main__":
    
    # gather up our passwords
    password_file = sys.argv[-1]
    with open(password_file, "r", encoding="utf-8") as pwd_file:
        password_lines = pwd_file.read().split("\n")
        
    # count valid passwords
    valid_count = 0
    for password_line in password_lines:
        if is_valid_password(password_line):
            valid_count += 1
    
    print("%d valid passwords" % (valid_count,))
    