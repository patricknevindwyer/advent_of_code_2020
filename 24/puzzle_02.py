import sys


class HexGrid:
    """
         /\
        |  |
         \/
    
     1 2 3 4 5 6
      7 8 9 0 1
     2 3 4 5 6 7
    
    y % 2 == 1
     e - ( 1,  0)
     w - (-1,  0)
    ne - ( 1, -1)
    nw - ( 0, -1)
    se - ( 1,  1)
    sw - ( 0,  1)
    
    y % 2 == 0
     e - ( 1,  0)
     w - (-1,  0)
    ne - ( 0, -1)
    nw - (-1, -1)
    se - ( 0,  1)
    sw - (-1,  1)
    
    """
    
    def __init__(self, size=50):
        self.tiles = self._empty_grid(size=size)
        self.size = size
        self.ref_x = int(size / 2)
        self.ref_y = int(size / 2)
    
    def _empty_grid(self, size=50):
        g = []
        for idx_y in range(size):
            g.append([0 for idx_x in range(size)])
        
        return g
    
    def display(self):
        for idx_y in range(self.size):
            if idx_y % 2 == 1:
                print(" ", flush=True, end="")
            print(" ".join([str(t) for t in self.tiles[idx_y]]))
                
    def location_for_moves(self, moves=None):
        """
        y % 2 == 1
         e - ( 1,  0)
         w - (-1,  0)
        ne - ( 1, -1)
        nw - ( 0, -1)
        se - ( 1,  1)
        sw - ( 0,  1)
    
        y % 2 == 0
         e - ( 1,  0)
         w - (-1,  0)
        ne - ( 0, -1)
        nw - (-1, -1)
        se - ( 0,  1)
        sw - (-1,  1)
        
        """
        x = self.ref_x
        y = self.ref_y

        for m in moves:
            if y % 2 == 1:
                move_units = {
                    "e":  ( 1,  0),
                    "w":  (-1,  0),
                    "ne": ( 1, -1),
                    "nw": ( 0, -1),
                    "se": ( 1,  1),
                    "sw": ( 0,  1)
                }

            # for x % 2 == 0
            else:
                move_units = {
                    "e":  ( 1,  0),
                    "w":  (-1,  0),
                    "ne": ( 0, -1),
                    "nw": (-1, -1),
                    "se": ( 0,  1),
                    "sw": (-1,  1)
                }

            mu = move_units[m]
            x += mu[0]
            y += mu[1]

        return x, y
            
    def toggle(self, x=None, y=None):
        self.tiles[y][x] = (self.tiles[y][x] + 1) % 2

    def count(self, state=1):
        agg = 0
        for idx_y in range(len(self.tiles)):
            for idx_x in range(len(self.tiles)):
                agg += self.tiles[idx_y][idx_x]
        return agg
    
    def neighbors(self, x=0, y=0):
        """
        y % 2 == 1
         e - ( 1,  0)
         w - (-1,  0)
        ne - ( 1, -1)
        nw - ( 0, -1)
        se - ( 1,  1)
        sw - ( 0,  1)
    
        y % 2 == 0
         e - ( 1,  0)
         w - (-1,  0)
        ne - ( 0, -1)
        nw - (-1, -1)
        se - ( 0,  1)
        sw - (-1,  1)
        
        """
        # for y % 2 == 1
        if y % 2 == 1:
            move_units = {
                "e":  ( 1,  0),
                "w":  (-1,  0),
                "ne": ( 1, -1),
                "nw": ( 0, -1),
                "se": ( 1,  1),
                "sw": ( 0,  1)
            }
        
        # for y % 2 == 0
        else:
            move_units = {
                "e":  ( 1,  0),
                "w":  (-1,  0),
                "ne": ( 0, -1),
                "nw": (-1, -1),
                "se": ( 0,  1),
                "sw": (-1,  1)
            }      
        
        nbs = []
        
        for (neb_x, neb_y) in move_units.values():
            loc_x = x + neb_x
            loc_y = y + neb_y
            
            if loc_x < 0 or loc_x >= self.size:
                continue
            if loc_y < 0 or loc_y >= self.size:
                continue
            
            nbs.append(self.tiles[loc_y][loc_x])
        
        return nbs
        
    def age(self):
        
        # create a grid copy
        gcopy = self._empty_grid(size=self.size)
        
        # walk the grid
        for idx_y in range(self.size):
            for idx_x in range(self.size):
                me = self.tiles[idx_y][idx_x]
                nbs = self.neighbors(x=idx_x, y=idx_y)
                
                me_next = me
                
                if me == 1:
                    if sum(nbs) == 0:
                        me_next = 0
                    elif sum(nbs) > 2:
                        me_next = 0
                else:
                    if sum(nbs) == 2:
                        me_next = 1
                gcopy[idx_y][idx_x] = me_next
        
        self.tiles = gcopy
                

def read_moves(filename):
    with open(filename, "r", encoding="utf-8") as f:
        raw = f.read()
    
    all_moves = []
    
    tokens = ["ne", "nw", "se", "sw", "w", "e"]
    
    for line in raw.split("\n"):
        
        moves = []
        
        while len(line) > 0:
            for tok in tokens:
                if line.startswith(tok):
                    moves.append(tok)
                    line = line[len(tok):]
                    break
        all_moves.append(moves)
    
    return all_moves


if __name__ == "__main__":
    all_moves = read_moves(sys.argv[-1])
    hgrid = HexGrid(size=160)
    for moves in all_moves:
        tile_x, tile_y = hgrid.location_for_moves(moves=moves)
        hgrid.toggle(x=tile_x, y=tile_y)
        
    print("Start")
    print("%d tiles are black" % (hgrid.count(),))
    
    hgrid.display()
    for day in range(100):
        hgrid.age()
        print("--- Day %d - %d black tiles" % (day + 1, hgrid.count(),))