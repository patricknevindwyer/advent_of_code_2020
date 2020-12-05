import sys


def read_pass(filename):
    with open(filename, "r", encoding="utf-8") as f:
        raw = f.read()
    
    cards = []
    
    for card in raw.split("\n"):
        row = card[:7]
        col = card[7:]
    
        # translate
        # FB - LH
        row = row.replace("F", "L").replace("B", "H")
    
        # LR - LH
        col = col.replace("R", "H")
    
        cards.append((row, col))
    return cards
    

def partition(insts, low=0, high=127):
    
    opts = range(low, high + 1)
    
    for inst in insts:
        
        pivot = int(len(opts) / 2)
        
        if inst == "L":
            opts = opts[:pivot]
        elif inst == "H":
            opts = opts[pivot:]
        
    return opts[0]


def find_seat(row, col):
    
    seat_row = partition(row, low=0, high=127)
    seat_col = partition(col, low=0, high=7)
    
    return seat_row, seat_col


if __name__ == "__main__":
    cards = read_pass(sys.argv[-1])
    
    seat_ids = []
    
    for card_row, card_col in cards:
        s_r, s_c = find_seat(card_row, card_col)
        seat_id = s_r * 8 + s_c
        seat_ids.append(seat_id)
    
    print("max seat_id: %d" % (max(seat_ids),))