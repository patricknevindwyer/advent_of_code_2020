import sys


class Deck:
    
    def __init__(self, cards=None):
        self.cards = cards
    
    def play(self):
        return self.cards.pop(0)
    
    def add(self, my_card=None, op_card=None):
        self.cards.append(my_card)
        self.cards.append(op_card)
    
    def score(self):
        self.cards.reverse()
        carry = 0
        idx = 0
        
        for card in self.cards:
            idx += 1
            carry += (card * idx)
            
        self.cards.reverse()
        return carry
    
    def empty(self):
        return len(self.cards) == 0
        

def read_deck(filename):
    with open(filename, "r", encoding="utf-8") as f:
        raw = f.read()
    
    pa_raw, pb_raw = raw.split("\n\n")
    
    pa = [int(c) for c in pa_raw.split("\n")[1:]]
    pb = [int(c) for c in pb_raw.split("\n")[1:]]
    
    return Deck(cards=pa), Deck(cards=pb)


def play(deck_a, deck_b):
    
    
    while not deck_a.empty() and not deck_b.empty():
        c_a = deck_a.play()
        c_b = deck_b.play()
        
        if c_a > c_b:
            deck_a.add(c_a, c_b)
        else:
            deck_b.add(c_b, c_a)
    
    # who won?
    if not deck_a.empty():
        return deck_a
    else:
        return deck_b


if __name__ == "__main__":
    deck_a, deck_b = read_deck(sys.argv[-1])
    winner = play(deck_a, deck_b)
    print("Score: %d" % (winner.score(),))