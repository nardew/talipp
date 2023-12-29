import jsonpickle
from talipp.indicators import BB

if __name__ == "__main__":
    bb = BB(5, 1, list(range(0, 100, 2)))
    bb_pickled = jsonpickle.encode(bb, unpicklable = True)
    bb_unpickled = jsonpickle.decode(bb_pickled)

    print(f"Original BB:  {bb[-1]}")
    print(f"Unpickled BB: {bb_unpickled[-1]}")

    print('\nUpdating indicators...\n')

    bb.add(100)
    bb_unpickled.add(100)

    print(f"Updated BB:           {bb[-1]}")
    print(f"Updated unpickled BB: {bb_unpickled[-1]}")
