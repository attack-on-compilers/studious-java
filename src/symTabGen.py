from symbol_table import *
from pprint import pprint as pprint

def generate_symbol_table(tree):
    global symbol_table
    symbol_table = RootSymbolTable()
    # pprint(tree)
    traverse_tree(tree)
    symbol_table.tprint()
    return

def traverse_tree(tree):
    global symbol_table
    # We perform a depth first traversal of the tree
    match tree[0]:
        case "":
            return
        
        case "PackageDeclaration":
            packageName = get_Name(tree[2])
            symbol_table.add_symbol(PackageSymbol(packageName))
        
        case "SingleTypeImportDeclaration":
            importName = get_Name(tree[2])
            symbol_table.add_symbol(ImportSymbol(importName))

        case "TypeImportOnDemandDeclaration":
            importName = get_Name(tree[2]) + ".*"
            symbol_table.add_symbol(ImportSymbol(importName))
        
        case "ClassDeclaration":
            className = tree[3]
            classModifiers = get_Modifiers(tree[1])
            classParent = get_Parent(tree[4])
            classInterfaces = get_Interfaces(tree[5])
            symbol_table.add_symbol(ClassSymbol(className, symbol_table, classModifiers, classParent, classInterfaces))
            symbol_table.enter_scope(className)
            traverse_tree(tree[6])
            symbol_table.exit_scope()

        case "ClassMemberDeclaration":
            pass

        case "StaticInitializer":
            pass

        case "ConstructorDeclaration":
            constructorName = get_Name(tree[1][2])
            constructorModifiers = get_Modifiers(tree[1][1])
            constructorParams = get_Parameters(tree[1][3])
            constructorExceptions = get_Exceptions(tree[2])
            symbol_table.add_symbol(ConstructorSymbol(constructorName, constructorModifiers, constructorParams, constructorExceptions))
            symbol_table.enter_scope(constructorName)
            traverse_tree(tree[1][4])
            symbol_table.exit_scope()


        case "InterfaceDeclaration":
            pass
        
        case "VariableDeclarator":
            variableName = get_Name(tree[1])
            variableType = get_Type(tree[2])
            variableModifiers = get_Modifiers(tree[0])
            print("Variable", variableName, variableType, variableModifiers)
            symbol_table.add_symbol(VariableSymbol(variableName, variableType, variableModifiers))

                    
        
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
        case "InterfaceType":
            return get_Name(tree[1])
        case "ClassOrInterfaceType":
            return get_Name(tree[1])
        case "ClassType":
            return get_Name(tree[1])
        
def get_Type(tree):
    match tree[0]:
        case "Type":
            return get_Type(tree[1])
        case "PrimitiveType":
            return tree[1]
        case "ReferenceType":
            match tree[1][0]:
                case "ClassOrInterfaceType":
                    return get_Name(tree[1])
                case "ArrayType":
                    if len(tree) == 3: # array without a variable name
                        return get_Type(tree[1][1]) + "[]"
                    elif len(tree) == 4: # array with a variable name
                        return get_Name(tree[1][1]) + "[]"

        
def get_Modifiers(tree):
    match tree[0]:
        case "BetaAlphaModifier":
            return get_Modifiers(tree[1])
        case "AlphaModifier":
            if len(tree) == 2:
                return get_Modifiers(tree[1])
            else:
                return get_Modifiers(tree[1]) + ", " + get_Modifiers(tree[2])
        case "Modifier":
            return tree[1]

def get_Parent(tree):
    match tree[0]:
        case "BetaSuper":
            return get_Parent(tree[1])
        case "Super":
            return get_Name(tree[2])
        
def get_Interfaces(tree):
    match tree[0]:
        case "BetaAlphaInterface":
            return get_Interfaces(tree[1])
        case "AlphaInterface":
            return get_Interfaces(tree[2])
        case "InterfaceTypeList":
            if len(tree) == 2:
                return get_Interfaces(tree[1])
            else:
                return get_Interfaces(tree[1]) + ", " + get_Interfaces(tree[3])
        case "InterfaceType":
            return get_Name(tree[1])
        
# def get_Parameters(tree):
#     match tree[0]:
#         case "FormalParameterList":
#             return [get_Parameter(param) for param in tree[1]]
#         case "":
#             return []

# def get_Parameter(tree):
#     parameterName = get_Name(tree[1])
#     parameterType = get_Type(tree[2])
#     return VariableSymbol(parameterName, parameterType)

def get_Exceptions(tree):
    match tree[0]:
        case "":
            return []
        case "Throw":
            return [get_Name(exception) for exception in tree[1][1:]]
