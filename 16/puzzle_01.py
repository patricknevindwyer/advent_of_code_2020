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


def find_invalid_fields(rules, nearby):
    invalids = []
    
    for ticket in nearby:
        for field in ticket:
            valid = False
            for rule in rules:
                if field >= rule["lower"] and field <= rule["upper"]:
                    valid = True
                    break
            
            if not valid:
                invalids.append(field)
    
    return invalids
    

if __name__ == "__main__":
    ticket_data = read_tickets(sys.argv[-1])
    invalid_fields = find_invalid_fields(ticket_data["rules"], ticket_data["nearby"])
    print(invalid_fields)
    print(sum(invalid_fields))