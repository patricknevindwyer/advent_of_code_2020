import sys


def read_equations(filename):
    with open(filename, "r", encoding="utf-8") as f:
        raw = f.read()
    
    return raw.split("\n")


def parse_equation(eq):
    """
    Parse an equation like:
        
        5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))
    
    into tokens
    """
    tokens = []
    carry = []
    
    for c in eq:
        
        # grab numbers
        if c in "1234567890":
            carry.append(c)
            continue
        
        # do we have a carry?
        if len(carry) > 0:
            tokens.append(int("".join(carry)))
            carry = []
        
        if c == " ":
            continue
        else:
            tokens.append(c)
    if len(carry) > 0:
        tokens.append(int("".join(carry)))
        
    return tokens


def eval_equation(eq):
    
    # reduce the equation form
    if reducable(eq):
        eq = reduce_equation(eq)
    
    # now solve - but we're first looking for order of operations. + highest, * lowest
    while "+" in eq:
        
        # find an addition op
        pivot = eq.index("+")
        left = pivot - 1
        right = pivot + 1
        
        inserted = eq[left] + eq[right]
        eq[left:right + 1] = [inserted]
        
    # standard reduce for multiplication
    carry = eq[0]
    
    for idx in range(1, len(eq), 2):
        op = eq[idx]
        right = eq[idx + 1]
        carry *= right
    return carry


def reducable(eq):
    return "(" in eq
    

def reduce_equation(eq):
    """
    find the next parenthetical, and reduce it through eval_equation
    """
    # print("in reduce: ", eq)
    
    while reducable(eq):
        
        # parenthesis reduction
        st_idx = eq.index("(")
        ed_idx = None
        p_count = 1
        for idx in range(st_idx + 1, len(eq)):
            tok = eq[idx]
            if tok == "(":
                p_count += 1
            elif tok == ")":
                p_count -= 1
                if p_count == 0:
                    ed_idx = idx
                    break
    
        # the st_idx : (ed_idx + 1) can be reduced, solve it, and then send back tokens
        red = eval_equation(eq[st_idx + 1:ed_idx])
        eq = eq[:st_idx] + [red] + eq[ed_idx + 1:]
        # print("  reduced: ", eq)
    
    return eq
        
    


if __name__ == "__main__":
    eqs = read_equations(sys.argv[-1])
    outs = []
    for eq in eqs:
        print("eq: %s" % (eq,))
        v = eval_equation(parse_equation(eq))
        outs.append(v)
        print("   = %d" % (v,))
    print("chk: %d" % (sum(outs),))