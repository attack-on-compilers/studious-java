import sys

class ActivationRecord:
    def __init__(self, num_params, num_locals):
        self.params = [0] * num_params
        self.return_value = 0
        self.old_sp = 0
        self.saved_registers = [0] * 4
        self.locals = [0] * num_locals
        self.return_address = 0

stack = []
pc = 0

def call(function_name, num_params):
    global sp, pc
    # push activation record onto stack
    ar = ActivationRecord(num_params, 10)
    ar.old_sp = len(stack) - num_params - 1 # store old stack pointer
    ar.return_address = pc + 1             # store return address
    stack.append(ar)

    # jump to function entry point
    pc = find_function(function_name)

def pushparam(value):
    global sp
    # push parameter onto stack
    ar = stack[-1]
    ar.params[sp - ar.old_sp - 1] = value

def return_(value):
    global sp, pc
    # set return value
    stack[-2].return_value = value

    # restore old stack pointer
    sp = stack[-2].old_sp

    # jump to return address
    pc = stack[-2].return_address

def find_function(function_name):
    # function lookup logic here
    pass


