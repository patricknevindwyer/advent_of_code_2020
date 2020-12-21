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
        
        # the points are kept around for final analysis, with an original set so we can
        # iterate through the rotations/etc
        self.points = points
        self.aligned_points = points
        self.aligned = False
        
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
    
    def deepcopy(self):
        g = Tile(id=self.id, points=self.points)
        g.points = copy.deepcopy(self.points)
        g.aligned_points = copy.deepcopy(self.aligned_points)
        g.aligned = True
        return g
        
    def display(self):
        print(self.render())
    
    def render(self):
        return "\n".join(["".join(row) for row in self.aligned_points])
        
    def iter_edges(self):
        for e in self.edges:
            yield e
    
    def iter_edges_with_key(self):
        """
        Walk the edge iterations with keys to what the edge represents
        """
        reps = ["top", "top-hor", "bottom", "bottom-hor", "left", "left-ver", "right", "right-ver"]
        
        for idx in range(len(reps)):
            yield reps[idx], self.edges[idx]
    
    def steps_for_transform(self, rep=None, facing=None):
        """
        Just return the steps required for a given transform
        """
        trans = {
            "left": {
                "top": ["cw", "cw", "cw"],
                "top-hor": ["cw", "cw", "cw", "ver"],
                "bottom": ["cw"],
                "bottom-hor": ["cw", "ver"],
                "left": [],
                "left-ver": ["ver"],
                "right": ["cw", "cw"],
                "right-ver": ["cw", "cw", "ver"]
            },
            "right": {
                "top": ["cw"],
                "top-hor": ["cw", "ver"],
                "bottom": ["cw", "cw", "cw"],
                "bottom-hor": ["cw", "cw", "cw", "ver"],
                "left": ["cw", "cw"],
                "left-ver": ["cw", "cw", "ver"],
                "right": [],
                "right-ver": ["ver"]                
            },
            "top": {
                "top": [],
                "top-hor": ["cw", "cw", "ver"],
                "bottom": ["cw", "cw"],
                "bottom-hor": ["ver"],
                "left": ["cw", "cw", "cw"],
                "left-ver": ["cw", "cw", "cw", "ver"],
                "right": ["cw"],
                "right-ver": ["cw", "ver"]                
            },
            "bottom": {
                "top": ["cw", "cw"],
                "top-hor": ["ver"],
                "bottom": [],
                "bottom-hor": ["cw", "cw", "ver"],
                "left": ["cw"],
                "left-ver": ["cw", "ver"],
                "right": ["cw", "cw", "cw"],
                "right-ver": ["cw", "cw", "cw", "ver"]                
            }
        }
        
        return trans[facing][rep]
        
    def transform(self, rep=None, facing=None):
        """
        Transform by one of our representations to face the rep side to the right or left.
        """
        self.aligned_points = copy.deepcopy(self.points)
        self.aligned = True
        
        trans = {
            "left": {
                "top": ["cw", "cw", "cw"],
                "top-hor": ["cw", "cw", "cw", "ver"],
                "bottom": ["cw"],
                "bottom-hor": ["cw", "ver"],
                "left": [],
                "left-ver": ["ver"],
                "right": ["cw", "cw"],
                "right-ver": ["cw", "cw", "ver"]
            },
            "right": {
                "top": ["cw"],
                "top-hor": ["cw", "ver"],
                "bottom": ["cw", "cw", "cw"],
                "bottom-hor": ["cw", "cw", "cw", "ver"],
                "left": ["cw", "cw"],
                "left-ver": ["cw", "cw", "ver"],
                "right": [],
                "right-ver": ["ver"]                
            },
            "top": {
                "top": [],
                "top-hor": ["cw", "cw", "ver"],
                "bottom": ["cw", "cw"],
                "bottom-hor": ["ver"],
                "left": ["cw", "cw", "cw"],
                "left-ver": ["cw", "cw", "cw", "ver"],
                "right": ["cw"],
                "right-ver": ["cw", "ver"]                
            },
            "bottom": {
                "top": ["cw", "cw"],
                "top-hor": ["ver"],
                "bottom": [],
                "bottom-hor": ["cw", "cw", "ver"],
                "left": ["cw"],
                "left-ver": ["cw", "ver"],
                "right": ["cw", "cw", "cw"],
                "right-ver": ["cw", "cw", "cw", "ver"]                
            }
        }
        
        for step in trans[facing][rep]:
            if step == "cw":
                self.aligned_points = list(zip(*self.aligned_points[::-1]))
            elif step == "ver":
                self.aligned_points.reverse()
            elif step == "hor":
                for row in self.aligned_points:
                    row.reverse()
        
    def strip_border(self):
        """
        Remove the border on the aligned points
        """
        self.aligned_points = [list(row[1:-1]) for row in self.aligned_points[1:-1]]
        self.points = [list(row[1:-1]) for row in self.points[1:-1]]
    
    def count_waves(self):
        pass
    
    def get_aligned_edge(self, facing=None):
        if facing == "top":
            return self.aligned_points[0]
        elif facing == "bottom":
            return self.aligned_points[-1]
        elif facing == "left":
            return [r[0] for r in self.aligned_points]
        elif facing == "right":
            return [r[-1] for r in self.aligned_points]
    

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


