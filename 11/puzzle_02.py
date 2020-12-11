import sys
import copy


class Grid:
    
    def __init__(self, width=20, height=20):
        self.width = width
        self.height = height
        self.grid = None
        self.stable = False
        
    def fill_empty(self):
        pass
    
    def fill_from_copy(self, other_grid=None):
        pass
    
    def fill_from_arrays(self, data_array=None):
        
        # reset our height/width
        self.height = len(data_array)
        self.width = len(data_array[0])
        
        self.grid = copy.deepcopy(data_array)
        
    def put(self, x, y, v):
        self.grid[y][x] = v
        
    def get(self, x=0, y=0):
        return self.grid[y][x]
    
    def count(self, v):
        c = 0
        
        for row in self.grid:
            for cell in row:
                if cell == v:
                    c += 1
        return c
    
    def neighbors(self, x=0, y=0):
        nebs = []
        
        # we now need to find the next possible seat, not just immediate neighbors
        dirs = [
            [ 1,  0], # right
            [-1,  0], # left
            [ 0,  1], # down
            [ 0, -1], # up
            [-1, -1], # NW
            [-1,  1], # SW
            [ 1, -1], # NE
            [ 1,  1], # SE
        ]
        
        for direction in dirs:
            nebs.append(self.neighbor_by_direction(x=x, y=y, delta_x=direction[0], delta_y=direction[1]))
        return nebs
    
    def neighbor_by_direction(self, x=0, y=0, delta_x=0, delta_y=0):
        
        # step until we don't have a valid position
        chk_x = x + delta_x
        chk_y = y + delta_y
        
        # we default to a floor space
        neb = "."
        
        while True:
            
            # are we out of bounds?
            if chk_x < 0 or chk_y < 0:
                break
            
            if chk_x >= self.width or chk_y >= self.height:
                break
                
            # look at the spot, if it's something iteresting keep going
            spot = self.grid[chk_y][chk_x]
            
            if spot != ".":
                neb = spot
                break
                
            # change our spot
            chk_x += delta_x
            chk_y += delta_y
        
        return neb
    
    def display(self):
        for row in self.grid:
            
            # offset
            print("  ", flush=True, end="")
            
            for cell in row:
                print(cell, flush=True, end="")
            print("")
    
    def step(self):
        
        # if we're already in a stable state, don't keep going
        if self.stable:
            return
            
        # create a copy of our array, and run our automata
        new_grid = copy.deepcopy(self.grid)
        
        for idx_h in range(self.height):
            for idx_w in range(self.width):
                me = self.get(x=idx_w, y=idx_h)
                
                # am I floor?
                if me == ".":
                    continue
                    
                # get the neighbors
                nebs = self.neighbors(x=idx_w, y=idx_h)
                
                nebs_seated = sum([1 for n in nebs if n == "#"])
                
                if me == "L" and nebs_seated == 0:
                    new_grid[idx_h][idx_w] = "#"
                if me == "#" and nebs_seated >= 5:
                    new_grid[idx_h][idx_w] = "L"
        
        # check for stasis
        if new_grid == self.grid:
            self.stable = True
            
        # store ourself
        self.grid = new_grid
        
        
def read_grid(filename):
    """
    Read in the test file and create a grid
    """
    
    with open(filename, "r", encoding="utf-8") as f:
        raw = f.read()
    
    # read our data
    rows = []
    
    for line in raw.split("\n"):
        row = []
        for c in line.strip():
            row.append(c)
        rows.append(row)
     
    g = Grid()
    g.fill_from_arrays(rows)
    
    return g


if __name__ == "__main__":
    grid = read_grid(sys.argv[-1])
    
    print("Starting arrangement:")
    grid.display()
    
    while not grid.stable:
        grid.step()
    
    print("There are %d seats occupied" % (grid.count("#"),))