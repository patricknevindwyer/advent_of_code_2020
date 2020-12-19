import sys
import re


def read_data(filename):
    
    with open(filename, "r", encoding="utf-8") as f:
        raw = f.read()
    
    # break out rules and messages
    rules = {}
    messages = []
    
    for line in raw.split("\n"):
        
        if ":" in line:
            idx, rule = line.split(": ")
            rules[int(idx)] = rule
        elif line.strip() == "":
            continue
        else:
            messages.append(line.strip())
    
    return rules, messages


def construct_rule_regex(rules, idx=0):
    
    # start with our rule base, we're going to recursively drop in
    rule_raw = rules[idx]
    
    if "\"" in rule_raw:
        
        # I'm a literal        
        return rule_raw.replace("\"", "")
        
    elif "|" in rule_raw:
        
        alts = []
        
        if idx == 8:
            # we're looking at our first rule doing +
            bits = []
            b_j = construct_rule_regex(rules, 42)
            return "%s+" % (b_j,)
            
        elif idx == 11:
            
            bits = []
            b_j = construct_rule_regex(rules, 42)
            b_k = construct_rule_regex(rules, 31)
            
            return "%s{x}%s{x}" % (b_j, b_k)

        else:
            # I have alternations
            for inner_rule in rule_raw.strip().split(" | "):
            
                # let's check if one of our rule bits is ourself, inducing a loop, in
                # which case we'll mark them as a multiple iteration of the previous
                # entry
            
                rule_bits = []
        
                # run the inner alternation pieces
                for r_idx in inner_rule.strip().split(" "):
                    rule_bits.append(construct_rule_regex(rules, int(r_idx)))
        
                alts.append("".join(rule_bits))
        
        return "(%s)" % ("|".join(alts),)
    else:

        rule_bits = []
        
        # I'm a straight up rule pattern
        for r_idx in rule_raw.strip().split(" "):
            rule_bits.append(construct_rule_regex(rules, int(r_idx)))
        
        return "".join(rule_bits)


def filter_messages(messages, rules):
    rule_regex = construct_rule_regex(rules)
    print("rule: <%s>" % (rule_regex,))
    
    # get a first pass matching with 1 repetition
    cnt = match_count(messages, rule_regex, 1)
    
    prv_cnt = 0
    rep = 2
    
    while prv_cnt != cnt:
        prv_cnt = cnt
        cnt += match_count(messages, rule_regex, rep)
        rep += 1
    
    return cnt
    

def match_count(messages, rule_regex, reps):
    mat = 0
    rr = rule_regex.replace("x", str(reps))
    for msg in messages:
        if re.fullmatch(rr, msg):
            mat += 1
    return mat
    
    
if __name__ == "__main__":
    rules, messages = read_data(sys.argv[-1])
    filtered = filter_messages(messages, rules)
    print("%d messages match rule 0" % (filtered,))
    