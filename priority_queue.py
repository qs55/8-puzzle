import heapq
import itertools
import numpy

class PriorityQueue(object):

    _REMOVED = "<REMOVED>"
    COUNT = 0
    def __init__(self):
        self.heap = []
        self.entries = {}
        self.counter = 0

    def add(self, task, priority=0):
        """Add a new task or update the priority of an existing task"""
        for entry in self.entries.items():
            if not isinstance(entry[1][2], str):
                if (task.config == entry[1][2].config).all():
                    self.remove(entry[0])

        # weight = -priority since heap is a min-heap
        entry = [priority, PriorityQueue.COUNT, task]
        self.entries[PriorityQueue.COUNT] = entry
        PriorityQueue.COUNT += 1
        heapq.heappush(self.heap, entry)
        self.counter += 1
        pass

    def remove(self, index):
        """ Mark the given task as REMOVED.

        Do this to avoid breaking heap-invariance of the internal heap.
        """
        entry = self.entries[index]
        entry[-1] = PriorityQueue._REMOVED
        self.counter -= 1
        pass

    def pop(self):
        """ Get task with highest priority.

        :return: Priority, Task with highest priority
        """
        while self.heap:
            weight, index, task = heapq.heappop(self.heap)
            # print(f"Priority: ----> {weight}")
            # print(f"Count: ----> {count}")
            # print(f"Index: ---> {index}")
            # print(f"Task: ----> {task}")
            if task is not PriorityQueue._REMOVED:
                del self.entries[index]
                self.counter -= 1
                return task
        raise KeyError("The priority queue is empty")

    def peek(self):
        """ Check task with highest priority, without removing.

        :return: Priority, Task with highest priority
        """
        while self.heap:
            weight, index, task = self.heap[0]
            if task is PriorityQueue._REMOVED:
                heapq.heappop(self.heap)
            else:
                return weight, task

        return None

    def __str__(self):
        temp = [str(e) for e in self.heap if e[-1] is not PriorityQueue._REMOVED]
        return "[%s]" % ", ".join(temp)

    def empty(self):
        if self.counter:
            return False
        return True
