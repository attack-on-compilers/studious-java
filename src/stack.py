class StackManager:
    def __init__(self, stack=8e6):
        self.stack = int(stack)
        self.stacktable = []

    def allocStack(self, name, size):
        self.stack -= size
        if self.stack < self.heap:
            raise Exception("Stack overflow")
        self.stacktable.append((name, self.stack, size))
        return self.stack, size

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
        self.stack = self.stacktable[-1][1]

    def getSymbolInfo(self, name):
        for i in range(len(self.stacktable) - 1, -1, -1):
            if self.stacktable[i][0] == name:
                return self.stacktable[i][1], self.stacktable[i][2], self.stack - self.stacktable[i][1]
