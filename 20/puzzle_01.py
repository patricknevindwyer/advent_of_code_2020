import copy
import sys


def read_tiles(filename):
    with open(filename, "r", encoding="utf-8") as f:
        raw = f.read()
    
    tiles = []
    
    # read everything
    for tile_raw in raw.split("\n\n"):
        tile_lines = tile_raw.strip().split("\n")
        
        # get the tile id
        tile_id = int(tile_lines[0].strip(":").split(" ")[1])
        
        # tile-ize the row data
        tile_bits = []
        for tile_row in tile_lines[1:]:
            tile_bits.append([c for c in tile_row.strip()])
        
        tiles.append(Tile(id=tile_id, points=tile_bits))
    
    return tiles
    
    
class Tile:
    
    def __init__(self, id=0, points=None):
        self.id = id
        self.edges = []
        self.edge_match_ids = set()
        
        # fill all edges
        
        # top and bottom
        for idx in [0, -1]:
            t = copy.deepcopy(points[idx])
            self.edges.append(copy.deepcopy(t))
            t.reverse()
            self.edges.append(copy.deepcopy(t))
        
        # left and right
        for idx in [0, -1]:
            side = [r[idx] for r in points]
            self.edges.append(copy.deepcopy(side))
            side.reverse()
            self.edges.append(copy.deepcopy(side))
        
    def iter_edges(self):
        for e in self.edges:
            yield e
    

def find_connections(tiles):
    
    for idx_a in range(len(tiles)):
        for idx_b in range(idx_a, len(tiles)):
            if idx_a == idx_b:
                continue
                
            match = False
            for a_edge in tiles[idx_a].iter_edges():
                for b_edge in tiles[idx_b].iter_edges():
                    if a_edge == b_edge:
                        match = True
                        break
                if match:
                    break
            if match:
                tiles[idx_a].edge_match_ids.add(tiles[idx_b].id)
                tiles[idx_b].edge_match_ids.add(tiles[idx_a].id)


if __name__ == "__main__":
    tiles = read_tiles(sys.argv[-1])
    find_connections(tiles)
    
    for tile in tiles:
        print("Tile %d" % (tile.id,))
        print("  edge matches: ", tile.edge_match_ids)
    
    corners = [tile.id for tile in tiles if len(tile.edge_match_ids) == 2]
    print("Corners: ", corners)
    carry = 1
    for c in corners:
        carry *= c
    print("chksum: %d" % (carry,))