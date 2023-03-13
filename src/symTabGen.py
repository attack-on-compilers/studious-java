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
            packageName = get_Name(tree[2])
            print("Package",packageName)
            symbol_table.add_symbol(PackageSymbol(packageName))
        
        case "SingleTypeImportDeclaration":
            importName = get_Name(tree[2])
            print("Import",importName)
            symbol_table.add_symbol(ImportSymbol(importName))

        case "TypeImportOnDemandDeclaration":
            importName = get_Name(tree[2]) + ".*"
            print("Import",importName)
            symbol_table.add_symbol(ImportSymbol(importName))
        
        case "TypeDeclaration":
            # if tree[1] == ";":
            #     return
            traverse_tree(tree[1])
        
        case "ClassDeclaration":
            className = get_Name(tree[3])
            classModifiers = get_Modifiers(tree[1])
            # SuperClass Todo
            # classInterface Todo
            # Add class to symob Table
            pass

        case "ClassMemberDeclaration":
            pass

        case "StaticInitializer":
            pass

        case "ConstructorDeclaration":
            pass

        case "InterfaceDeclaration":
            pass
        
        case "VariableDeclarator":
            pass
        
        case _:
            for i in range(1, len(tree)):
                traverse_tree(tree[i])


def get_Name(tree):
    match tree[0]:
        case "Name":
            return get_Name(tree[1])
        case "IdentifierId":
            return tree[1]
        case "NameDotIdentifierId":
            return get_Name(tree[1]) + "." + tree[3]
        
def get_Modifiers(tree):
    pass
