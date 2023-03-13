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
            symbol_table.add_symbol(ClassSymbol(className, symbol_table.current, classModifiers, classParent, classInterfaces))
            symbol_table.enter_scope(className)
            traverse_tree(tree[6])
            symbol_table.exit_scope()

        case "FieldDeclaration":
            fieldModifiers = get_Modifiers(tree[1])
            fieldType = get_Type(tree[2])
            dims = 0
            if fieldType[-1] == "]":
                dims = fieldType.count("[")
                fieldType = fieldType[:fieldType.find("[")]
            fieldVariables = get_Variables(tree[3])
            for i in fieldVariables:
                symbol_table.add_symbol(VariableSymbol(i, fieldType, fieldModifiers, dims))

        case "MethodDeclaration":
            print("Tree[1]", tree[1][3][1])
            methodModifiers = get_Modifiers(tree[1][1])
            if tree[1][2] == "void":
                methodType = "void"
            else:
                methodType = get_Type(tree[1][2])
            methodName = tree[1][3][1]
            # Need to fix method name
            print(methodName, methodType, methodModifiers)
            methodParams = []
            # if len(tree[1][3]) == 5:
            #     methodParams = get_Parameters(tree[1][3][3])
            methodThrows = [] 
            # Need to Implement methodThrows
            methodSignature = methodName + "(" + ",".join(methodParams) + ")"
            symbol_table.add_symbol(MethodSymbol(methodSignature, methodType, symbol_table.current, methodModifiers, methodThrows))
            symbol_table.enter_scope(methodSignature)
            for i in methodParams:
                # symbol_table.add_symbol(VariableSymbol(i[1], i[0], VariableScope.PARAMETER))
                # Need to implement method parameters
                pass
            traverse_tree(tree[2])
            symbol_table.exit_scope()



        case "StaticInitializer":
            pass

        # case "ConstructorDeclaration":
        #     constructorName = get_Name(tree[1][2])
        #     constructorModifiers = get_Modifiers(tree[1][1])
        #     constructorParams = get_Parameters(tree[1][3])
        #     constructorExceptions = get_Exceptions(tree[2])
        #     symbol_table.add_symbol(ConstructorSymbol(constructorName, constructorModifiers, constructorParams, constructorExceptions))
        #     symbol_table.enter_scope(constructorName)
        #     traverse_tree(tree[1][4])
        #     symbol_table.exit_scope()


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
        case "VariableDeclaratorId":
            match len(tree):
                case 2:
                    return tree[1]
                case 4:
                    return tree[1] + "[]"
        
def get_Type(tree):
    match tree[0]:
        case "Type":
            return get_Type(tree[1])
        case "PrimitiveType":
            match tree[1]:
                case "boolean":
                    return "boolean"
            return get_Type(tree[1])
        case "NumericType":
            return get_Type(tree[1])
        case "IntegralType":
            return tree[1]
        case "FloatingPointType":
            return tree[1]
        case "ReferenceType":
            return get_Type(tree[1])
        case "ClassOrInterfaceType":
            return get_Name(tree[1])
        case "ArrayType":
            match tree[1][0]:
                case "Name":
                    return get_Name(tree[1]) + "[]"
            return get_Type(tree[1]) + "[]"

        
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
        
def get_Variables(tree):
    match tree[0]:
        case "AlphaVariableDeclarator":
            if len(tree) == 2:
                return get_Variables(tree[1])
            else:
                return get_Variables(tree[1]) + get_Variables(tree[3])
        case "VariableDeclarator":
            if len(tree) == 2:
                return [get_Name(tree[1])]
            else:
                # traverse_tree(tree)
                # Need to add traverse logic for VariableDeclaratorId : VariableDeclaratorId ASSIGN Expression
                return [get_Name(tree[1])]
