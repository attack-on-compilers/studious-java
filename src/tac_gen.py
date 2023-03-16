
from symbol_table import symbol_table
from tac import TAC

def tac_gen(parse_tree):
    tac = TAC("__t", "")
    tac_gen_helper(parse_tree, tac)
    return tac

def tac_gen_helper(parse_tree, tac):
    match parse_tree[0]:
        case "":
            return
        
        case _:
            for child in parse_tree[1:]:
                tac_gen_helper(child, tac)