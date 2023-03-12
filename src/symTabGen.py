from symbol_table import *

def generate_symbol_table(tree):
    global global_symbol_table
    global_symbol_table = RootSymbolTable()
    traverse_tree(tree)
    return

def traverse_tree(tree):
    global global_symbol_table
    # We perform a depth first traversal of the tree
    match tree[0]:
        case "":
            return

        case "PackageDeclaration":
            package_name = traverse_tree(tree[2])
            print("Package",package_name)
            # current_symbol_table.add_symbol(PackageSymbol(traverse_tree(tree[2])))

        case "SingleTypeImportDeclaration":
            print("Single",traverse_tree(tree[2]))
            # current_symbol_table.add_symbol(ImportSymbol(traverse_tree(tree[2])))
            # Need to see how to manage the import symbol
            pass
        case "TypeImportOnDemandDeclaration":
            print("Demand",traverse_tree(tree[2]),".*")
            # current_symbol_table.add_symbol(ImportSymbol(traverse_tree(tree[2])))
            # Need to see how to manage the import symbol
            pass

        case "IdentifierId":
            return tree[1]

        case "NameDotIdentifierId":
            # Need to see if a better representation is possible
            return traverse_tree(tree[1]) + "." + tree[3]

        case "TypeDeclaration":
            if tree[1] == ";":
                return
            traverse_tree(tree[1])

        case _:
            for i in range(1, len(tree)):
                return traverse_tree(tree[i])


        

