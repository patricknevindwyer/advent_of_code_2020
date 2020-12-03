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
    
    # test the passwords
    valid = False
    password = " " + r_password.strip()
    for crit_let, crit_points in crit.items():
        
        # test the given positions in the password
        pl = crit_points["l"]
        pr = crit_points["r"]
        let_l = password[pl]
        let_r = password[pr]
        
        if let_l == crit_let and let_r != crit_let:
            valid = True
        elif let_l != crit_let and let_r == crit_let:
            valid = True
            
    return valid
    

def parse_criteria(crit):
    """
    Given a password criteria, parse it into a simple rule set by letter
    """
    occurs, letter = crit.split(" ")
    occ_min, occ_max = occurs.split("-")
    
    return {letter: {"l": int(occ_min), "r": int(occ_max)}}


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
    