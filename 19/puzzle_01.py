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
        
        # I have alternations
        for inner_rule in rule_raw.strip().split(" | "):
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
    mat = []
    for msg in messages:
        if re.fullmatch(rule_regex, msg) is not None:
            mat.append(msg)
    return mat


if __name__ == "__main__":
    rules, messages = read_data(sys.argv[-1])
    filtered = filter_messages(messages, rules)
    print("%d messages match rule 0" % (len(filtered),))
    