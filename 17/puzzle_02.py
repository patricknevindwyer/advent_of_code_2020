import sys


class HyperCubeAutomata:
    
    def __init__(self, size=11):
        # setup our cube structures, in w, z, y, x ordering
        self.hcube = self._empty_hypercube(size)
        self.size = size
    
    def _empty_hypercube(self, size=11):
        hcube = []
        for w in range(size):
            cube = []
            for z in range(size):
                rows = []
                for y in range(size):
                    rows.append(["." for _i in range(size)])
                cube.append(rows)
            hcube.append(cube)
        return hcube
        
    def get(self, x, y, z, w):
        return self.hcube[w][z][y][x]
    
    def set(self, x, y, z, w, v):
        self.hcube[w][z][y][x] = v
    
    def insert_slice(self, slice=None, w=0, z=0, x_offset=0, y_offset=0):
        
        for idx_y in range(len(slice)):
            for idx_x in range(len(slice[0])):
                self.set(idx_x + x_offset, idx_y + y_offset, z, w, slice[idx_y][idx_x])
    
    def neighbors(self, x=0, y=0, z=0, w=0):
        
        nebs = []
        
        for idx_w in range(w - 1, w + 2):
            if idx_w < 0 or idx_w >= self.size:
                continue
                
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
                        if idx_z == z and idx_y == y and idx_x == x and idx_w == w:
                            continue
                    
                        nebs.append(self.hcube[idx_w][idx_z][idx_y][idx_x])
        return nebs
    
    def step(self):
        
        # create our empty next stage cube
        ncube = self._empty_hypercube(self.size)
        
        # walk da cube
        for idx_w in range(self.size):
            for idx_z in range(self.size):
                for idx_y in range(self.size):
                    for idx_x in range(self.size):
                    
                        me = self.get(x=idx_x, y=idx_y, z=idx_z, w=idx_w)
                        nebs = self.neighbors(x=idx_x, y=idx_y, z=idx_z, w=idx_w)
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
                        ncube[idx_w][idx_z][idx_y][idx_x] = me_prime
        self.hcube = ncube
    
    def is_empty(self, w=0, z=0):
        active = 0
        for idx_y in range(self.size):
            for idx_x in range(self.size):
                if self.hcube[w][z][idx_y][idx_x] == "#":
                    active += 1
        return active == 0
        
    def display(self):
        z_correct = int(self.size / 2)
        w_correct = int(self.size / 2)
        
        for idx_w in range(self.size):
            for idx_z in range(self.size):
                
                if self.is_empty(w=idx_w, z=idx_z):
                    continue
                    
                print("z=%d, w=%d" % (idx_z - z_correct, idx_w - w_correct))
            
                for idx_y in range(self.size):
                    print("".join(self.hcube[idx_w][idx_z][idx_y]))
                print("")
    
    def active(self):
        a_count = 0
        for idx_w in range(self.size):
            for idx_z in range(self.size):
                for idx_y in range(self.size):
                    for idx_x in range(self.size):
                        if self.hcube[idx_w][idx_z][idx_y][idx_x] == "#":
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
    cube = HyperCubeAutomata(size=size)
    cube.insert_slice(sl, w=size_h, z=size_h, x_offset=off, y_offset=off)
    
    # debug display layer one
    cube.display()
    for s in range(6):
        cube.step()
    print("%d active cells" % (cube.active(),))