def arrange_tiles(tiles, edge_size=12):
    """
    Arrange the tiles to make sense of the image, picking one of the corners to start
    """
    
    # we assume a 12x12 grid for our image, and we start at a corner and arrange things from there
    # arranged and row are both arrays of Tile objects
    arranged = []
    row = []
    
    # index tiles by id
    tile_by_id = {tile.id: tile for tile in tiles}
    
    # track which tiles have already been placed
    placed = set()
    
    while len(placed) != len(tiles):
        while len(row) < edge_size:
            
            # at each row we start with a seed value, and work from there
            if len(row) == 0:
                if len(arranged) == 0:
            
                    # seed is the first corner we have available
                    seed = [t for t in tiles if len(t.edge_match_ids) == 2][0]
                else:
                    # seed is based on the tile above us, and we need to find the ids we _could_ be at an edge
                    above = arranged[-1][0]
                    seed = tile_by_id[[edge_id for edge_id in above.edge_match_ids if edge_id not in placed][0]]
        
                # ok - place our seed in the row
                placed.add(seed.id)
                row.append(seed)
            else:
                
                if len(arranged) == 0:
                    # just find whatever has our left as a match
                    # find whatever has the left and above as a match
                    anchor_left = row[-1].id
                
                    for tile in tiles:
                        if tile.id in placed:
                            continue
                        if anchor_left in tile.edge_match_ids and len(tile.edge_match_ids) <= 3:
                            placed.add(tile.id)
                            row.append(tile)
                            break
                    
                else:
                    # find whatever has the left and above as a match
                    anchor_left = row[-1].id
                    anchor_top = arranged[-1][len(row)].id
                
                    for tile in tiles:
                        if tile.id in placed:
                            continue
                        if anchor_left in tile.edge_match_ids and anchor_top in tile.edge_match_ids:
                            placed.add(tile.id)
                            row.append(tile)
                            break
                
        # ok we've placed a row
        arranged.append(row)
        row = []

    
    # debug - print our arrangement of ids
    for row in arranged:
        print(" ".join([str(t.id) for t in row]))    
    
    return arranged


def all_aligned(arranged):
    for row in arranged:
        for tile in row:
            if not tile.aligned:
                return False
    return True
    

