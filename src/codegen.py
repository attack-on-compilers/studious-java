from pprint import pprint
from symbol_table import *
from lexer import *
from utils import *
from tac import *
import string
import secrets


class Register:
    # these registers mapped to None and 0 initially (for no initial stored values and start time)
    regs = dict.fromkeys(["%rbx", "%r10", "%r11", "%r12", "%r13", "%r14"], [None, 0])
    heap_reg = dict.fromkeys(["%r15"], [None, 0])

    # registers for arguments
    argument_registers = dict(zip(map(str, range(6)), ["%rdi", "%rsi", "%rdx", "%rcx", "%r8", "%r9"]))

    RIP_reg = None
    RBP_reg = None
    count = 0
    locations = dict()

    super_registers = ["%rax", "%rbx", "%rcx", "%rdx", "%r8", "%r9", "%r10", "%r11", "%r12", "%r13", "%r14", "%r15"]
    sub_registers = ["%al", "%bl", "%cl", "%dl", "%r8b", "%r9b", "%r10b", "%r11b", "%r12b", "%r13b", "%r14b", "%r15b"]

    last_byte_map = dict(zip(super_registers, sub_registers))

    def __init__(self):
        print("Hola!")

    def lru_policy(self):
        ## use the lru policy
        # get the register with the least recent use
        # return the register
        setmin = 1e10 + 5
        for key in self.regs:
            if self.regs[key][1] < setmin:
                setmin = self.regs[key][1]
                lru_reg = key
        return lru_reg

    def write_back(self, arr=None, flush=True):
        # write back the value to memory
        instructions = []
        if flush:
            instructions.append("#" + str(self.regs))
        for r, v in self.regs.items():
            if arr is not None and r not in arr:
                continue
            if v[0]:
                loc = self.locations.get(v[0], [None, ""])[1]
                if loc != "Tempo":
                    instructions.append(f"\tmov {r}, {loc}")
                if flush:
                    self.locations.pop(v[0], None)
                    self.regs[r] = [None, 0]
        return instructions

    def get_register(self, v=None):
        v = "".join(secrets.choice(string.ascii_lowercase) for _ in range(8)) if v is None else v
        instructions = []
        if v in self.locations and self.locations[v][0] is not None:
            reg = self.locations[v][0]
            # self.regs[reg][1] = self.count
            self.count = self.count + 1
            return reg, []

        self.count = self.count + 1
        reg = self.lru_policy()
        # instructions = self.write_back([reg], True)
        self.regs[reg] = v, self.count

        if v not in self.locations:
            self.locations[v] = [reg, "Tempo"]
        else:
            self.locations[v][0] = reg
            instructions.append(f"  mov {self.locations[v][1]}, {reg}")
        return reg, instructions


