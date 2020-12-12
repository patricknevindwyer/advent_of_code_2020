import sys


def read_inst(filename):
    with open(filename, "r", encoding="utf-8") as f:
        raw = f.read()
    
    insts = []
    
    for line in raw.split("\n"):
        inst = line[0]
        amt = int(line.strip()[1:])
        insts.append({"instruction": inst, "amount": amt})
    
    return insts


def navigate(insts, heading=None, x=0, y=0):
    
    for inst in insts:
        amt = inst["amount"]
        if inst["instruction"] == "N":
            y += amt
        elif inst["instruction"] == "S":
            y -= amt
        elif inst["instruction"] == "E":
            x += amt
        elif inst["instruction"] == "W":
            x -= amt
        elif inst["instruction"] == "R":
            r_change = {"N": "E", "S": "W", "E": "S", "W": "N"}
            
            while amt > 0:
                amt -= 90
                heading = r_change[heading]
        elif inst["instruction"] == "L":
            l_change = {"N": "W", "S": "E", "E": "N", "W": "S"}
            
            while amt > 0:
                amt -= 90
                heading = l_change[heading]
        elif inst["instruction"] == "F":
            if heading == "N":
                y += amt
            elif heading == "S":
                y -= amt
            elif heading == "E":
                x += amt
            elif heading == "W":
                x -= amt
    
    return x, y


if __name__ == "__main__":
    insts = read_inst(sys.argv[-1])
    nx, ny = navigate(insts, heading="E", x=0, y=0)
    print("Distance from start: %d" % (abs(nx) + abs(ny),))