def align_tiles(arranged):
    
    # while not all_aligned(arranged):
    # at the start of each row, we align to our right
    # after the first tile of each row, try to align with the tile to the left
    variances = {}
    
    for t_cycle in range(10):
        
        unaligned = 0
        for row in arranged:
            for tile in row:
                if not tile.aligned:
                    unaligned += 1
                    
        print("atry %d || %d unaligned **************************" % (t_cycle, unaligned))
        
        for idx_y, row in enumerate(arranged):
            for idx_x, tile in enumerate(row):
            
                if tile.aligned:
                    continue
                
                # walk our local area and look for alignments
                for pinned_y in range(idx_y - 1, idx_y + 2):
                    if tile.aligned:
                        break
                
                    for pinned_x in range(idx_x - 1, idx_x + 2):
                
                        if tile.aligned:
                            break
                    
                        if tile.id == 3917:
                            print("    pre fast align tile(%d)" % (3917,))
                            print("     pinned_y: ", pinned_y)
                            print("     pinned_x: ", pinned_x)
                    
                        # don't check ourself
                        if pinned_y == idx_y and pinned_x == idx_x:
                            continue
                
                        # don't go out of bounds
                        if pinned_y < 0 or pinned_y >= len(arranged):
                            continue
                
                        if pinned_x < 0 or pinned_x >= len(arranged):
                            continue
                
                        # make sure this is cardinal to us
                        if pinned_x != idx_x and pinned_y != idx_y:
                            continue
                    
                        # check our neighbor
                        nb = arranged[pinned_y][pinned_x]
                
                        if not nb.aligned:
                            continue
                        
                        if tile.id == 3917:
                            print("    fast align tile(%d)" % (3917,))
                            print("     pinned_y: ", pinned_y)
                            print("     pinned_x: ", pinned_x)
                            print("     nb_id: ", nb.id)
                        print("    fast align tile(%d) to tile(%d)" % (tile.id, nb.id))
                        # get the edge near us
                        comp_edge = None
                        edge_facing = None
                        self_facing = None
                
                        if pinned_x == idx_x:
                            if pinned_y < idx_y:
                                edge_facing = "bottom"
                                self_facing = "top"
                            else:
                                edge_facing = "top"
                                self_facing = "bottom"
                        elif pinned_x < idx_x:
                            edge_facing = "right"
                            self_facing = "left"
                        else:
                            edge_facing = "left"
                            self_facing = "right"
                
                        comp_edge = nb.get_aligned_edge(facing=edge_facing)
                
                        matches = []
                        for rep, edge in tile.iter_edges_with_key():
                            if edge == comp_edge:
                                matches.append(rep)
                        if len(matches) == 1:
                            print("!! Fast pinned")
                            tile.transform(facing=self_facing, rep=rep)
        
                if tile.aligned:
                    continue
            
                # short circuit - if we're not a root tile, check if our alignment only matches
                # with a rooted tile
                if idx_y != 0 and idx_x != 0:
            
                    # left hand column
                    if idx_x == 0:
                
                        # check above us
                        above = arranged[idx_y - 1][0]
                        above_edge = above.get_aligned_edge(facing="bottom")
                
                        if above.aligned:
                            matches = []
                            for rep, edge in tile.iter_edges_with_key():
                                if edge == above_edge:
                                    matches.append(rep)
                    
                            if len(matches) == 1:
                                tile.transform(facing="top", rep=rep)
                                continue
                        
                    # top row
                    elif idx_y == 0:
                
                        # check to the left
                        left = arranged[idx_y][idx_x - 1]
                        left_edge = left.get_aligned_edge(facing="right")
                
                        if left.aligned:
                            matches = []
                            for rep, edge in tile.iter_edges_with_key():
                                if edge == left_edge:
                                    matches.append(rep)
                    
                            if len(matches) == 1:
                                tile.transform(facing="left", rep=rep)
                                continue
            
                    # not in the top or left edge
                    else:
                
                        # check the top or left
                
                        # check above us
                        above = arranged[idx_y - 1][0]
                        above_edge = above.get_aligned_edge(facing="bottom")
                
                        if above.aligned:
                            matches = []
                            for rep, edge in tile.iter_edges_with_key():
                                if edge == above_edge:
                                    matches.append(rep)
                    
                            if len(matches) == 1:
                                tile.transform(facing="top", rep=rep)
                                continue
                
                        # check to the left
                        left = arranged[idx_y][idx_x - 1]
                        left_edge = left.get_aligned_edge(facing="right")
                
                        if left.aligned:
                            matches = []
                            for rep, edge in tile.iter_edges_with_key():
                                if edge == left_edge:
                                    matches.append(rep)
                    
                            if len(matches) == 1:
                                tile.transform(facing="left", rep=rep)
                                continue
                
                # Ok - what next?
                # for everything but the bottom row
                if idx_y < (len(arranged) - 1):
            
                    # all but the right column
                    if idx_x < (len(arranged) - 1):
            
                        print("align tile %d" % (tile.id,))
            
                        # compare against the tile to the right and below
                        right = row[idx_x + 1]
                        below = arranged[idx_y + 1][idx_x]
            
                        aligned = False
            
                        # alignments is an index of things like ("cw", "hor") which define a tile transform
                        alignments = {}
            
                        # transform cue defines a representation and facing we'll use to finally transform
                        # this tile
                        transform_cue = {}
            
                        # compare to right
                        for rep, edge in tile.iter_edges_with_key():
                            for r_edge in right.iter_edges():
                                if edge == r_edge:
                                    # tile.transform(facing="right", rep=rep)
                        
                                    # store this transform for later. the 
                                    steps = tile.steps_for_transform(facing="right", rep=rep)
                                    alignments[tuple(steps)] = 1
                                    transform_cue[tuple(steps)] = rep
            
                        # compare to below
                        for rep, edge in tile.iter_edges_with_key():
                            for b_edge in below.iter_edges():
                                if edge == b_edge:
                                    steps = tile.steps_for_transform(facing="bottom", rep=rep)
                                    if tuple(steps) not in alignments:
                                        alignments[tuple(steps)] = 0
                                        transform_cue[tuple(steps)] = rep
                                    alignments[tuple(steps)] += 1
            
                        # identify the alignment we should use
                        matched_alignments = [align for align, matches in alignments.items() if matches == 2]
                        if len(matched_alignments) == 1:
                            print("tile(%d) has 1 alignment" % (tile.id,))
                            tile.transform(facing="right", rep=transform_cue[matched_alignments[0]])
                        else:
                            print(alignments)
                            print("tile(%d) has multiple alignments" % (tile.id,))
                            
                            # huh. let's pick one, and see what we get
                            if t_cycle > 5:
                                variances[tile.id] = {"facing": "right", "reps": [transform_cue[ak] for ak in alignments.keys()]}
                                picked = transform_cue[list(alignments.keys())[0]]
                                tile.transform(facing="right", rep=picked)
                                
                                
                    else:
            
                        print("align tile %d" % (tile.id,))
            
                        # compare against the tile to the right and below
                        left = row[idx_x - 1]
                        below = arranged[idx_y + 1][idx_x]
            
                        aligned = False
            
                        # alignments is an index of things like ("cw", "hor") which define a tile transform
                        alignments = {}
            
                        # transform cue defines a representation and facing we'll use to finally transform
                        # this tile
                        transform_cue = {}
            
                        # compare to right
                        for rep, edge in tile.iter_edges_with_key():
                            for l_edge in left.iter_edges():
                                if edge == l_edge:
                                    # tile.transform(facing="right", rep=rep)
                        
                                    # store this transform for later. the 
                                    steps = tile.steps_for_transform(facing="left", rep=rep)
                                    alignments[tuple(steps)] = 1
                                    transform_cue[tuple(steps)] = rep
            
                        # compare to below
                        for rep, edge in tile.iter_edges_with_key():
                            for b_edge in below.iter_edges():
                                if edge == b_edge:
                                    steps = tile.steps_for_transform(facing="bottom", rep=rep)
                                    if tuple(steps) not in alignments:
                                        alignments[tuple(steps)] = 0
                                        transform_cue[tuple(steps)] = rep
                                    alignments[tuple(steps)] += 1
            
                        # identify the alignment we should use
                        matched_alignments = [align for align, matches in alignments.items() if matches == 2]
                        if len(matched_alignments) == 1:
                            print("tile(%d) has 1 alignment" % (tile.id,))
                            tile.transform(facing="left", rep=transform_cue[matched_alignments[0]])
                        else:
                            print(alignments)
                            print("tile(%d) has multiple alignments" % (tile.id,))
                            
                            # huh. let's pick one, and see what we get
                            if t_cycle > 5:
                                variances[tile.id] = {"facing": "left", "reps": [transform_cue[ak] for ak in alignments.keys()]}
                                picked = transform_cue[list(alignments.keys())[0]]
                                tile.transform(facing="left", rep=picked)
                                
                            
                else:
            
                    # bottom row
            
            
                    # all but the right column
                    if idx_x < (len(arranged) - 1):
            
                        print("align tile %d" % (tile.id,))
            
                        # compare against the tile to the right and above
                        right = row[idx_x + 1]
                        above = arranged[idx_y - 1][idx_x]
            
                        aligned = False
            
                        # alignments is an index of things like ("cw", "hor") which define a tile transform
                        alignments = {}
            
                        # transform cue defines a representation and facing we'll use to finally transform
                        # this tile
                        transform_cue = {}
            
                        # compare to right
                        for rep, edge in tile.iter_edges_with_key():
                            for r_edge in right.iter_edges():
                                if edge == r_edge:
                                    # tile.transform(facing="right", rep=rep)
                        
                                    # store this transform for later. the 
                                    steps = tile.steps_for_transform(facing="right", rep=rep)
                                    alignments[tuple(steps)] = 1
                                    transform_cue[tuple(steps)] = rep
            
                        # compare to below
                        for rep, edge in tile.iter_edges_with_key():
                            for b_edge in above.iter_edges():
                                if edge == b_edge:
                                    steps = tile.steps_for_transform(facing="top", rep=rep)
                                    if tuple(steps) not in alignments:
                                        alignments[tuple(steps)] = 0
                                        transform_cue[tuple(steps)] = rep
                                    alignments[tuple(steps)] += 1
            
                        # identify the alignment we should use
                        matched_alignments = [align for align, matches in alignments.items() if matches == 2]
                        if len(matched_alignments) == 1:
                            print("tile(%d) has 1 alignment" % (tile.id,))
                            tile.transform(facing="right", rep=transform_cue[matched_alignments[0]])
                        else:
                            print(alignments)
                            print("tile(%d) has multiple alignments" % (tile.id,))
                            
                            # huh. let's pick one, and see what we get
                            if t_cycle > 5:
                                variances[tile.id] = {"facing": "right", "reps": [transform_cue[ak] for ak in alignments.keys()]}
                                picked = transform_cue[list(alignments.keys())[0]]
                                tile.transform(facing="right", rep=picked)
                                
                                                            
                    else:
            
                        print("align tile %d" % (tile.id,))
            
                        # compare against the tile to the right and below
                        left = row[idx_x - 1]
                        above = arranged[idx_y - 1][idx_x]
            
                        aligned = False
            
                        # alignments is an index of things like ("cw", "hor") which define a tile transform
                        alignments = {}
            
                        # transform cue defines a representation and facing we'll use to finally transform
                        # this tile
                        transform_cue = {}
            
                        # compare to right
                        for rep, edge in tile.iter_edges_with_key():
                            for l_edge in left.iter_edges():
                                if edge == l_edge:
                                    # tile.transform(facing="right", rep=rep)
                        
                                    # store this transform for later. the 
                                    steps = tile.steps_for_transform(facing="left", rep=rep)
                                    alignments[tuple(steps)] = 1
                                    transform_cue[tuple(steps)] = rep
            
                        # compare to below
                        for rep, edge in tile.iter_edges_with_key():
                            for b_edge in above.iter_edges():
                                if edge == b_edge:
                                    steps = tile.steps_for_transform(facing="top", rep=rep)
                                    if tuple(steps) not in alignments:
                                        alignments[tuple(steps)] = 0
                                        transform_cue[tuple(steps)] = rep
                                    alignments[tuple(steps)] += 1
            
                        # identify the alignment we should use
                        matched_alignments = [align for align, matches in alignments.items() if matches == 2]
                        if len(matched_alignments) == 1:
                            print("tile(%d) has 1 alignment" % (tile.id,))
                            tile.transform(facing="left", rep=transform_cue[matched_alignments[0]])
                        else:
                            print(alignments)
                            print("tile(%d) has multiple alignments" % (tile.id,))
                            
                            # huh. let's pick one, and see what we get
                            if t_cycle > 5:
                                variances[tile.id] = {"facing": "left", "reps": [transform_cue[ak] for ak in alignments.keys()]}
                                
                                picked = transform_cue[list(alignments.keys())[0]]
                                tile.transform(facing="left", rep=picked)
                            
    print(variances)
    for row in arranged:
        for tile in row:
            if not tile.aligned:
                print("Tile %d not aligned" % (tile.id,))
    return variances
    

