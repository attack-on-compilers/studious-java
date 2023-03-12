from symbol_table import *

global_symbol_table = SymbolTable(None)
current_symbol_table = global_symbol_table
previous_symbol_table = None

def generate_symbol_table(tree):
    # Generate a symbol table from the given Parse Tree.
    # print("Tree=",tree)
    # print("Tree[0]=",tree[0],len(tree))
    # print("Tree[1]=",tree[1])
    # print("Tree[1][0]=",tree[1][0])
    # print("Tree[1][1]=",tree[1][1])
    # print("Tree[1][2]=",tree[1][2])
    traverse_tree(tree)
    return

def traverse_tree(tree):
    global current_symbol_table
    # We perform a depth first traversal of the tree
    match tree[0]:
        case "":
            return
        case "Start":
            traverse_tree(tree[1])
        case "CompilationUnit":
            for i in range(1, len(tree)):
                traverse_tree(tree[i])
        case "BetaPackageDeclaration":
            for i in range(1, len(tree)):
                traverse_tree(tree[i])
        case "PackageDeclaration":
            current_symbol_table.add_symbol(PackageSymbol(traverse_tree(tree[2])))
        case "BetaAlphaImportDeclaration":
            for i in range(1, len(tree)):
                traverse_tree(tree[i])
        case "AlphaImportDeclaration":
            for i in range(1, len(tree)):
                traverse_tree(tree[i])
        case "ImportDeclaration":
            for i in range(1, len(tree)):
                traverse_tree(tree[i])
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
        case "Name":
            # Returns a string of the name
            return traverse_tree(tree[1])
        case "IdentifierId":
            return tree[1]
        case "NameDotIdentifierId":
            # Need to see if a better representation is possible
            return traverse_tree(tree[1]) + "." + tree[3]
        case "BetaAlphaTypeDeclaration":
            for i in range(1, len(tree)):
                traverse_tree(tree[i])
        case "AlphaTypeDeclaration":
            for i in range(1, len(tree)):
                traverse_tree(tree[i])
        case "TypeDeclaration":
            if tree[1] == ";":
                return
            traverse_tree(tree[1])
        case "ClassDeclaration":
            className = tree[3]
            print("Class",className)
            current_symbol_table.add_symbol(ClassSymbol(className))
            previous_symbol_table = current_symbol_table
            if( current_symbol_table.get_symbol(className) is not None ):
                print("Class",className,"already exists!")
            current_symbol_table = SymbolTable(current_symbol_table)
            for i in range(3, len(tree)):
                traverse_tree(tree[i])
            current_symbol_table = previous_symbol_table
            # Not complete yet
        


        

