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

    rbp = dict.fromkeys(["%rbp"], [None, 0])
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
        self.count = self.count + 1
        reg = self.lru_policy()
        # instructions = self.write_back([reg], True)
        self.regs[reg] = v, self.count

        if v not in self.locations:
            self.locations[v] = [reg, parse_tac_arg(v)]
        #     self.locations[v] = [reg, "Tempo"]
        # else:
        self.locations[v][0] = reg
        instructions.append(f"  mov {self.locations[v][1]}, {reg}")
        return reg, instructions


def parse_tac_arg(field):
    spl = field.split("#")
    if len(spl) == 1:
        return "#" + field
    offset = int(spl[1])
    offset = -1 * offset
    return f"{offset}(%rbp)"

class GAS:
    def __init__(self):
        self.instructions = []

    def tac_to_x86_mapping(self, tac):
        instructions = []
        reg = Register()
        # tac = TAC()
        # tac.table = [
        #     ['=', '5', 'test_13_main_block1_x#56'],
        #     ['=', '6', 'test_13_main_block1_y#64'],
        #     ['+', 'test_13_main_block1_x#56', 'test_13_main_block1_y#64', '__t_18#240'],
        #     ['-', 'test_13_main_block1_x#56', 'test_13_main_block1_y#64', '__t_18#240'],
        #     ['=', '__t_18#240', 'test_13_main_block1_z#72']
        # ]
        # Loop through each TAC instruction
        for t in tac.table:
            if len(t) == 4:
                op, arg1, arg2, res = t[0], t[1], t[2], t[3]

                if op == "+":
                    # Load arg1 into a register
                    reg1, load1 = reg.get_register(arg1)
                    instructions.extend(load1)

                    # Load arg2 into a register
                    reg2, load2 = reg.get_register(arg2)
                    instructions.extend(load2)

                    # reg3, load3 = reg.get_register(res)
                    # instructions.extend(load3)

                    
                    # Add the values and store the result in res
                    instructions.append(f"  add {reg1}, {reg2}")

                    res = parse_tac_arg(t[3])
                    instructions.append(f"  mov {reg2}, {res}")

                elif op == "-":
                    # Load arg1 into a register
                    reg1, load1 = reg.get_register(arg1)
                    instructions.extend(load1)

                    # Load arg2 into a register
                    reg2, load2 = reg.get_register(arg2)
                    instructions.extend(load2)

                    # reg3, load3 = reg.get_register(res)
                    # instructions.extend(load3)

                    # Subtract the values and store the result in res
                    instructions.append(f"  sub {reg1}, {reg2}")
                    g = -1*(int)(t[3].split("#")[-1])

                    instructions.append(f"  mov {reg2}, {g}(%rbp)")

                elif op == "*":
                    # Load arg1 into a register
                    reg1, load1 = reg.get_register(arg1)
                    instructions.extend(load1)

                    # Load arg2 into a register
                    reg2, load2 = reg.get_register(arg2)
                    instructions.extend(load2)

                    # reg3, load3 = reg.get_register(res)
                    # instructions.extend(load3)

                    # Multiply the values and store the result in res
                    instructions.append(f"  imul {reg1}, {reg2}")

                    res = parse_tac_arg(t[3])
                    instructions.append(f"  mov {reg2}, {res}")

                elif op == "/":
                    # Load arg1 into a register
                    reg1, load1 = reg.get_register(arg1)
                    instructions.extend(load1)

                    # Load arg2 into a register
                    reg2, load2 = reg.get_register(arg2)
                    instructions.extend(load2)

                    # reg3, load3 = reg.get_register(res)
                    # instructions.extend(load3)

                    # Divide the values and store the result in res
                    g = -1*(int)(t[3].split("#")[-1])

                    instructions.append(f"  mov {reg1}, {g}(%rbp)")

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

                    # reg3, load3 = reg.get_register(res)
                    # instructions.extend(load3)

                    # Divide the values and store the result in res
                    g = -1*(int)(t[3].split("#")[-1])

                    instructions.append(f"  mov {reg1}, {g}(%rbp)")
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

                    # reg3, load3 = reg.get_register(res)
                    # instructions.extend(load3)

                    instructions.append(f"  cmp {reg1}, {reg2}")

                    g = -1*(int)(t[3].split("#")[-1])

                    instructions.append(f"  setg {g}(%rbp)")

                elif op == "<":
                    # Load arg1 into a register
                    reg1, load1 = reg.get_register(arg1)
                    instructions.extend(load1)

                    # Load arg2 into a register
                    reg2, load2 = reg.get_register(arg2)
                    instructions.extend(load2)

                    # reg3, load3 = reg.get_register(res)
                    # instructions.extend(load3)

                    instructions.append(f"  cmp {reg1}, {reg2}")
                    g = -1*(int)(t[3].split("#")[-1])

                    instructions.append(f"  setl {g}(%rbp)")

                elif op == ">=":
                    # Load arg1 into a register
                    reg1, load1 = reg.get_register(arg1)
                    instructions.extend(load1)

                    # Load arg2 into a register
                    reg2, load2 = reg.get_register(arg2)
                    instructions.extend(load2)

                    # reg3, load3 = reg.get_register(res)
                    # instructions.extend(load3)

                    instructions.append(f"  cmp {reg1}, {reg2}")
                    g = -1*(int)(t[3].split("#")[-1])

                    instructions.append(f"  setge {g}(%rbp)")

                elif op == "<=":
                    # Load arg1 into a register
                    reg1, load1 = reg.get_register(arg1)
                    instructions.extend(load1)

                    # Load arg2 into a register
                    reg2, load2 = reg.get_register(arg2)
                    instructions.extend(load2)

                    # reg3, load3 = reg.get_register(res)
                    # instructions.extend(load3)

                    instructions.append(f"  cmp {reg1}, {reg2}")
                    g = -1*(int)(t[3].split("#")[-1])

                    instructions.append(f"  setle {g}(%rbp)")

                elif op == "==":
                    # Load arg1 into a register
                    reg1, load1 = reg.get_register(arg1)
                    instructions.extend(load1)

                    # Load arg2 into a register
                    reg2, load2 = reg.get_register(arg2)
                    instructions.extend(load2)

                    # reg3, load3 = reg.get_register(res)
                    # instructions.extend(load3)

                    instructions.append(f"  cmp {reg1}, {reg2}")
                    g = -1*(int)(t[3].split("#")[-1])

                    instructions.append(f"  sete {g}(%rbp)")

                elif op == "!=":
                    # Load arg1 into a register
                    reg1, load1 = reg.get_register(arg1)
                    instructions.extend(load1)

                    # Load arg2 into a register
                    reg2, load2 = reg.get_register(arg2)
                    instructions.extend(load2)

                    # reg3, load3 = reg.get_register(res)
                    # instructions.extend(load3)

                    instructions.append(f"  cmp {reg1}, {reg2}")
                    g = -1*(int)(t[3].split("#")[-1])

                    instructions.append(f"  setne {g}(%rbp)")

                elif op == "&&":
                    # Load arg1 into a register
                    reg1, load1 = reg.get_register(arg1)
                    instructions.extend(load1)

                    # Load arg2 into a register
                    reg2, load2 = reg.get_register(arg2)
                    instructions.extend(load2)

                    # reg3, load3 = reg.get_register(res)
                    # instructions.extend(load3)

                    instructions.append(f"  and {reg1}, {reg2}")
                    
                    g = -1*(int)(t[3].split("#")[-1])

                    instructions.append(f"  mov {reg2}, {g}(%rbp)")

                elif op == "||":
                    # Load arg1 into a register
                    reg1, load1 = reg.get_register(arg1)
                    instructions.extend(load1)

                    # Load arg2 into a register
                    reg2, load2 = reg.get_register(arg2)
                    instructions.extend(load2)

                    # reg3, load3 = reg.get_register(res)
                    # instructions.extend(load3)

                    instructions.append(f"  or {reg1}, {reg2}")
                    
                    g = -1*(int)(t[3].split("#")[-1])

                    instructions.append(f"  mov {reg2}, {g}(%rbp)")

                elif op == "^":
                    # Load arg1 into a register
                    reg1, load1 = reg.get_register(arg1)
                    instructions.extend(load1)

                    # Load arg2 into a register
                    reg2, load2 = reg.get_register(arg2)
                    instructions.extend(load2)

                    # reg3, load3 = reg.get_register(res)
                    # instructions.extend(load3)

                    instructions.append(f"  xor {reg1}, {reg2}")
                    g = -1*(int)(t[3].split("#")[-1])

                    instructions.append(f"  mov {reg2}, {g}(%rbp)")

                elif op == ">>":
                    # Load arg1 into a register
                    reg1, load1 = reg.get_register(arg1)
                    instructions.extend(load1)

                    # Load arg2 into a register
                    reg2, load2 = reg.get_register(arg2)
                    instructions.extend(load2)

                    # reg3, load3 = reg.get_register(res)
                    # instructions.extend(load3)

                    g = -1*(int)(t[3].split("#")[-1])

                    instructions.append(f"  mov {reg1}, {g}(%rbp)")

                    instructions.append(f"  shr {reg2}, {g}(%rbp)")

                elif op == "<<":
                    # Load arg1 into a register
                    reg1, load1 = reg.get_register(arg1)
                    instructions.extend(load1)

                    # Load arg2 into a register
                    reg2, load2 = reg.get_register(arg2)
                    instructions.extend(load2)

                    # reg3, load3 = reg.get_register(res)
                    # instructions.extend(load3)

                    g = -1*(int)(t[3].split("#")[-1])

                    instructions.append(f"  mov {reg1}, {g}(%rbp)")

                    instructions.append(f"  shl {reg2}, {g}(%rbp)")

            if t[0] == "BeginFunction":
                funcname = t[1][:-1]
                instructions.append(t[1])
                instructions.append("  pushq %rbp")
                instructions.append("  movq %rsp, %rbp")
                instructions.append(f"  subq ${tac.size[funcname]}, %rsp")
            
            if t[0] == "Return":
                if len(t) == 2:
                    reg1, load1 = reg.get_register(t[1])
                    instructions.extend(load1)
                    instructions.append(f"  mov {reg1}, %rax")
                instructions.append("  leave")
                instructions.append("  ret")
            if len(t) == 1 and t[0][0] == "." and t[0][-1] == ":":
                instructions.append(t[0])
            
        self.instructions = instructions


    def tprint(self):
        for instruction in self.instructions:
            print(instruction)
    def fprint(self, file):
        for instruction in self.instructions:
            file.write(instruction + "\n")  

if __name__ == "__main__":
    asm = GAS()
    asm.tac_to_x86_mapping(None)
    asm.tprint()
