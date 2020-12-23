import sys
import copy


class Ring:
    
    def __init__(self, r=None):
        self.ring = copy.deepcopy(r)
        
        # fill up to one million
        for x in range(6,1000001):
            self.ring.append(x)
            
        self.idx = 0
    
    def current(self):
        return self.ring[idx]
    
    def __str__(self):
        labs = []
        
        for idx in range(len(self.ring)):
            if idx == self.idx:
                labs.append("(%d)" % (self.ring[idx]))
            else:
                labs.append("%d" % (self.ring[idx]))
        return " ".join(labs)
    
    def step(self):
        
        # adjust so we have plenty of working room
        if (len(self.ring) - self.idx) <= 3:
            # re arrange
            self.ring = self.ring[self.idx:] + self.ring[:self.idx]
            self.idx = 0
            
        pickup = self.ring[self.idx + 1:self.idx + 4]
        self.ring = self.ring[:self.idx + 1] + self.ring[self.idx + 4:]
        # print("Pickup: %s" % (", ".join([str(d) for d in pickup])))
        
        # what's our placement
        place = self.ring[self.idx] - 1
        
        while place in pickup:
            place -= 1
            
        if place < 1:
            place = max(self.ring)
        
        # print("destination: %d" % (place,))
        
        # insert the new slice
        dst_idx = self.ring.index(place)
        self.ring = self.ring[:dst_idx + 1] + pickup + self.ring[dst_idx + 1:]
        
        # adjust idx?
        if dst_idx < self.idx:
            self.idx += 3
        
        # increment the index
        self.idx += 1
    
    def hidden(self):
        pivot = self.ring.index(1)
        return self.ring[pivot + 1:pivot + 3]
        
    def checksum(self):
        pivot = self.ring.index(1)
        chk_order = self.ring[pivot:] + self.ring[:pivot]
        return "".join([str(d) for d in chk_order])[1:]


def read_labels(filename):
    with open(filename, "r", encoding="utf-8") as f:
        raw = f.read()
    
    return Ring(r=[int(d) for d in raw.strip()])


if __name__ == "__main__":
    ring = read_labels(sys.argv[-1])
    
    
    for move in range(10000000):
        if move % 100000 == 0:
            print("-- move %d --" % (move + 1,))
            print("idx: %s" % (ring.idx,))
        ring.step()
    
    print("-- final --")
    print("cups: %s" % (ring,))
    
    hidden = ring.hidden()
    chk = hidden[0] * hidden[1]
    print("hidden %d * %d == %d" % (hidden[0], hidden[1], chk))