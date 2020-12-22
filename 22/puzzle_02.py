import sys
import copy


class Deck:
    
    def __init__(self, id=None, cards=None):
        self.id = id
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
    
    def chksum(self):
        return ":".join([str(c) for c in self.cards])
    
    def should_recurse(self, card):
        return card <= len(self.cards)
    
    def recursion_deck(self, card):
        return Deck(id=self.id, cards=copy.deepcopy(self.cards[:card]))
    
    def __str__(self):
        return ", ".join([str(c) for c in self.cards])
        

def read_deck(filename):
    with open(filename, "r", encoding="utf-8") as f:
        raw = f.read()
    
    pa_raw, pb_raw = raw.split("\n\n")
    
    pa = [int(c) for c in pa_raw.split("\n")[1:]]
    pb = [int(c) for c in pb_raw.split("\n")[1:]]
    
    return Deck(id="player a", cards=pa), Deck(id="player b", cards=pb)


def play(deck_a, deck_b):
    
    rounds = 0
    
    previous_decks = set()
    
    while not deck_a.empty() and not deck_b.empty():
        
        rounds += 1
        print("-- Round %d" % (rounds,))
        print("Deck A: %s" % (deck_a,))
        print("Deck B: %s" % (deck_b,))
        
        # check for ordering for infinite recursion drop out
        chksum = deck_a.chksum() + "::" + deck_b.chksum()
        if chksum in previous_decks:
            return deck_a
        else:
            previous_decks.add(chksum)
            
        # play this round by picking cards
        c_a = deck_a.play()
        c_b = deck_b.play()
        
        if deck_a.should_recurse(c_a) and deck_b.should_recurse(c_b):
            
            print("Playing a sub-game")
            print("")
            
            # who is the winner?
            recursion_winner = play(deck_a.recursion_deck(c_a), deck_b.recursion_deck(c_b))
            if recursion_winner.id == deck_a.id:
                deck_a.add(c_a, c_b)
            else:
                deck_b.add(c_b, c_a)

        else:
            
            # just play normally
            if c_a > c_b:
                deck_a.add(c_a, c_b)
            else:
                deck_b.add(c_b, c_a)
        print("")
    

    # who won?
    if not deck_a.empty():
        return deck_a
    else:
        return deck_b


if __name__ == "__main__":
    deck_a, deck_b = read_deck(sys.argv[-1])
    winner = play(deck_a, deck_b)
    print("Score: %d" % (winner.score(),))