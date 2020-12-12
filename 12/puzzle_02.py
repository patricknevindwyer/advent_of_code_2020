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


def navigate(insts, x=0, y=0, wx=0, wy=0):
    
    # track the way point and the ship location
    
    for inst in insts:
        amt = inst["amount"]
        if inst["instruction"] == "N":
            wy += amt
        elif inst["instruction"] == "S":
            wy -= amt
        elif inst["instruction"] == "E":
            wx += amt
        elif inst["instruction"] == "W":
            wx -= amt
        elif inst["instruction"] == "R":
            
            # rotate the way point so on each rotation x becomes y, y becomes x, but we need to
            # do a sign swap as well.
            # pos x to neg y
            # pos y to pos x
            # neg x to pos y
            # neg y to neg x
            while amt > 0:
                old_x = wx
                old_y = wy
                
                if old_x > 0:
                    wy = -1 * old_x
                elif old_x < 0:
                    wy = -1 * old_x
                else:
                    wy = old_x
                
                if old_y > 0:
                    wx = old_y
                elif old_y < 0:
                    wx = old_y
                else:
                    wx = old_x
                    
                amt -= 90

        elif inst["instruction"] == "L":
            
            # rotate the way point so on each rotation x becomes y, y becomes x, but we need to
            # do a sign swap as well.
            # pos x to pos y
            # pos y to neg x
            # neg x to neg y
            # neg y to pos x
            while amt > 0:
                old_x = wx
                old_y = wy
                
                if old_x > 0:
                    wy = old_x
                elif old_x < 0:
                    wy = old_x
                else:
                    wy = old_x
                
                if old_y > 0:
                    wx = -1 * old_y
                elif old_y < 0:
                    wx = -1 * old_y
                else:
                    wx = old_x
                    
                amt -= 90

        elif inst["instruction"] == "F":
            
            # move towards the waypoint
            y += (wy * amt)
            x += (wx * amt)
    
    return x, y


if __name__ == "__main__":
    insts = read_inst(sys.argv[-1])
    nx, ny = navigate(insts, x=0, y=0, wx=10, wy=1)
    print("Distance from start: %d" % (abs(nx) + abs(ny),))