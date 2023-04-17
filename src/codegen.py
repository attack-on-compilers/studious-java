#import necessary libraries


class Register:
    # these registers mapped to None and 0 initially (for no initial stored values and start time)
    regs = dict.fromkeys(['%rbx', '%r10', '%r11', '%r12', '%r13', '%r14', '%r15'], [None, 0])

    #registers for arguments
    argument_registers = dict(
        zip(
            map(str, range(6)),
            ['%rdi', '%rsi', '%rdx', '%rcx', '%r8', '%r9']
        )
    )

    def __init__(self):
        print('')

    def lru_policy(self):
        ## use the lru policy

    def write_back(self):
       
        

    def get_reg(self, var=None):
        


class ASM:
    
