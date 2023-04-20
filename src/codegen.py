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

    def get_register(self, v=None, r=None):
        v = "".join(secrets.choice(string.ascii_lowercase) for _ in range(8)) if v is None else v
        instructions = []
        self.count = self.count + 1
        if r is not None:
            reg = r
        else:
            reg = self.lru_policy()
        # instructions = self.write_back([reg], True)
        self.regs[reg] = v, self.count

        if v not in self.locations:
            self.locations[v] = [reg, parse_tac_arg(v)]
        self.locations[v][0] = reg
        instructions.append(f"  movq {self.locations[v][1]}, {reg}")
        return reg, instructions


def parse_tac_arg(field):
    global reg
    global instructions
    if type(field) == int:
        return f"${field}"
    if field[-1] == ")":
        reg1, load = reg.get_register(field[10:-1])
        instructions.extend(load)
        instructions.append(f"  movq {parse_tac_arg(field[10:-1])}, {reg1}")
        return "(" + reg1 + ")"
    spl = field.split("#")
    if len(spl) == 1:
        return "$" + field
    offset = int(spl[1])
    offset = -1 * offset
    return f"{offset}(%rbp)"


class GAS:
    def __init__(self):
        self.x86instructions = []
        self.constants = [".LC0:", '  .string "%d"', ".LC1:", '  .string "\\n"']

    def add_constant(self, c):
        label = f".LC{len(self.constants) // 2}"
        self.constants.append(label + ":")
        self.constants.append(f"  .string {c}")
        return label

    def tac_to_x86_mapping(self, tac):
        global reg
        reg = Register()
        for t in tac.table:
            global instructions
            instructions = []
            if len(t) == 4:
                op, arg1, arg2, res = t[0], t[1], t[2], t[3]

                if op == "+":
                    # Load arg1 into a register
                    reg1, load1 = reg.get_register(arg1)
                    instructions.extend(load1)

                    # Load arg2 into a register
                    reg2, load2 = reg.get_register(arg2)
                    instructions.extend(load2)

                    # Add the values and store the result in res
                    instructions.append(f"  addq {reg1}, {reg2}")

                    res = parse_tac_arg(t[3])
                    instructions.append(f"  movq {reg2}, {res}")

                elif op == "-":
                    # Load arg1 into a register
                    # reg1, load1 = reg.get_register(arg1)
                    # instructions.extend(load1)

                    # # Load arg2 into a register
                    # reg2, load2 = reg.get_register(arg2)
                    # instructions.extend(load2)

                    # Add the values and store the result in res
                    instructions.append(f"  movq {parse_tac_arg(arg1)}, %rax")

                    instructions.append(f"  subq {parse_tac_arg(arg2)}, %rax")

                    res = parse_tac_arg(t[3])
                    instructions.append(f"  movq %rax, {res}")

                elif op == "*":
                    instructions.append(f"  movq {parse_tac_arg(arg1)}, %rax")

                    # Multiply the values and store the result in res
                    instructions.append(f"  imulq {parse_tac_arg(arg2)}, %rax")

                    res = parse_tac_arg(t[3])
                    instructions.append(f"  movq %rax, {res}")

                elif op == "/":
                    # Divide the values and store the result in res

                    reg1, load1 = reg.get_register(arg1, "%rax")
                    instructions.extend(load1)
                    
                    #instructions.append(f"  movq {parse_tac_arg(arg1)}, %rax")

                    instructions.append(f"  cqto")

                    reg2, load2 = reg.get_register(arg2)
                    instructions.extend(load2)

                    instructions.append(f"  idivq {reg2}")
                    res = parse_tac_arg(t[3])

                    instructions.append(f"  movq %rax, {res}")
                    # check completeness one more statement may be needded

                elif op == "%":
                    # Load arg1 into a register
                    # instructions.append(f"  movq {parse_tac_arg(arg1)}, %rax")
                    # instructions.append(f"  cqto")
                    # instructions.append(f"  idivq {parse_tac_arg(arg2)}")
                    # res = parse_tac_arg(t[3])


                    reg1, load1 = reg.get_register(arg1, "%rax")
                    instructions.extend(load1)
                    
                    #instructions.append(f"  movq {parse_tac_arg(arg1)}, %rax")

                    instructions.append(f"  cqto")

                    reg2, load2 = reg.get_register(arg2)
                    instructions.extend(load2)

                    instructions.append(f"  idivq {reg2}")
                    res = parse_tac_arg(t[3])


                    instructions.append(f"  movq %rdx, {res}")
                    # check completeness one more statement may be needded

                elif op == ">":
                    instructions.append(f"  movq {parse_tac_arg(arg1)}, %rax")
                    instructions.append(f"  cmpq {parse_tac_arg(arg2)}, %rax")
                    instructions.append(f"  setg %al")
                    instructions.append(f"  movzbl %al, %eax")
                    res = parse_tac_arg(t[3])
                    instructions.append(f"  movq %rax, {res}")

                elif op == "<":
                    # Load arg1 into a register
                    instructions.append(f"  movq {parse_tac_arg(arg1)}, %rax")
                    instructions.append(f"  cmpq {parse_tac_arg(arg2)}, %rax")
                    instructions.append(f"  setl %al")
                    instructions.append(f"  movzbl %al, %eax")
                    res = parse_tac_arg(t[3])
                    instructions.append(f"  movq %rax, {res}")

                elif op == ">=":
                    instructions.append(f"  movq {parse_tac_arg(arg1)}, %rax")
                    instructions.append(f"  cmpq {parse_tac_arg(arg2)}, %rax")
                    instructions.append(f"  setge %al")
                    instructions.append(f"  movzbl %al, %eax")
                    res = parse_tac_arg(t[3])
                    instructions.append(f"  movq %rax, {res}")

                elif op == "<=":
                    instructions.append(f"  movq {parse_tac_arg(arg1)}, %rax")
                    instructions.append(f"  cmpq {parse_tac_arg(arg2)}, %rax")
                    instructions.append(f"  setle %al")
                    instructions.append(f"  movzbl %al, %eax")
                    res = parse_tac_arg(t[3])
                    instructions.append(f"  movq %rax, {res}")

                elif op == "==":
                    instructions.append(f"  movq {parse_tac_arg(arg1)}, %rax")
                    instructions.append(f"  cmpq {parse_tac_arg(arg2)}, %rax")
                    instructions.append(f"  sete %al")
                    instructions.append(f"  movzbl %al, %eax")
                    res = parse_tac_arg(t[3])
                    instructions.append(f"  movq %rax, {res}")

                elif op == "!=":
                    instructions.append(f"  movq {parse_tac_arg(arg1)}, %rax")
                    instructions.append(f"  cmpq {parse_tac_arg(arg2)}, %rax")
                    instructions.append(f"  setne %al")
                    instructions.append(f"  movzbl %al, %eax")
                    res = parse_tac_arg(t[3])
                    instructions.append(f"  movq %rax, {res}")

            if t[0] == "BeginFunction":
                funcname = t[1][:-1]
                if funcname.endswith("main"):
                    instructions.append("  .globl main")
                    instructions.append("main:")
                else:
                    instructions.append(t[1])
                fsize = tac.size[funcname]
                # align to 16 bytes
                if fsize % 16 != 0:
                    fsize += 16 - fsize % 16
                instructions.append("  pushq %rbp")
                instructions.append("  movq %rsp, %rbp")
                instructions.append(f"  subq ${fsize}, %rsp")
            if t[0] == "Return":
                if len(t) == 2:
                    reg1, load1 = reg.get_register(t[1])
                    instructions.extend(load1)
                    instructions.append(f"  mov {reg1}, %rax")
                instructions.append("  leave")
                instructions.append("  ret")
            if len(t) == 1 and t[0][0] == "." and t[0][-1] == ":":
                instructions.append(t[0])
            if t[0] == "FunctionInvocation":
                instructions.append(f"  subq $8, %rsp")
            if t[0] == "PushToStack":
                instructions.append(f"  pushq {parse_tac_arg(t[1])}")
            if t[0] == "ProcCall":
                instructions.append(f"  call {t[1]}")
                instructions.append(f"  movq %rax, {parse_tac_arg(t[2])}")
            if t[0] == "addrsp":
                instructions.append(f"  addq ${t[1]}, %rsp")
            if t[0] == "PrintNewline":
                instructions.append(f"  movq $.LC1, %rdi")
                instructions.append(f"  movl $0, %eax")
                instructions.append(f"  call printf")
            if t[0] == "PrintInt":
                reg1, load = reg.get_register(t[1])
                instructions.extend(load)
                instructions.append(f"  movq {reg1}, %rsi")
                instructions.append(f"  movq $.LC0, %rdi")
                instructions.append(f"  movl $0, %eax")
                instructions.append(f"  call printf")
            if t[0] == "PrintString":
                lc = self.add_constant(t[1])
                instructions.append(f"  movq ${lc}, %rdi")
                instructions.append(f"  movl $0, %eax")
                instructions.append(f"  call printf")
            if t[0] == "fopen":
                file_lc = self.add_constant(t[1])
                mode_lc = self.add_constant(t[2])
                instructions.append(f"  movq ${file_lc}, %rdi")
                instructions.append(f"  movq ${mode_lc}, %rsi")
                instructions.append(f"  movl $0, %eax")
                instructions.append(f"  call fopen")
                instructions.append(f"  movq %rax, {parse_tac_arg(t[3])}")
            if t[0] == "fprintf":
                lc = self.add_constant(t[2])
                lent = len(t[2]) - t[2].count("\\") + t[2].count("\\\\") - 2
                instructions.append(f"  movq {parse_tac_arg(t[1])}, %rax")
                instructions.append(f"  movq %rax, %rcx")
                instructions.append(f"  movl ${lent}, %edx")
                instructions.append(f"  movl $1, %esi")
                instructions.append(f"  movl ${lc}, %edi")
                instructions.append(f"  call fwrite")
            if t[0] == "fclose":
                instructions.append(f"  movq {parse_tac_arg(t[1])}, %rax")
                instructions.append(f"  movq %rax, %rdi")
                instructions.append(f"  call fclose")
                instructions.append(f"  movl $0, %eax")
            if t[0] == "=":
               # print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA", t)
                reg1, load1 = reg.get_register(t[1])
                instructions.extend(load1)
                instructions.append(f"  movq {reg1}, {parse_tac_arg(t[2])}")
            if t[0] == "+=":
                reg1, load1 = reg.get_register(t[1])
                instructions.extend(load1)
                instructions.append(f"  addq {reg1}, {parse_tac_arg(t[2])}")   

            if t[0] == "-=":
                reg1, load1 = reg.get_register(t[1])
                instructions.extend(load1)
                instructions.append(f"  subq {reg1}, {parse_tac_arg(t[2])}")   

            if t[0] == "*=":
                reg1, load1 = reg.get_register(t[1])
                instructions.extend(load1)
                instructions.append(f"  imulq {parse_tac_arg(t[2])}, %rax")
                instructions.append(f"  movq {reg1}, {parse_tac_arg(t[2])}")   

            if t[0] == "/=":

                reg1, load1 = reg.get_register(t[2], "%rax")
                instructions.extend(load1)
                
                #instructions.append(f"  movq {parse_tac_arg(arg1)}, %rax")

                instructions.append(f"  cqto")

                reg2, load2 = reg.get_register(t[1])
                instructions.extend(load2)

                instructions.append(f"  idivq {reg2}")
                res = parse_tac_arg(t[2])

                instructions.append(f"  movq %rax, {res}")  

            if t[0] == "%=":

                reg1, load1 = reg.get_register(t[2], "%rax")
                instructions.extend(load1)
                
                #instructions.append(f"  movq {parse_tac_arg(arg1)}, %rax")

                instructions.append(f"  cqto")

                reg2, load2 = reg.get_register(t[1])
                instructions.extend(load2)

                instructions.append(f"  idivq {reg2}")
                res = parse_tac_arg(t[2])

                instructions.append(f"  movq %rdx, {res}")         

            if t[0] == "allocmem":
                instructions.append(f"  movl ${t[1]}, %edi")
                instructions.append(f"  call malloc")
                instructions.append(f"  movq %rax, {parse_tac_arg(t[2])}")
            if t[0] == "cmp":
                instructions.append(f"  cmpq {parse_tac_arg(t[1])}, {parse_tac_arg(t[2])}")
            if t[0] == "CondJump" and t[1] == "ne":
                instructions.append(f"  jne {t[2]}")
            if t[0] == "CondJump" and t[1] == "e":
                instructions.append(f"  je {t[2]}")
            if t[0] == "Jump":
                instructions.append(f"  jmp {t[1]}")
            if t[0] == "Dereference":
                reg1, load1 = reg.get_register(t[1])
                instructions.extend(load1)
                instructions.append(f"  movq {parse_tac_arg(t[1])}, {reg1}")
                instructions.append(f"  movq ({reg1}), {reg1}")
                instructions.append(f"  movq {reg1}, {parse_tac_arg(t[2])}")
                instructions.append("# Dereference done")

            if len(instructions) == 0:
                print("No instructions for", t)

            self.x86instructions.extend(instructions)

    def tprint(self):
        for constant in self.constants:
            print(constant)
        for instruction in self.x86instructions:
            print(instruction)

    def fprint(self, file):
        for constant in self.constants:
            file.write(constant + "\n")
        for instruction in self.x86instructions:
            file.write(instruction + "\n")
        file.write("\n")


if __name__ == "__main__":
    asm = GAS()
    asm.tac_to_x86_mapping(None)
    asm.tprint()
