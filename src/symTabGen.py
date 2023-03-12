from symbol_table import *

global_symbol_table = SymbolTable()
current_symbol_table = global_symbol_table

def generate_symbol_table(tree):
    """Generate a symbol table from the given Parse Tree."""
    traverse_tree(tree)
    return

def traverse_tree(tree):
    """We perform a depth first traversal of the tree"""
    