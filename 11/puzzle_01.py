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
        for idx_y in range(y - 1, y + 2):
            for idx_x in range(x - 1, x + 2):
                if idx_y < 0 or idx_x < 0:
                    continue
                if idx_y >= self.height or idx_x >= self.width:
                    continue
                
                if idx_y == y and idx_x == x:
                    continue
                
                nebs.append(self.grid[idx_y][idx_x])
        return nebs
    
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
                if me == "#" and nebs_seated >= 4:
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