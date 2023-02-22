import sys
import ply.lex as lex

CONST_SPECIAL_CHARACTERS = u'\xf1\xe1\xe9\xed\xf3\xfa\xc1\xc9\xcd\xd3\xda\xd1'


reserved = (
    "abstract",
    "continue",
    "for",
    "new",
    "switch",
    "assert",
    "default",
    "if",
    "package",
    "synchronized",
    "boolean",
    "do",
    "goto",
    "private",
    "this",
    "break",
    "double",
    "implements",
    "protected",
    "throw",
    "byte",
    "else",
    "import",
    "public",
    "throws",
    "case",
    "enum",
    "instanceof",
    "return",
    "transient",
    "catch",
    "extends",
    "int",
    "short",
    "try",
    "char",
    "final",
    "interface",
    "static",
    "void",
    "class",
    "finally",
    "long",
    "strictfp",
    "volatile",
    "const",
    "float",
    "native",
    "super",
    "while",
    "_",
    "exports",
    "opens",
    "requires",
    "uses",
    "module",
    "permits",
    "sealed",
    "var",
    "non-sealed",
    "provides",
    "to",
    "with",
    "open",
    "record",
    "transitive",
    "yield",
)


tokens = reserved + (
    "IDENTIFIER",
# Literal                     {IntegerLiteral}|{FloatingPointLiteral}|{BooleanLiteral}|{CharacterLiteral}|{StringLiteral}|{TextBlock}|{NullLiteral}
    "INTEGER_LITERAL",
    "FLOATING_POINT_LITERAL",
    "BOOLEAN_LITERAL",
    "CHARACTER_LITERAL",
    "STRING_LITERAL",
    "TEXT_BLOCK",
    "NULL_LITERAL",
# Separator                   "("|")"|"{"|"}"|"["|"]"|";"|","|"."|"..."|"@"|"::"
    "LEFT_PAREN",
    "RIGHT_PAREN",
    "LEFT_BRACE",
    "RIGHT_BRACE",
    "LEFT_BRACKET",
    "RIGHT_BRACKET",
    "SEMICOLON",
    "COMMA",
    "DOT",
    "ELLIPSIS",
    "AT",
    "COLON_COLON",
# Operator                    "="|">"|"<"|"!"|"~"|"?"|":"|"->"|"=="|">="|"<="|"!="|"&&"|"||"|"++"|"--"|"+"|"-"|"*"|"/"|"&"|"|"|"^"|"%"|"<<"|">>"|">>>"|"+="|"-="|"*="|"/="|"&="|"|="|"^="|"%="|"<<="|">>="|">>>="
    "ASSIGN",
    "GREATER",
    "LESS",
    "EXCLAMATION",
    "TILDE",
    "QUESTION",
    "COLON",
    "ARROW",
    "EQUAL_EQUAL",
    "GREATER_EQUAL",
    "LESS_EQUAL",
    "EXCLAMATION_EQUAL",
    "AMPERSAND_AMPERSAND",
    "BAR_BAR",
    "PLUS_PLUS",
    "MINUS_MINUS",
    "PLUS",
    "MINUS",
    "STAR",
    "SLASH",
    "AMPERSAND",
    "BAR",
    "CARET",
    "PERCENT",
    "LEFT_SHIFT",
    "RIGHT_SHIFT",
    "UNSIGNED_RIGHT_SHIFT",
    "PLUS_ASSIGN",
    "MINUS_ASSIGN",
    "STAR_ASSIGN",
    "SLASH_ASSIGN",
    "AMPERSAND_ASSIGN",
    "BAR_ASSIGN",
    "CARET_ASSIGN",
    "PERCENT_ASSIGN",
    "LEFT_SHIFT_ASSIGN",
    "RIGHT_SHIFT_ASSIGN",
    "UNSIGNED_RIGHT_SHIFT_ASSIGN",
)

# Regular expression rules for simple tokens
t_LEFT_PAREN = r"\("
t_RIGHT_PAREN = r"\)"
t_LEFT_BRACE = r"\{"
t_RIGHT_BRACE = r"\}"
t_LEFT_BRACKET = r"\["
t_RIGHT_BRACKET = r"\]"
t_SEMICOLON = r";"
t_COMMA = r","
t_DOT = r"\."
t_ELLIPSIS = r"\.\.\."
t_AT = r"\@"
t_COLON_COLON = r"::"

t_ASSIGN = r"="
t_GREATER = r">"
t_LESS = r"<"
t_EXCLAMATION = r"!"
t_TILDE = r"~"
t_QUESTION = r"\?"
t_COLON = r":"
t_ARROW = r"->"
t_EQUAL_EQUAL = r"=="
t_GREATER_EQUAL = r">="
t_LESS_EQUAL = r"<="
t_EXCLAMATION_EQUAL = r"!="
t_AMPERSAND_AMPERSAND = r"&&"
t_BAR_BAR = r"\|\|"
t_PLUS_PLUS = r"\+\+"
t_MINUS_MINUS = r"--"
t_PLUS = r"\+"
t_MINUS = r"-"
t_STAR = r"\*"
t_SLASH = r"/"
t_AMPERSAND = r"&"
t_BAR = r"\|"
t_CARET = r"\^"
t_PERCENT = r"%"
t_LEFT_SHIFT = r"<<"
t_RIGHT_SHIFT = r">>"
t_UNSIGNED_RIGHT_SHIFT = r">>>"
t_PLUS_ASSIGN = r"\+="
t_MINUS_ASSIGN = r"-="
t_STAR_ASSIGN = r"\*="
t_SLASH_ASSIGN = r"/="
t_AMPERSAND_ASSIGN = r"&="
t_BAR_ASSIGN = r"\|="
t_CARET_ASSIGN = r"\^="
t_PERCENT_ASSIGN = r"%="
t_LEFT_SHIFT_ASSIGN = r"<<="
t_RIGHT_SHIFT_ASSIGN = r">>="
t_UNSIGNED_RIGHT_SHIFT_ASSIGN = r">>>="

t_ignore = " \t"

disallowed_identifiers = {r.lower(): r for r in reserved}
disallowed_identifiers["__asm_direc"] = "ASSEMBLY_DIRECTIVE"

TYPE_NAMES = []


# Implementations of the lexer rules

def t_IDENTIFIER(t):
    r"[A-Za-z_][\w_]*"
    global EXPECTED_TYPENAMES
    t.type = disallowed_identifiers.get(t.value, "IDENTIFIER")
    # if t.type == "IDENTIFIER":
        # if t.value in TYPE_NAMES:
            # t.type = "TYPE_NAME"
    return t


def t_NEWLINE(t):
    r"\n+"
    t.lexer.lineno += t.value.count("\n")


def t_comment(t):
    r"/\*(.|\n)*?\*/ | //(.)*?\n"
    t.lexer.lineno += t.value.count("\n")


def t_preprocessor(t):
    r"\#(.)*?\n"
    t.lexer.lineno += 1


# A string containing ignored characters (spaces and tabs)
t_ignore = " \t"

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()

if __name__ == "__main__":
    with open(str(sys.argv[1]), "r+") as file:
        data = file.read()
        file.close()
        print("{token type, token name, line nunmber, index relative to start of input}")
        lex.runmain(lexer, data)