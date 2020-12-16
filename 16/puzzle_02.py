import sys
import json


def read_tickets(filename):
    with open(filename, "r", encoding="utf-8") as f:
        raw = f.read()
    
    # split by double newlines
    rules, y_ticket, n_tickets = raw.split("\n\n")
    
    # parse the rules
    par_rules = []
    
    for line in rules.split("\n"):
        tag, rule_data = line.strip().split(": ")
        for rule_range in rule_data.split(" or "):
            lower, upper = rule_range.split("-")
            par_rules.append(
                {
                    "tag": tag,
                    "lower": int(lower),
                    "upper": int(upper)
                }
            )
    
    # parse my ticket
    your_ticket = [int(y) for y in y_ticket.split("\n")[1].split(",")]
    
    # parse the nearby tickets
    nearby_tickets = []
    for n_ticket_raw in n_tickets.split("\n")[1:]:
        nearby_tickets.append(
            [int(n) for n in n_ticket_raw.split(",")]
        )
    
    return {
        "rules": par_rules,
        "ticket": your_ticket,
        "nearby": nearby_tickets
    }


def is_valid_ticket(rules, ticket):

    for field in ticket:
        valid = False
        for rule in rules:
            if field >= rule["lower"] and field <= rule["upper"]:
                valid = True
                break
        if not valid:
            return False
    return True


def does_rule_match(rule, value):
    return value >= rule["lower"] and value <= rule["upper"]


def do_rules_match(rules, value):   
    for rule in rules:
        if does_rule_match(rule, value):
            return True
    return False
    

def valid_rule_tags_for_field(rules, tickets, field_idx):
    
    # compact our rule set by rule tag
    rules_by_tag = {}
    for rule in rules:
        if rule["tag"] not in rules_by_tag:
            rules_by_tag[rule["tag"]] = []
        rules_by_tag[rule["tag"]].append(rule)
        
    # collect which rule tags are valid for the given values
    values = [t[field_idx] for t in tickets]
    valid_rule_tag = []
    
    for tag, tag_rules in rules_by_tag.items():
        negates = [v for v in values if not do_rules_match(tag_rules, v)]
        if len(negates) == 0:
            valid_rule_tag.append(tag)
    
    return list(set(valid_rule_tag))


def is_constraint_stable(field_to_tag):
    for _field_idx, tags in field_to_tag.items():
        if len(tags) > 1:
            return False
    return True


def constrain(field_to_tag):
    # find any field/tag mappings that have only one value, and remove those from all others
    singlets = []
    for _field_idx, tags in field_to_tag.items():
        if len(tags) == 1:
            singlets.append(tags[0])
    singlets = set(singlets)
    
    # rebuild/remove
    rebuilt = {}
    
    for field_idx, tags in field_to_tag.items():
        if len(tags) == 1:
            rebuilt[field_idx] = tags
        else:
            rebuilt[field_idx] = [t for t in tags if t not in singlets]
    return rebuilt

if __name__ == "__main__":
    ticket_data = read_tickets(sys.argv[-1])
    
    # setup our nearby tickets that make sense
    valid_tickets = [t for t in ticket_data["nearby"] if is_valid_ticket(ticket_data["rules"], t)]
    print("valid tickets:")
    for t in valid_tickets:
        print(t)
    
    field_to_tag = {}
    
    # let's try and map out likely field tags as a first stage
    for field_idx in range(len(valid_tickets[0])):
        
        field_to_tag[field_idx] = valid_rule_tags_for_field(ticket_data["rules"], valid_tickets, field_idx)
    
    # now apply constraints until we have a secured rule set
    while not is_constraint_stable(field_to_tag):
        field_to_tag = constrain(field_to_tag)
    
    # extract the fields that start with departure
    d_indices = []
    for idx in range(len(field_to_tag)):
        print("idx(%03d) : %s" % (idx, field_to_tag[idx][0]))
        if field_to_tag[idx][0].startswith("departure"):
            d_indices.append(idx)
    
    carry = 1
    for idx in d_indices:
        carry *= ticket_data["ticket"][idx]
    print("chksum: %d" % (carry,))
    