class ASM:
    def __init__(self):
        self.instructions = []

    def tac_to_x86_mapping(self, tac):
        instructions = []
        reg = Register()
        tac = [
            ["test_13:"],
            ["BeginFunction", "test_13_main:"],
            ["PopFromStack", "test_13_main_args"],
            ["stackpoint++", 8],
            ["=", "10", "test_13_main_a"],
            ["stackpoint++", 8],
            ["=", "5", "test_13_main_b"],
            ["stackpoint++", 8],
            ["-", "test_13_main_a", "test_13_main_b", "__t_3"],
            ["+", "__t_3", "5", "__t_2"],
            ["-", "__t_2", "7", "__t_1"],
            ["=", "__t_1", "test_13_main_c"],
            ["stackpoint--", 40],
            ["stackpoint--", 16],
            ["myClass:"],
            ["stackpoint++", 8],
            ["stackpoint++", 8],
            ["stackpoint++", 8],
            ["stackpoint--", 56],
        ]
        # Loop through each TAC instruction
        for t in tac:
            if len(t) == 4:
                op, arg1, arg2, res = t[0], t[1], t[2], t[3]

                if op == "+":
                    # Load arg1 into a register
                    reg1, load1 = reg.get_register(arg1)
                    instructions.extend(load1)

                    # Load arg2 into a register
                    reg2, load2 = reg.get_register(arg2)
                    instructions.extend(load2)

                    reg3, load3 = reg.get_register(res)
                    instructions.extend(load3)

                    # Add the values and store the result in res
                    instructions.append(f"  add {reg1}, {reg2}")
                    instructions.append(f"  mov {reg3}, {reg1}")

                elif op == "-":
                    # Load arg1 into a register
                    reg1, load1 = reg.get_register(arg1)
                    instructions.extend(load1)

                    # Load arg2 into a register
                    reg2, load2 = reg.get_register(arg2)
                    instructions.extend(load2)

                    reg3, load3 = reg.get_register(res)
                    instructions.extend(load3)

                    # Subtract the values and store the result in res
                    instructions.append(f"  sub {reg1}, {reg2}")
                    instructions.append(f"  mov {reg3}, {reg1}")

                elif op == "*":
                    # Load arg1 into a register
                    reg1, load1 = reg.get_register(arg1)
                    instructions.extend(load1)

                    # Load arg2 into a register
                    reg2, load2 = reg.get_register(arg2)
                    instructions.extend(load2)

                    reg3, load3 = reg.get_register(res)
                    instructions.extend(load3)

                    # Multiply the values and store the result in res
                    instructions.append(f"  imul {reg1}, {reg2}")
                    instructions.append(f"  mov {reg3}, {reg1}")

                elif op == "/":
                    # Load arg1 into a register
                    reg1, load1 = reg.get_register(arg1)
                    instructions.extend(load1)

                    # Load arg2 into a register
                    reg2, load2 = reg.get_register(arg2)
                    instructions.extend(load2)

                    reg3, load3 = reg.get_register(res)
                    instructions.extend(load3)

                    # Divide the values and store the result in res
                    instructions.append(f"  mov {reg3}, {reg1}")
                    instructions.append(f"  cqo")
                    instructions.append(f"  idiv {reg2}")
                    # check completeness one more statement may be needded

                elif op == "%":
                    # Load arg1 into a register
                    reg1, load1 = reg.get_register(arg1)
                    instructions.extend(load1)

                    # Load arg2 into a register
                    reg2, load2 = reg.get_register(arg2)
                    instructions.extend(load2)

                    reg3, load3 = reg.get_register(res)
                    instructions.extend(load3)

                    # Divide the values and store the result in res
                    instructions.append(f"  mov {reg3}, {reg1}")
                    instructions.append(f"  cqo")
                    instructions.append(f"  idiv {reg2}")
                    # check completeness one more statement may be needded

                elif op == ">":
                    # Load arg1 into a register
                    reg1, load1 = reg.get_register(arg1)
                    instructions.extend(load1)

                    # Load arg2 into a register
                    reg2, load2 = reg.get_register(arg2)
                    instructions.extend(load2)

                    reg3, load3 = reg.get_register(res)
                    instructions.extend(load3)

                    instructions.append(f"  cmp {reg1}, {reg2}")
                    instructions.append(f"  setg {reg3}")

                elif op == "<":
                    # Load arg1 into a register
                    reg1, load1 = reg.get_register(arg1)
                    instructions.extend(load1)

                    # Load arg2 into a register
                    reg2, load2 = reg.get_register(arg2)
                    instructions.extend(load2)

                    reg3, load3 = reg.get_register(res)
                    instructions.extend(load3)

                    instructions.append(f"  cmp {reg1}, {reg2}")
                    instructions.append(f"  setl {reg3}")

                elif op == ">=":
                    # Load arg1 into a register
                    reg1, load1 = reg.get_register(arg1)
                    instructions.extend(load1)

                    # Load arg2 into a register
                    reg2, load2 = reg.get_register(arg2)
                    instructions.extend(load2)

                    reg3, load3 = reg.get_register(res)
                    instructions.extend(load3)

                    instructions.append(f"  cmp {reg1}, {reg2}")
                    instructions.append(f"  setge {reg3}")

                elif op == "<=":
                    # Load arg1 into a register
                    reg1, load1 = reg.get_register(arg1)
                    instructions.extend(load1)

                    # Load arg2 into a register
                    reg2, load2 = reg.get_register(arg2)
                    instructions.extend(load2)

                    reg3, load3 = reg.get_register(res)
                    instructions.extend(load3)

                    instructions.append(f"  cmp {reg1}, {reg2}")
                    instructions.append(f"  setle {reg3}")

                elif op == "==":
                    # Load arg1 into a register
                    reg1, load1 = reg.get_register(arg1)
                    instructions.extend(load1)

                    # Load arg2 into a register
                    reg2, load2 = reg.get_register(arg2)
                    instructions.extend(load2)

                    reg3, load3 = reg.get_register(res)
                    instructions.extend(load3)

                    instructions.append(f"  cmp {reg1}, {reg2}")
                    instructions.append(f"  sete {reg3}")

                elif op == "!=":
                    # Load arg1 into a register
                    reg1, load1 = reg.get_register(arg1)
                    instructions.extend(load1)

                    # Load arg2 into a register
                    reg2, load2 = reg.get_register(arg2)
                    instructions.extend(load2)

                    reg3, load3 = reg.get_register(res)
                    instructions.extend(load3)

                    instructions.append(f"  cmp {reg1}, {reg2}")
                    instructions.append(f"  setne {reg3}")

                elif op == "&&":
                    # Load arg1 into a register
                    reg1, load1 = reg.get_register(arg1)
                    instructions.extend(load1)

                    # Load arg2 into a register
                    reg2, load2 = reg.get_register(arg2)
                    instructions.extend(load2)

                    reg3, load3 = reg.get_register(res)
                    instructions.extend(load3)

                    instructions.append(f"  and {reg1}, {reg2}")
                    instructions.append(f"  mov {reg3}, {reg1}")

                elif op == "||":
                    # Load arg1 into a register
                    reg1, load1 = reg.get_register(arg1)
                    instructions.extend(load1)

                    # Load arg2 into a register
                    reg2, load2 = reg.get_register(arg2)
                    instructions.extend(load2)

                    reg3, load3 = reg.get_register(res)
                    instructions.extend(load3)

                    instructions.append(f"  or {reg1}, {reg2}")
                    instructions.append(f"  mov {reg3}, {reg1}")

                elif op == "^":
                    # Load arg1 into a register
                    reg1, load1 = reg.get_register(arg1)
                    instructions.extend(load1)

                    # Load arg2 into a register
                    reg2, load2 = reg.get_register(arg2)
                    instructions.extend(load2)

                    reg3, load3 = reg.get_register(res)
                    instructions.extend(load3)

                    instructions.append(f"  xor {reg1}, {reg2}")
                    instructions.append(f"  mov {reg3}, {reg1}")

                elif op == ">>":
                    # Load arg1 into a register
                    reg1, load1 = reg.get_register(arg1)
                    instructions.extend(load1)

                    # Load arg2 into a register
                    reg2, load2 = reg.get_register(arg2)
                    instructions.extend(load2)

                    reg3, load3 = reg.get_register(res)
                    instructions.extend(load3)

                    instructions.append(f"  mov {reg3}, {reg1}")
                    instructions.append(f"  shr {reg3}, {reg2}")

                elif op == "<<":
                    # Load arg1 into a register
                    reg1, load1 = reg.get_register(arg1)
                    instructions.extend(load1)

                    # Load arg2 into a register
                    reg2, load2 = reg.get_register(arg2)
                    instructions.extend(load2)

                    reg3, load3 = reg.get_register(res)
                    instructions.extend(load3)

                    instructions.append(f"  mov {reg3}, {reg1}")
                    instructions.append(f"  shl {reg3}, {reg2}")

        self.instructions = instructions


    def print(self):
        for instruction in self.instructions:
            print(instruction)
    def fprint(self, file):
        for instruction in self.instructions:
            file.write(instruction + "\n")  

if __name__ == "__main__":
    asm = ASM()
    asm.tac_to_x86_mapping(None)
    asm.print()
