import io
import sys
from lexer import *


def get_Name(tree):
    if type(tree) == str:
        return tree
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
        case "LeftHandSide":
            return get_Name(tree[1])
        case "ArrayAccess":
            return get_Name(tree[1])
        case "FieldAccess":
            return get_Name(tree[1]) + "." + get_Name(tree[3])
        case "Primary":
            return get_Name(tree[1])
        case "PrimaryNoNewArray":
            # print("TYYYY",tree, len(tree), tree[1])
            if len(tree) == 2:
                return get_Name(tree[1])
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
        case _:
            for i in range(1, len(tree)):
                x = get_Name(tree[i])
                if x is not None:
                    return x


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


def get_NumberOfElements(tree):
    # print("YOOOOOOOOO",tree[0])
    match tree[0]:
        case "AlphaVariableDeclarator":
            if len(tree) == 2:
                return [get_NumberOfElements(tree[1])]
            else:
                return get_NumberOfElements(tree[1]) + [get_NumberOfElements(tree[3])]
        case "VariableDeclarator":
            if len(tree) == 2:
                if len(tree[1]) == 2:
                    return 1
                else:
                    return 0
            else:
                return get_NumberOfElements(tree[3])
        case "VariableInitializer":
            return get_NumberOfElements(tree[1])
        case "Expression":
            return get_NumberOfElements(tree[1])
        case "ArrayCreationExpression":
            return get_NumberOfElements(tree[3])
        case "AlphaDimExpr":
            # print("BLABLABLA",tree)
            if len(tree) == 3:
                return get_NumberOfElements(tree[1]) * get_LiteralValue(tree[2])
            else:
                return get_LiteralValue(tree[1])
        case "DimExpr":
            return get_NumberOfElements(tree[2])
        case "Literal":
            return 1
        case "ArrayInitializer":
            return get_NumberOfElements(tree[2])
        case "BetaAlphaVariableInitializer":
            if tree[1] == "":
                return 0
            else:
                return get_NumberOfElements(tree[1])
        case "AlphaVariableInitializer":
            if len(tree) == 2:
                return get_NumberOfElements(tree[1])
            else:
                return get_NumberOfElements(tree[1]) + get_NumberOfElements(tree[3])
        case _:
            if len(tree) == 2:
                return get_NumberOfElements(tree[1])
            else:
                return 1


def get_LiteralValue(tree):
    # print("NOOOOOOOOO",tree[0])
    match tree[0]:
        case "DimExpr":
            return get_LiteralValue(tree[2])
        case "Literal":
            return int(tree[1])
        case _:
            if len(tree) == 2:
                return get_LiteralValue(tree[1])
            else:
                return 1


