import sys


def read_public_keys(filename):
    with open(filename, "r", encoding="utf-8") as f:
        raw = f.read()
    
    return tuple([int(l) for l in raw.split("\n")])
    
    
# target: 5764801
# pow(7, 8, 20201227)
def transform(subject=7, loop_size=8):
    return pow(subject, loop_size, 20201227)
    # carry = 1
    # for _idx in range(loop_size):
    #     carry = (carry * subject) % 20201227
    # return carry


def derive_loop_size(public_key=None):
    """
    Derive a public key by testing the transform sizes
    """    
    loop_size = 1
    while transform(loop_size=loop_size) != public_key:
        loop_size += 1
    
    return loop_size
    

if __name__ == "__main__":
    
    # read in our public keys
    door_pub, card_pub = read_public_keys(sys.argv[-1])
    
    print("Public Keys")
    print("Card: ", card_pub)
    print("Door: ", door_pub)
    
    print("Loop Sizes")
    door_prv = derive_loop_size(public_key=door_pub)
    card_prv = derive_loop_size(public_key=card_pub)
    print("Card: ", card_prv)
    print("Door: ", door_prv)
    
    print("Encryption Key")
    print("Card: ", transform(subject=door_pub, loop_size=card_prv))
    print("Door: ", transform(subject=card_pub, loop_size=door_prv))