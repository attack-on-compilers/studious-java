from symbol_table import *
from pprint import pprint as pprint

def generate_symbol_table(tree):
    global symbol_table
    symbol_table = RootSymbolTable()
    # pprint(tree)
    traverse_tree(tree)
    return

def traverse_tree(tree):
    global symbol_table
    # We perform a depth first traversal of the tree
    match tree[0]:
        case "":
            return
        
        case "PackageDeclaration":
            packageName = traverse_tree(tree[2])
            print("Package",packageName)
            symbol_table.add_symbol(PackageSymbol(packageName))
        
        case "SingleTypeImportDeclaration":
            importName = traverse_tree(tree[2])
            print("Import",importName)
            symbol_table.add_symbol(ImportSymbol(importName))

        case "TypeImportOnDemandDeclaration":
            importName = traverse_tree(tree[2]) + ".*"
            print("Import",importName)
            symbol_table.add_symbol(ImportSymbol(importName))

        case "Name":
            # Returns a string of the name
            return traverse_tree(tree[1])
        
        case "IdentifierId":
            return tree[1]
        
        case "NameDotIdentifierId":
            # Need to see if a better representation is possible
            return traverse_tree(tree[1]) + "." + tree[3]
        
        case "TypeDeclaration":
            if tree[1] == ";":
                return
            traverse_tree(tree[1])
        
        # case "ClassDeclaration":
        #     className = tree[3]
        #     print("Class",className)
        #     current_symbol_table.add_symbol(ClassSymbol(className))
        #     previous_symbol_table = current_symbol_table
        #     if( current_symbol_table.get_symbol(className) is not None ):
        #         print("Class",className,"already exists!")
        #     current_symbol_table = SymbolTable(current_symbol_table)
        #     for i in range(3, len(tree)):
        #         traverse_tree(tree[i])
        #     current_symbol_table = previous_symbol_table
            # Not complete yet
        case _:
            for i in range(1, len(tree)):
                traverse_tree(tree[i])



        

