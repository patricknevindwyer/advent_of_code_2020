import sys

class LocalMap:
    
    def __init__(self, filename):
        """
        load the file, and get our map loaded into memory
        """
        self._data = []
        
        # load data
        with open(filename, "r", encoding="utf-8") as map_file:
            raw = map_file.read()
        
        # parse data
        for line in raw.split("\n"):
            r = []
            for c in line.strip():
                r.append(c)
            self._data.append(r)
    
    def height(self):
        return len(self._data)
    
    def width(self):
        return len(self._data[0])
        
    def get(self, x, y):
        
        # quick bail
        if y >= self.height():
            return None
        
        # wrap x around via modulo
        x = x % self.width()
        
        return self._data[y][x]


def trees_on_slope(tree_geo, s_rise, s_run):
    
    loc_x = 0
    loc_y = 0
    tree_count = 0
    
    while loc_y < tree_geo.height():
        at = tree_geo.get(loc_x, loc_y)
        
        if at == "#":
            tree_count += 1
        
        loc_x += s_run
        loc_y += s_rise
    
    return tree_count
        
        
if __name__ == "__main__":
    
    tree_geo = LocalMap(sys.argv[-1])
    tree_count = trees_on_slope(tree_geo, 1, 3)
    print("%d" % (tree_count,))