def get_TypeSize(type):
    if type == "int":
        return 4
    elif type == "boolean":
        return 1
    elif type == "char":
        return 1
    elif type == "byte":
        return 1
    elif type == "short":
        return 2
    elif type == "long":
        return 8
    elif type == "float":
        return 4
    elif type == "double":
        return 8
    else:
        return 0


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
                raise Exception("Type mismatch in binary operation, cannot convert double to float")
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
                raise Exception("Type mismatch in binary operation, cannot convert {} to {}".format(right, left))
                # pass
        case "<<":
            if (left == "int" or left == "long" or left == "byte" or left == "short") and (
                right == "int" or right == "long" or right == "short" or right == "byte"
            ):
                pass
            else:
                raise Exception("Shift opeartor incompatible with types {} and {}".format(left, right))

        case ">>":
            if (left == "int" or left == "long" or left == "byte" or left == "short") and (
                right == "int" or right == "long" or right == "short" or right == "byte"
            ):
                pass
            else:
                raise Exception("Shift opeartor incompatible with types {} and {}".format(left, right))

        case ">>>":
            if (left == "int" or left == "long" or left == "byte" or left == "short") and (
                right == "int" or right == "long" or right == "short" or right == "byte"
            ):
                pass
            else:
                raise Exception("Shift opeartor incompatible with types {} and {}".format(left, right))

        case ">":
            if (
                left == "int"
                or left == "long"
                or left == "byte"
                or left == "short"
                or left == "float"
                or left == "double"
                or left == "char"
            ) and (
                right == "int"
                or right == "long"
                or right == "byte"
                or right == "short"
                or right == "float"
                or right == "double"
                or right == "char"
            ):
                pass
            else:
                raise Exception("Type mismatch in binary operation, cannot compare {} with {}".format(left, right))

        case "<":
            if (
                left == "int"
                or left == "long"
                or left == "byte"
                or left == "short"
                or left == "float"
                or left == "double"
                or left == "char"
            ) and (
                right == "int"
                or right == "long"
                or right == "byte"
                or right == "short"
                or right == "float"
                or right == "double"
                or right == "char"
            ):
                pass
            else:
                raise Exception("Type mismatch in binary operation, cannot compare {} with {}".format(left, right))

        case ">=":
            if (
                left == "int"
                or left == "long"
                or left == "byte"
                or left == "short"
                or left == "float"
                or left == "double"
                or left == "char"
            ) and (
                right == "int"
                or right == "long"
                or right == "byte"
                or right == "short"
                or right == "float"
                or right == "double"
                or right == "char"
            ):
                pass
            else:
                raise Exception("Type mismatch in binary operation, cannot compare {} with {}".format(left, right))

        case "<=":
            if (
                left == "int"
                or left == "long"
                or left == "byte"
                or left == "short"
                or left == "float"
                or left == "double"
                or left == "char"
            ) and (
                right == "int"
                or right == "long"
                or right == "byte"
                or right == "short"
                or right == "float"
                or right == "double"
                or right == "char"
            ):
                pass
            else:
                raise Exception("Type mismatch in binary operation, cannot compare {} with {}".format(left, right))

        case "==":
            if left == right:
                pass
            elif (
                left == "int"
                or left == "long"
                or left == "byte"
                or left == "short"
                or left == "float"
                or left == "double"
                or left == "char"
            ) and (
                right == "int"
                or right == "long"
                or right == "byte"
                or right == "short"
                or right == "float"
                or right == "double"
                or right == "char"
            ):
                pass
            else:
                raise Exception("Type mismatch in binary operation, cannot compare {} with {}".format(left, right))

        case "!=":
            if left == right:
                pass
            elif (
                left == "int"
                or left == "long"
                or left == "byte"
                or left == "short"
                or left == "float"
                or left == "double"
                or left == "char"
            ) and (
                right == "int"
                or right == "long"
                or right == "byte"
                or right == "short"
                or right == "float"
                or right == "double"
                or right == "char"
            ):
                pass
            else:
                raise Exception("Type mismatch in binary operation, cannot compare {} with {}".format(left, right))


def unop_type_check(operator, left_or_right, expression):
    match operator:
        case "++":
            if (
                left_or_right == "int"
                or left_or_right == "float"
                or left_or_right == "long"
                or left_or_right == "double"
                or left_or_right == "char"
                or left_or_right == "short"
                or left_or_right == "byte"
            ):
                pass
            else:
                raise Exception("Unary operator {} incompatible with type {}".format("++", left_or_right))

        case "--":
            if (
                left_or_right == "int"
                or left_or_right == "float"
                or left_or_right == "long"
                or left_or_right == "double"
                or left_or_right == "char"
                or left_or_right == "short"
                or left_or_right == "byte"
            ):
                pass
            else:
                raise Exception("Unary operator {} incompatible with type {}".format("--", left_or_right))

        case "~":
            if left_or_right == "String" or left_or_right == "boolean" or left_or_right == "float" or left_or_right == "double":
                raise Exception("Unary operator {} incompatible with type {}".format("~", left_or_right))
            elif left_or_right == "char":
                print("WARNING: THREAT USE OF UNARY OPERATOR FOR CHAR")
                pass
            elif left_or_right == "int" or left_or_right == "long" or left_or_right == "byte" or left_or_right == "short":
                pass
            else:
                raise Exception("Unary operator ~ incompatible with type {}".format(left_or_right))

        case "!":
            if left_or_right == "boolean":
                pass
            else:
                raise Exception("Unary operator ! incompatible with type {}".format(left_or_right))


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
        raise Exception("Type mismatch in method return type and method header type, expected float, found double")
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
        raise Exception(
            "Type mismatch in method return type and method header type, expected {}, found {}".format(
                methodheader_type, methodreturn_type
            )
        )


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
    if (t1 == "String") and (
        t2 == "int" or t2 == "short" or t2 == "byte" or t2 == "long" or t1 == "char" or t2 == "float" or t2 == "double"
    ):
        return t1
    if (t2 == "String") and (
        t1 == "int" or t1 == "short" or t1 == "byte" or t1 == "long" or t1 == "char" or t1 == "float" or t1 == "double"
    ):
        return t2
    if (t1 == "char") and (t2 == "int" or t2 == "short" or t2 == "byte" or t2 == "long" or t1 == "char"):
        return t2
    if (t2 == "char") and (t1 == "int" or t1 == "short" or t1 == "byte" or t1 == "long" or t1 == "char"):
        return t1
    else:
        raise Exception("Type mismatch in binary operation, cannot convert {} to {} or vice versa".format(t1, t2))
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
        raise Exception("Method invocation type mismatch, cannot convert {} to {} or vice versa".format(t1, t2))
