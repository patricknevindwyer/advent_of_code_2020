import sys


def read_schedule(filename):
    
    with open(filename, "r", encoding="utf-8") as f:
        raw = f.read()
    
    ts, sched = raw.split("\n")
    
    return {
        "schedule": [int(s) for s in sched.replace("x", "0").split(",")]
    }


def crt(schedules):
    
    buses = [(idx, sched) for idx, sched in enumerate(schedules) if sched != 0]
    ts = 0
    lcm = 1
    for st, bus in buses:
        while (ts + st) % bus != 0:
            ts += lcm
        lcm *= bus
    return ts
    
        
if __name__ == "__main__":
    schedules = read_schedule(sys.argv[-1])
    synchro = crt(schedules["schedule"])
    print("Busses synchronize at %d minutes" % synchro)