def image_iterations(arranged, variances):
    """
    Create an iterator over our possible tile permutations, and then iterate
    over image versions
    """
    
    # pre-index our images for quick look up later on
    id_to_tile = {}
    for row in arranged:
        for tile in row:
            id_to_tile[tile.id] = tile
    
    # setup variances
    #  id: {facing, reps}
    v_tups = []
    for tile_id, variance in variances.items():
        tup_base = {"id": tile_id, "reps": []}
        for rep in variance["reps"]:
            tup_base["reps"].append({"facing": variance["facing"], "rep": rep})
        v_tups.append(tup_base)
    
    # call variance_iter
    for variance in variance_iter(v_tups):
        
        # take each variance entry and apply to our image, yeilding the image
        for tile_vary in variance:
            id_to_tile[tile_vary["tile_id"]].transform(facing=tile_vary["facing"], rep=tile_vary["rep"])
        
        yield arranged
        

def variance_iter(variances, carry=None):
    if carry is None:
        carry = []
    
    # grab the first variance
    variance = variances[0]
    
    # is this the last variance?
    if len(variances) == 1:
        for rep in variance["reps"]:
            yield carry + [{"tile_id": variance["id"], "facing": rep["facing"], "rep": rep["rep"]}]
    else:
        
        # iterate each of our items
        for rep in variance["reps"]:
            yield from variance_iter(variances[1:], carry + [{"tile_id": variance["id"], "facing": rep["facing"], "rep": rep["rep"]}])


