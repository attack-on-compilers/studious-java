import io
import sys
from lexer import *


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
                    return get_Name(tree[1]) + "[]"
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
        case "":
            return []
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
        case _:
            return []


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


def binop_type_check(left, operator, right, expression):
    match operator:
        case "=":
            if left == right:
                pass
            elif (left == "int" or left == "long" or left == "short" or left == "byte" or left == "char") and (
                right == "int" or right == "long" or right == "short" or right == "byte" or right == "char"
            ):
                pass
            elif left == "float" and right == "double":
                raise Exception("Type mismatch in binary operation")
            elif left == "double" and right == "float":
                pass
            elif left == "float" and (
                right == "int" or right == "long" or right == "short" or right == "byte" or right == "char"
            ):
                pass
            elif left == "double" and (
                right == "int" or right == "long" or right == "short" or right == "byte" or right == "char"
            ):
                pass
            else:
                raise Exception("Type mismatch in binary operation")
                #pass


def unop_type_check(operator, left_or_right, expression):
    pass


def method_type_check(methodreturn_type, methodheader_type):
    if methodreturn_type == methodheader_type:
        pass
    elif methodreturn_type is None and methodheader_type == "void":
        pass
    elif (
        methodreturn_type == "int"
        or methodreturn_type == "long"
        or methodreturn_type == "char"
        or methodreturn_type == "byte"
        or methodreturn_type == "short"
    ) and (
        methodheader_type == "long"
        or methodheader_type == "int"
        or methodheader_type == "short"
        or methodheader_type == "byte"
        or methodheader_type == "char"
    ):
        pass
    elif methodreturn_type == "float" and methodheader_type == "double":
        pass
    elif methodreturn_type == "double" and methodheader_type == "float":
        raise Exception("Type mismatch in method return type and method header type")
    elif methodheader_type == "float" and (
        methodreturn_type == "int"
        or methodreturn_type == "long"
        or methodreturn_type == "short"
        or methodreturn_type == "byte"
        or methodreturn_type == "char"
    ):
        pass
    elif methodheader_type == "double" and (
        methodreturn_type == "int"
        or methodreturn_type == "long"
        or methodreturn_type == "short"
        or methodreturn_type == "byte"
        or methodreturn_type == "char"
    ):
        pass
    else:
        raise Exception("Type mismatch in method return type and method header type")


def string_to_type(expression):
    try:
        output_buffer = io.StringIO()
        sys.stdout = output_buffer

        # Run the lexer and store the output
        lex.runmain(lexer, expression)
        output = output_buffer.getvalue()
        # Reset standard output to its original value
        sys.stdout = sys.__stdout__
        start = output.index("(") + 1  # get the index of the opening parenthesis and add 1 to skip it
        end = output.index(",")  # get the index of the first comma
        result = output[start:end]  # extract the substring between the two indices
        if (
            result == "INTEGER_LITERAL_OCTAL"
            or result == "INTEGER_LITERAL_DEC"
            or result == "INTEGER_LITERAL_HEXADEC"
            or result == "INTEGER_LITERAL_BINAR"
        ):
            return "int"
        if result == "FLOATING_LITERAL_REDUCED_POINT" and not (expression[-1] == "f" or expression[-1] == "F"):
            return "double"
        if result == "FLOATING_LITERAL_REDUCED_POINT" and (expression[-1] == "f" or expression[-1] == "F"):
            return "float"
        if result == "BOOLEAN_LITERAL":
            return "boolean"
        if result == "CHARACTER_LITERAL":
            return "char"
        if result == "STRING_LITERAL":
            return "String"
        if result == "TEXT_BLOCK":
            return "str"  ##verify once
        if result == "NULL_LITERAL":
            return "null"
    except:
        return type(expression).__name__


def big(t1, t2):
    if t1 == t2:
        return t1
    if t1 == "double" and (t2 == "float" or t2 == "int" or t2 == "short" or t2 == "long" or t2 == "byte" or t2 == "char"):
        return t1
    if t2 == "double" and (t1 == "float" or t1 == "int" or t1 == "short" or t1 == "long" or t1 == "byte" or t1 == "char"):
        return t2
    if t1 == "float" and (t2 == "int" or t2 == "short" or t2 == "long" or t2 == "byte" or t2 == "char"):
        return t1
    if t2 == "float" and (t1 == "int" or t1 == "short" or t1 == "long" or t1 == "byte" or t1 == "char"):
        return t2
    if t1 == "long" and (t2 == "int" or t2 == "short" or t2 == "byte" or t2 == "char"):
        return t1
    if t2 == "long" and (t1 == "int" or t1 == "short" or t1 == "byte" or t1 == "char"):
        return t2
    if t1 == "int" and (t2 == "short" or t2 == "byte" or t2 == "char"):
        return t1
    if t2 == "int" and (t1 == "short" or t1 == "byte" or t1 == "char"):
        return t2
    if t1 == "short" and t2 == "byte":
        return t1
    if t2 == "short" and t1 == "byte":
        return t2
    if (t1 == "char" or t1 == "String") and (t2 == "int" or t2 == "short" or t2 == "byte" or t2 == "long" or t1 == "char"):
        return t1
    if (t2 == "char" or t2 == "String") and (t1 == "int" or t1 == "short" or t1 == "byte" or t1 == "long" or t1 == "char"):
        return t2
    else:
        raise Exception("Type mismatch in binary operation")
    # pass


def big_method(t1, t2):
    # t1: method invocation params
    # t2: method called type
    if t1 == t2:
        return
    # if t1 == "double" and (t2 == "float" or t2 == "int" or t2 == "short" or t2 == "long" or t2 == "byte"):
    #     pass
    if t2 == "double" and (t1 == "float" or t1 == "int" or t1 == "short" or t1 == "long" or t1 == "byte" or t1 == "char"):
        return
    # if t1 == "float" and (t2 == "int" or t2 == "short" or t2 == "long" or t2 == "byte"):
    #     pass
    if t2 == "float" and (t1 == "int" or t1 == "short" or t1 == "long" or t1 == "byte" or t1 == "char"):
        return
    # if t1 == "long" and (t2 == "int" or t2 == "short" or t2 == "byte"):
    #     return t1
    if t2 == "long" and (t1 == "int" or t1 == "short" or t1 == "byte" or t1 == "char"):
        return
    # if t1 == "int" and (t2 == "short" or t2 == "byte"):
    #     return t1
    if t2 == "int" and (t1 == "short" or t1 == "byte" or t1 == "char"):
        return
    # if t1 == "short" and t2 == "byte":
    #     return t1
    if t2 == "short" and t1 == "byte":
        return
    # if (t1 == "char" or t1 == "String") and (t2 == "int" or t2 == "short" or t2 == "byte" or t2 == "long" or t1 == "char"):
    #     return t1
    # if (t2 == "char" or t2 == "String") and (t1 == "int" or t1 == "short" or t1 == "byte" or t1 == "long" or t1 == "char"):
    #     pass
    else:
        raise Exception("Method invocation type mismatch")