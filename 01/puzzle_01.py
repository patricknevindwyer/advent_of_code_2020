
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
            
            # skip adding to ourself
            if adx == bdx:
                continue
            
            anm = numbers[adx]
            bnm = numbers[bdx]
            
            if anm + bnm == 2020:
                yield (anm, bnm)


if __name__ == "__main__":
    
    for a, b in pairs("input_01.dat"):
        print("%d * %d == %d" % (a, b, a * b))