def merge_tiles(aligned):
    """
    take arranged and aligned tiles, strip the borders, and merge
    """
    # copy
    merge_tiles = []
    for row in aligned:
        merge_row = []
        for tile in row:
            merge_row.append(tile.deepcopy())
        merge_tiles.append(merge_row)
        
    # strip
    for row in merge_tiles:
        for tile in row:
            tile.strip_border()
    
    full_image = []
    
    for row in merge_tiles:
        
        # walk the row index for our full image set row
        rows_per_tile = len(row[0].aligned_points)
        for tile_row_idx in range(rows_per_tile):
            pixel_row = []
            for tile in row:
                pixel_row += tile.aligned_points[tile_row_idx]
            full_image.append(pixel_row)
    
    return Tile(id=9999, points=full_image)
    

def find_dragons(image):
    
    # setup our dragon
    dragon = """                  # 
#    ##    ##    ###
 #  #  #  #  #  #   """
    
    dragon_pixels = dragon.split("\n")
    dragon_width = len(dragon_pixels[0])
    dragon_height = len(dragon_pixels)
    
    # we're going to search through all representations of the image
    for rep, _edge in image.iter_edges_with_key():
        
        match_count = 0
        
        # transform the image
        image.transform(facing="right", rep=rep)
        rendered = image.render().split("\n")
        # image.display()
        # print("---")
        # check our sizes
        image_width = len(rendered[0])
        image_height = len(rendered)
        
        # now walk the image looking for matches, and filling in any dragons we find
        for image_y in range(image_height - dragon_height):
            for image_x in range(image_width - dragon_width):
                
                # we're anchored at image_x image_y
                match = True
                for drg_y in range(dragon_height):
                    for drg_x in range(dragon_width):
                        drg_pix = dragon_pixels[drg_y][drg_x]
                        img_pix = rendered[image_y + drg_y][image_x + drg_x]
                        
                        # don't care about blanks
                        if drg_pix == " ":
                            continue
                            
                        if drg_pix != img_pix:
                            match = False
                            break
                    if not match:
                        break
                
                # we've got a match, fill it in
                if match:
                    match_count += 1
                    
                    for drg_y in range(dragon_height):
                        for drg_x in range(dragon_width):
                            drg_pix = dragon_pixels[drg_y][drg_x]
                            if drg_pix == "#":
                                rendered[image_y + drg_y] = rendered[image_y + drg_y][:image_x + drg_x] + "0" + rendered[image_y + drg_y][image_x + drg_x + 1:]

        if match_count > 1:
            print("---")
            print("rep(%s) has %d dragons" % (rep, match_count))            
            # print("\n".join(rendered))
            print("%d waves" % ("".join(rendered).count("#")))

            
if __name__ == "__main__":
    tiles = read_tiles(sys.argv[-1])
    find_connections(tiles)
    
    # for tile in tiles:
    #     print("Tile %d" % (tile.id,))
    #     print("  edge matches: ", tile.edge_match_ids)
    
    corners = [tile.id for tile in tiles if len(tile.edge_match_ids) == 2]
    print("Corners: ", corners)
    carry = 1
    for c in corners:
        carry *= c
    print("chksum: %d" % (carry,))
    
    arranged = arrange_tiles(tiles)
    variances = align_tiles(arranged)
    print("variance iterations")
    for arranged_immage in image_iterations(arranged, variances):
        image = merge_tiles(arranged)
        find_dragons(image)