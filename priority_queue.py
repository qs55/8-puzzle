import heapq


class PriorityQueue(object):

    _REMOVED = "<REMOVED>"
    COUNT = 0

    def __init__(self):
        self.heap = []
        self.entries = {}
        self.counter = 0
        self.removed = 0

    def add(self, task, priority=0):
        for entry in self.entries.items():
            if not isinstance(entry[1][2], str):
                if (task.config == entry[1][2].config).all():
                    self.remove(entry[0])
                    self.removed += 1

        entry = [priority, PriorityQueue.COUNT, task]
        self.entries[PriorityQueue.COUNT] = entry
        PriorityQueue.COUNT += 1
        heapq.heappush(self.heap, entry)
        self.counter += 1
        pass

    def remove(self, index):
        entry = self.entries[index]
        entry[-1] = PriorityQueue._REMOVED
        self.counter -= 1
        pass

    def pop(self):
        while self.heap:
            weight, index, task = heapq.heappop(self.heap)
            if task is not PriorityQueue._REMOVED:
                del self.entries[index]
                self.counter -= 1
                return task
        raise KeyError("The priority queue is empty")

    def empty(self):
        if self.counter:
            return False
        return True
