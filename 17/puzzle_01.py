import sys


class CubeAutomata:
    
    def __init__(self, size=11):
        # setup our cube structures, in z, y, x ordering
        self.cube = self._empty_cube(size)
        self.size = size
    
    def _empty_cube(self, size=11):
        cube = []
        for z in range(size):
            rows = []
            for y in range(size):
                rows.append(["." for _i in range(size)])
            cube.append(rows)
        return cube
        
    def get(self, x, y, z):
        return self.cube[z][y][x]
    
    def set(self, x, y, z, v):
        self.cube[z][y][x] = v
    
    def insert_slice(self, slice=None, z=0, x_offset=0, y_offset=0):
        
        for idx_y in range(len(slice)):
            for idx_x in range(len(slice[0])):
                self.set(idx_x + x_offset, idx_y + y_offset, z, slice[idx_y][idx_x])
    
    def neighbors(self, x=0, y=0, z=0):
        
        nebs = []
        
        for idx_z in range(z - 1, z + 2):
            
            # bounds
            if idx_z < 0 or idx_z >= self.size:
                continue
                
            for idx_y in range(y - 1, y + 2):
                
                # bounds
                if idx_y < 0 or idx_y >= self.size:
                    continue
                    
                for idx_x in range(x - 1, x + 2):
                    
                    # bounds
                    if idx_x < 0 or idx_x >= self.size:
                        continue
                    
                    # don't count ourself
                    if idx_z == z and idx_y == y and idx_x == x:
                        continue
                    
                    nebs.append(self.cube[idx_z][idx_y][idx_x])
        return nebs
    
    def step(self):
        
        # create our empty next stage cube
        ncube = self._empty_cube(self.size)
        
        # walk da cube
        for idx_z in range(self.size):
            for idx_y in range(self.size):
                for idx_x in range(self.size):
                    
                    me = self.get(x=idx_x, y=idx_y, z=idx_z)
                    nebs = self.neighbors(x=idx_x, y=idx_y, z=idx_z)
                    a_nebs = len([n for n in nebs if n == "#"])
                    me_prime = "."
                    
                    if me == "#":
                        if a_nebs == 2 or a_nebs == 3:
                            me_prime = "#"
                        else:
                            me_prime = "."
                    else:
                        if a_nebs == 3:
                            me_prime = "#"
                        else:
                            me_prime = "."
                    ncube[idx_z][idx_y][idx_x] = me_prime
        self.cube = ncube
    
    def display(self):
        z_correct = int(self.size / 2)
        for idx_z in range(self.size):
            print("z=%d" % (idx_z - z_correct,))
            
            for idx_y in range(self.size):
                print("".join(self.cube[idx_z][idx_y]))
            print("")
    
    def active(self):
        a_count = 0
        for idx_z in range(self.size):
            for idx_y in range(self.size):
                for idx_x in range(self.size):
                    if self.cube[idx_z][idx_y][idx_x] == "#":
                        a_count += 1
        return a_count
        

def read_slice(filename):
    with open(filename, "r", encoding="utf-8") as f:
        raw = f.read()
    rows = []
    
    for l in raw.split("\n"):
        rows.append([c for c in l.strip()])
    
    return rows


if __name__ == "__main__":
    sl = read_slice(sys.argv[-1])
    
    # determine _where_ we're inserting our slice, centering it
    # in the cube
    size = 21
    size_h = int(size / 2)
    off = size_h - int(len(sl) / 2)
    
    # create the cube
    cube = CubeAutomata(size=size)
    cube.insert_slice(sl, z=size_h, x_offset=off, y_offset=off)
    
    # debug display layer one
    cube.display()
    for s in range(6):
        cube.step()
    print("%d active cells" % (cube.active(),))