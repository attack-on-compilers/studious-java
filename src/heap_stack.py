class HeapStackManager:
    def __init__(self, stack=16e6):
        self.heap = 0
        self.stack = int(stack)
        self.heaptable = []
        self.stacktable = []

    def allocheap(self, name, size):
        self.heap += size
        if self.heap > self.stack:
            raise Exception("Heap of memory")
        self.heaptable.append((name, self.heap - size, size))
        return self.heap - size

    def allocstack(self, name, size):
        self.stack -= size
        if self.stack < self.heap:
            raise Exception("Stack overflow")
        self.stacktable.append((name, self.stack, size))
        return self.stack

    def addSequence(self, name):
        self.stacktable.append(name)

    def removeSequence(self, name=None):
        if name is None:
            while type(self.stacktable[-1]) is not str:
                self.stacktable.pop()
        else:
            while self.stacktable[-1] != name:
                self.stacktable.pop()
        self.stacktable.pop()
        self.stack += self.stacktable[-1][2]

    def getSymbolStackInfo(self, name):
        for i in range(len(self.stacktable) - 1, -1, -1):
            if self.stacktable[i][0] == name:
                return self.stacktable[i][1], self.stacktable[i][2]
