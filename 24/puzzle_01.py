import sys


class HexGrid:
    """
         /\
        |  |
         \/
    
     1 2 3 4 5 6
      7 8 9 0 1
    
     e - ( 1,  0)
     w - (-1,  0)
    ne - ( 1, -1)
    nw - ( 0, -1)
    se - ( 0,  1)
    sw - (-1,  1)
    """
    
    def __init__(self, size=50):
        self.tiles = []
        for idx_y in range(size):
            self.tiles.append([0 for idx_x in range(size)])
    
        self.ref_x = int(size / 2)
        self.ref_y = int(size / 2)
        
    def location_for_moves(self, moves=None):
        move_agg_x = 0
        move_agg_y = 0
        
        move_units = {
            "e": (1, 0),
            "w": (-1, 0),
            "ne": (1, -1),
            "nw": (0, 0-1),
            "se": (0, 1),
            "sw": (-1, 1)
        }
        
        for m in moves:
            mu = move_units[m]
            move_agg_x += mu[0]
            move_agg_y += mu[1]
        
        return self.ref_x + move_agg_x, self.ref_y + move_agg_y
    
    def toggle(self, x=None, y=None):
        self.tiles[y][x] = (self.tiles[y][x] + 1) % 2

    def count(self, state=1):
        agg = 0
        for idx_y in range(len(self.tiles)):
            for idx_x in range(len(self.tiles)):
                agg += self.tiles[idx_y][idx_x]
        return agg


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
    hgrid = HexGrid()
    for moves in all_moves:
        tile_x, tile_y = hgrid.location_for_moves(moves=moves)
        hgrid.toggle(x=tile_x, y=tile_y)
    print("%d tiles are black" % (hgrid.count(),))