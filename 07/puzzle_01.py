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


def does_bag_contain(rules, outer, inner):
    """
    Search the bag stack until we run out of options, looking for the particular bag
    """
    b_stack = [outer]
    
    while len(b_stack) > 0:
        search_bag = b_stack.pop(0)    
        bag_contents = rules[search_bag]
        
        # does this back contents contain our target bag? add the contents to the stack
        for inner_bag in bag_contents:
            if inner_bag["color"] == inner:
                return True
            else:
                b_stack.append(inner_bag["color"])
    return False
    

def count_bags_containing(rules, color):
    """
    Build out our search stack, and start counting
    """
    root_colors = rules.keys()
    
    return sum([1 for root in root_colors if does_bag_contain(rules, root, color)])


if __name__ == "__main__":
    rules = read_rules(sys.argv[-1])
    search_color = "shiny gold"
    print("%d bags can contain %s" % (count_bags_containing(rules, search_color), search_color))