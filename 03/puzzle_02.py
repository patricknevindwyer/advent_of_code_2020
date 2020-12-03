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
    
    # get our geo
    tree_geo = LocalMap(sys.argv[-1])
    
    # time to test our different slopes
    slopes = [
        (1, 1),
        (3, 1),
        (5, 1),
        (7, 1),
        (1, 2)
    ]
    
    tree_counts = 1
    
    for (slope_run, slope_rise) in slopes:
        tree_count = trees_on_slope(tree_geo, slope_rise, slope_run)
        tree_counts = tree_counts * tree_count
    
    print("%d" % (tree_counts,))