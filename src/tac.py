# A Class for three AC (TAC) system stored in quadripole
class TAC:
    def __init__(self, temp_prefix="t", temp_suffix=""):
        self.temp_var = type("temp_var", (object,), {})()
        self.temp_var.count = 0
        self.temp_var.prefix = temp_prefix + "_"
        self.temp_var.suffix = "_" + temp_suffix if temp_suffix else ""

        self.table = []
        self.labels = []

    def new_temp(self):
        self.temp_var.count += 1
        return self.temp_var.prefix + str(self.temp_var.count) + self.temp_var.suffix

    def add(self, op, arg1, arg2, result):
        self.table.append([op, arg1, arg2, result])
    
    def add3(self, op, arg1, result):
        self.table.append([op, arg1, result])

    def add_label(self, label=""):
        if not label:
            label = "L" + str(len(self.labels))
        self.table.append([label + ":"])
        self.labels.append(label)
        return label

    def add_param(self, param):
        self.table.append(["PopFromStack", param])

    def tprint(self):
        for i in range(len(self.table)):
            print(self.table[i])
