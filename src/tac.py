# A Class for three AC (TAC) system stored in quadripole
class TAC:
    def __init__(self, temp_prefix="__t"):
        self.temp_var = type("temp_var", (object,), {})()
        self.temp_var.count = 0
        self.temp_var.prefix = temp_prefix + "_"
        self.table = []
        self.labels = []

    def new_temp(self):
        self.temp_var.count += 1
        return self.temp_var.prefix + str(self.temp_var.count)

    def add(self, op, arg1, arg2, result):
        self.table.append([op, arg1, arg2, result])

    def add3(self, op, arg1, result):
        self.table.append([op, arg1, result])

    def add_call(self, func, result):
        self.table.append(["ProcCall", func, result])

    def add_epilouge(self):
        self.table.append(["=", "stackpoint", "basepoint"])

    def pop_param(self, param):
        self.table.append(["PopFromStack", param])

    def push_param(self, param, size=None):
        if size is not None:
            self.table.append(["stackpoint++", size])
        self.table.append(["PushToStack", param])

    def add_return(self, result):
        self.table.append(["Return", result])

    def cond_jump(self, cond, label):
        self.table.append(["CondJump", cond, label])

    def jump(self, label):
        self.table.append(["Jump", label])

    def gen_label(self):
        label = "L" + str(len(self.labels))
        self.labels.append(label)
        return label

    def alloc_mem(self, size, result_addr):
        self.table.append(["allocmem", size, result_addr])

    def alloc_stack(self, size):
        self.table.append(["stackpoint++", size])

    def free_stack(self, size):
        self.table.append(["stackpoint--", size])

    def add_entry(self, entry):
        self.table.append(entry)

    def add_label(self, label=""):
        if not label:
            label = "L" + str(len(self.labels))
        self.table.append([label + ":"])
        self.labels.append(label)
        return label
    
    def add_function(self, label=""):
        if not label:
            label = "L" + str(len(self.labels))
        self.table.append(["BeginFunction", label + ":"])
        self.labels.append(label)
        return label

    def tprint(self):
        for i in range(len(self.table)):
            print(self.table[i])
