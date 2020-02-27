import heapq
import itertools
import numpy

class PriorityQueue(object):

    _REMOVED = "<REMOVED>"
    COUNT = 0
    def __init__(self):
        self.heap = []
        self.entries = {}
        self.counter = itertools.count()

    def add(self, task, priority=0):
        """Add a new task or update the priority of an existing task"""
        for entry in self.entries.items():
            if not isinstance(entry[1][3], str):
                if (task == entry[1][3]).all():
                    self.remove(entry[0])

        count = next(self.counter)
        # weight = -priority since heap is a min-heap
        entry = [priority, count, PriorityQueue.COUNT, task]
        self.entries[PriorityQueue.COUNT] = entry
        PriorityQueue.COUNT += 1
        heapq.heappush(self.heap, entry)
        pass

    def remove(self, index):
        """ Mark the given task as REMOVED.

        Do this to avoid breaking heap-invariance of the internal heap.
        """
        entry = self.entries[index]
        entry[-1] = PriorityQueue._REMOVED
        pass

    def pop(self):
        """ Get task with highest priority.

        :return: Priority, Task with highest priority
        """
        while self.heap:
            weight, count, index, task = heapq.heappop(self.heap)
            # print(f"Priority: ----> {weight}")
            # print(f"Count: ----> {count}")
            # print(f"Index: ---> {index}")
            # print(f"Task: ----> {task}")
            if task is not PriorityQueue._REMOVED:
                del self.entries[index]
                return index, weight, task
        raise KeyError("The priority queue is empty")

    def peek(self):
        """ Check task with highest priority, without removing.

        :return: Priority, Task with highest priority
        """
        while self.heap:
            weight, count, index, task = self.heap[0]
            if task is PriorityQueue._REMOVED:
                heapq.heappop(self.heap)
            else:
                return weight, task

        return None

    def __str__(self):
        temp = [str(e) for e in self.heap if e[-1] is not PriorityQueue._REMOVED]
        return "[%s]" % ", ".join(temp)

    def empty(self):
        if len(self.entries):
            return False
        return True



def main():
    pq = PriorityQueue()
    arr1 = numpy.zeros((3,3), 'int')
    arr2 = numpy.zeros((3,3), 'int')
    arr3 = numpy.zeros((3,3), 'int')
    pq.add(arr1, 1)
    pq.add(arr2, 2)
    pq.add(arr3, 3)


    print(pq.empty())
    print(pq.pop())
    # print(pq.pop())
    print(pq.entries)




main()