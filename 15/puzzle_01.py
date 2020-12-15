import sys


def read_starting_numbers(filename, line=0):
    with open(filename, "r", encoding="utf-8") as f:
        raw = f.read()
    
    data = raw.split("\n")[line]
    
    return [int(d) for d in data.strip().split(",")]


def counting_game(starts, stop_at=2020):
    
    counting_index = 0
    
    # we match an index to a list of last seen indices
    seen_numbers = {}
    last_number = None
    
    while counting_index < stop_at:
        counting_index += 1

        # either pre-fill with our starting numbers, or pick a new speaking number
        if len(starts) > 0:
            speak_number = starts.pop(0)
        else:
            # take our last spoken number and figure out when
            # it was last seen
            if last_number not in seen_numbers:
                speak_number = 0
            else:
                prev_idxs = seen_numbers[last_number]
                if len(prev_idxs) == 2:
                    speak_number = prev_idxs[-1] - prev_idxs[0]
                else:
                    speak_number = 0
        
        # record our last spoken number
        last_number = speak_number
        
        # record that we've seen this number, keeping the last two entries
        if speak_number not in seen_numbers:
            seen_numbers[speak_number] = []
        seen_numbers[speak_number].append(counting_index)
        if len(seen_numbers[speak_number]) > 2:
            seen_numbers[speak_number] = seen_numbers[speak_number][1:]
        
    return last_number

if __name__ == "__main__":
    
    if len(sys.argv) == 3:
        case = int(sys.argv[-1])
        filename = sys.argv[-2]
    else:
        case = 0
        filename = sys.argv[-1]
    
    starts = read_starting_numbers(filename, line=case)
    print("Seeds: ", starts)
    print("The 2020th number is %d" % (counting_game(starts),))