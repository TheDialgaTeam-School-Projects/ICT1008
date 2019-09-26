
class PQ:
    def __init__(self):
        self.HeapQueue = [0]
        self.size = 0

    # insert value into the PQ
    def insert(self, value):
        self.HeapQueue.append(value)
        self.size += 1
        self.swim(self.size)

    # return minimum value and delete it from the heap
    def deleteMin(self):
        minValue = self.HeapQueue[1]
        self.HeapQueue[1] = self.HeapQueue[self.size]
        self.size = self.size - 1
        self.HeapQueue.pop()
        self.sink(1)
        return minValue

    # return the minimum value
    def peekMin(self):
        return self.HeapQueue[1]

    # check is PQ is empty
    def isEmpty(self):
        if self.size == 0:
            return True
        else:
            return False

    # return certain value in the heap
    def contain(self, value):
        for x in range(0, self.size):
            index = x + 1
            if self.HeapQueue[index] == value:
                return True

        return False

    # swap with parent to maintain heap property
    def swim(self, index):
        while index / 2 > 0:
            if self.HeapQueue[index] < self.HeapQueue[index / 2]:
                self.HeapQueue[index/2], self.HeapQueue[index] = self.HeapQueue[index], self.HeapQueue[index/2]
            index = index / 2

    # swap with smallest child to maintain heap property
    def sink(self, index):
        while (index * 2) <= self.size:
            mc = self.minChild(index)
            if self.HeapQueue[index] > self.HeapQueue[mc]:
                self.HeapQueue[index], self.HeapQueue[mc] = self.HeapQueue[mc], self.HeapQueue[index]

            index = mc

    # return the index of the smallest child
    def minChild(self, index):
        # if index out of range
        if index * 2 + 1 > self.size:
            return index * 2
        else:
            # return the smallest child.
            if self.HeapQueue[index * 2] < self.HeapQueue[index * 2 + 1]:
                return index * 2
            else:
                return index * 2 + 1

    # clear priority queue
    def clear(self):
        self.HeapQueue = [0]
        self.size = 0

    # print priority queue
    def printPQ(self):
        print self.HeapQueue