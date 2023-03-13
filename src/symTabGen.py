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
            methodModifiers = get_Modifiers(tree[1][1])
            if tree[1][2] == "void":
                methodReturnType = "void"
            else:
                methodReturnType = get_Type(tree[1][2])
            methodName = get_Name(tree[1][3])
            methodParams = []
            if len(tree[1][3]) == 5:
                methodParams = get_Parameters(tree[1][3][3])
            methodThrows = get_Exceptions(tree[1][4])
            methodSignature = methodName + "(" 
            if len(methodParams) != 0:
                for i in methodParams:
                    methodSignature += i[0] + ","
            methodSignature += ")"
            symbol_table.add_symbol(MethodSymbol(methodSignature, methodReturnType, symbol_table.current, methodModifiers, methodThrows))
            symbol_table.enter_scope(methodSignature)
            for i in methodParams:
                fieldModifiers = []
                fieldType = i[0]
                dims = 0
                if fieldType[-1] == "]":
                    dims = fieldType.count("[")
                    fieldType = fieldType[:fieldType.find("[")]
                symbol_table.add_symbol(VariableSymbol(i[1], fieldType, [], dims))
                pass
            traverse_tree(tree[2])
            symbol_table.exit_scope()

        case "StaticInitializer":
            static_init_name = "<clinit>"
            symbol_table.add_symbol(MethodSymbol(static_init_name, "void", symbol_table.current, [], []))
            symbol_table.enter_scope(static_init_name)
            traverse_tree(tree[2])
            symbol_table.exit_scope()

        case "ConstructorDeclaration":
            constructorModifiers = get_Modifiers(tree[1])
            constructorName = get_Name(tree[2][1])
            constructorParams = get_Parameters(tree[2][3])
            constructorThrows = get_Exceptions(tree[3])
            constructorSignature = constructorName + "("
            if len(constructorParams) != 0:
                for i in constructorParams:
                    constructorSignature += i[0] + ","
            constructorSignature += ")"
            symbol_table.add_symbol(MethodSymbol(constructorSignature, None, symbol_table.current, constructorModifiers, constructorThrows))
            symbol_table.enter_scope(constructorSignature)
            for i in constructorParams:
                fieldModifiers = []
                fieldType = i[0]
                dims = 0
                if fieldType[-1] == "]":
                    dims = fieldType.count("[")
                    fieldType = fieldType[:fieldType.find("[")]
                symbol_table.add_symbol(VariableSymbol(i[1], fieldType, [], dims))
            traverse_tree(tree[4])
            symbol_table.exit_scope()


        case "InterfaceDeclaration":
            interfaceName = tree[3]
            interfaceModifiers = get_Modifiers(tree[1])
            interfaceInterfaces = get_Interfaces(tree[4])
            symbol_table.add_symbol(InterfaceSymbol(interfaceName, symbol_table.current, interfaceModifiers, interfaceInterfaces))
            symbol_table.enter_scope(interfaceName)
            traverse_tree(tree[5])
            symbol_table.exit_scope()
            
        case "Block":    
            pass

        case "VariableDeclarator":
            pass
            # variableName = get_Name(tree[1])
            # variableType = get_Type(tree[2])
            # variableModifiers = get_Modifiers(tree[0])
            # print("Variable", variableName, variableType, variableModifiers)
            # symbol_table.add_symbol(VariableSymbol(variableName, variableType, variableModifiers))

                    
        
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
        case "MethodDeclarator":
            if len(tree) == 5:
                return tree[1]
            else:
                return get_Name(tree[1])
        
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
                return get_Modifiers(tree[1]) + get_Modifiers(tree[2])
        case "Modifier":
            return [tree[1]]

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
                return get_Interfaces(tree[1]) + get_Interfaces(tree[3])
        case "InterfaceType":
            return [get_Name(tree[1])]
        case "BetaExtendsAlphaInterface":
            if tree[1] == "":
                return []
            else:
                return get_Interfaces(tree[1])
        case "ExtendsAlphaInterface":
            if len(tree) == 2:
                return get_Interfaces(tree[1])
            else:
                return get_Interfaces(tree[1]) + get_Interfaces(tree[3])


def get_Exceptions(tree):
    match tree[0]:
        case "BetaAlphaThrow":
            if tree[1] == "":
                return []
            else:
                return get_Exceptions(tree[1])
        case "AlphaThrow":
            return get_Exceptions(tree[2])
        case "ClassTypeList":
            if len(tree) == 2:
                return [get_Name(tree[1])]
            else:
                return get_Exceptions(tree[1]) + [get_Name(tree[3])]
        
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

def get_Parameters(tree):
    match tree[0]:
        case "BetaFormalParameterList":
            if tree[1] == "":
                return []
            else:
                return get_Parameters(tree[1])
        case "FormalParameterList":
            if len(tree) == 2:
                return get_Parameters(tree[1])
            else:
                return get_Parameters(tree[1]) + get_Parameters(tree[3])
        case "FormalParameter":
            parameterType = get_Type(tree[1])
            parameterName = get_Name(tree[2])
            return [[parameterType, parameterName]]
        case _:
            return []