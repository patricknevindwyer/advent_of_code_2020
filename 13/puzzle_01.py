import sys


def read_schedule(filename):
    
    with open(filename, "r", encoding="utf-8") as f:
        raw = f.read()
    
    ts, sched = raw.split("\n")
    
    return {
        "depart": int(ts),
        "schedule": [int(s) for s in sched.split(",") if s != "x"]
    }


def wait_time(depart, scheduled):
    if depart % scheduled == 0:
        return 0
    
    base = int(depart / scheduled) + 1
    return (base * scheduled) - depart


def find_a_bus(departure_time, schedules):
    
    waits = list(zip(schedules, [wait_time(departure_time, scheduled) for scheduled in schedules]))
    waits = sorted(waits, key=lambda w: w[1])
    return waits[0]


if __name__ == "__main__":
    schedules = read_schedule(sys.argv[-1])
    bus_and_wait = find_a_bus(schedules["depart"], schedules["schedule"])
    print("Bus %d has a wait of %d minutes" % bus_and_wait)
    print("chksum: %d" % (bus_and_wait[0] * bus_and_wait[1],))