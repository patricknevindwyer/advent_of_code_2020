
def pairs(input_file):
    """
    Open the input file, find any pairs of numbers summing to 2020, yield
    each result as an iterator.
    """
    numbers = []
    
    with open(input_file, "r", encoding="utf-8") as input:
        raw = input.read()
        
    for line in raw.split():
        numbers.append(int(line.strip()))
    
    # brute force, hooray
    for adx in range(len(numbers)):
        for bdx in range(len(numbers)):
            for cdx in range(len(numbers)):
                
                # skip adding to ourself
                if adx == bdx or bdx == cdx or adx == cdx:
                    continue
            
                anm = numbers[adx]
                bnm = numbers[bdx]
                cnm = numbers[cdx]
                
                if anm + bnm + cnm == 2020:
                    yield (anm, bnm, cnm)


if __name__ == "__main__":
    
    for a, b, c in pairs("input_01.dat"):
        print("%d * %d * %d == %d" % (a, b, c, a * b * c))
