import itertools
from heapq import heappush, heappop


REMOVED = '<removed-element>'      # placeholder for a removed element

class UpdatablePriorityQueue:
    def __init__(this):
        this.pq = []                         # list of entries arranged in a heap
        this.entry_finder = {}               # mapping of elements to entries
        this.counter = itertools.count()     # unique sequence count

    def add(this, element, priority=0):
        'Add a new element or update the priority of an existing element'
        if element in this.entry_finder:
            this.remove_element(element)
        count = next(this.counter)
        entry = [priority, count, element]
        this.entry_finder[element] = entry
        heappush(this.pq, entry)

    def remove_element(this, element):
        entry = this.entry_finder.pop(element)
        entry[-1] = REMOVED

    def pop(this):
        while this.pq:
            priority, count, element = heappop(this.pq)
            if element is not REMOVED:
                del this.entry_finder[element]
                return element
        raise KeyError('pop from an empty priority queue')

    def size(this):
        return len(this.entry_finder)

    def isEmpty(this):
        return this.size() == 0

