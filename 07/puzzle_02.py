import sys
import json


def read_rules(filename):
    """
    Read the rules file and generate a dictionary with entries
    like:
        
        "light red": [{"color": "bright white", "qty": 1}, {"color": "muted yellow", "qty": 2}],
        ...
    """
    
    with open(filename, "r", encoding="utf-8") as f:
        raw = f.read()
    
    rules = {}
    
    for line in raw.split("\n"):
        if line.strip() == "":
            continue
            
        line = line.strip().rstrip(".")
        outer, inners_raw = line.split(" bags contain ")
        
        if outer not in rules:
            rules[outer] = []
        
        if inners_raw == "no other bags":
            continue
            
        # build better inners
        inners = [i.rstrip("s").replace(" bag", "") for i in inners_raw.split(", ")]
        
        for inner in inners:
            bits = inner.split(" ")
            qty = int(bits[0])
            clr = " ".join(bits[1:])
            rules[outer].append(
                {
                    "color": clr,
                    "qty": qty
                }
            )
    
    return rules


def count_bag_contents(rules, outer):
    """
    Recursively count our bag contents, making sure to carry the values of the inner bags
    when there are multiple
    """
    
    contents = rules[outer]
    
    # we count ourself
    count = 1
    
    for inner_bag in contents:
        qty = inner_bag["qty"]
        inner_count = count_bag_contents(rules, inner_bag["color"])
        count += (qty * inner_count)
    return count
    

if __name__ == "__main__":
    rules = read_rules(sys.argv[-1])
    search_color = "shiny gold"
    print("1 %s bag contains %d total bags" % (search_color, count_bag_contents(rules, search_color) - 1))