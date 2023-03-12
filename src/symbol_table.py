from enum import Enum


class Symbol:
    def __init__(self, name, symbol_type):
        self.name = name
        self.symbol_type = symbol_type


class ClassSymbol(Symbol):
    def __init__(self, name, parent):
        super().__init__(name, "class")
        self.symbol_table = SymbolTable(parent=parent, name=name + " symbol table")


class MethodSymbol(Symbol):
    def __init__(self, name, return_type, parent, scope=VariableScope.PRIVATE):
        super().__init__(name, "method")
        self.symbol_table = SymbolTable(parent=parent, name=name + " symbol table")
        self.return_type = return_type
        self.scope = VariableScope.PRIVATE


class BlockSymbol(Symbol):
    def __init__(self, name, parent):
        super().__init__(name, "block")
        self.symbol_table = SymbolTable(parent=parent, name=name + " symbol table")


class InterfaceSymbol(Symbol):
    def __init__(self, name, parent):
        super().__init__(name, "interface")
        self.symbol_table = SymbolTable(parent=parent, name=name + " symbol table")


class VariableScope(Enum):
    PRIVATE = 1
    PUBLIC = 2
    PARAMETER = 3


class VariableType(Enum):
    BYTE = "byte"
    SHORT = "short"
    INT = "int"
    LONG = "long"
    CHAR = "char"
    FLOAT = "float"
    DOUBLE = "double"
    BOOLEAN = "boolean"


VariableDataTypes = [
    VariableType.BYTE,
    VariableType.SHORT,
    VariableType.INT,
    VariableType.LONG,
    VariableType.CHAR,
    VariableType.FLOAT,
    VariableType.DOUBLE,
    VariableType.BOOLEAN,
]


def get_variable_symbols(name, data_type, parent):
    if data_type in VariableDataTypes:
        raise Exception("Invalid data type")
    data_symbol_table = parent.get_symbol(name, data_type).symbol_table
    variables = []
    for symbol in data_symbol_table.symbols.values():
        if symbol.scope == VariableScope.PUBLIC:
            variables.append(VariableSymbol(symbol.name, symbol.data_type, scope=VariableScope.PUBLIC, dims=symbol.dims))
    return variables


class VariableSymbol(Symbol):
    def __init__(self, name, data_type, scope=VariableScope.PRIVATE, dims=1):
        super().__init__(name, "variable")
        self.data_type = data_type
        self.scope = scope
        self.dims = dims


class SymbolTable:
    def __init__(self, parent=None, name=None):
        self.name = name
        self.parent = parent
        self.symbols = {}

    def add_symbol(self, symbol):
        if symbol.name in self.symbols:
            raise Exception("Symbol already defined")
        self.symbols[symbol.name] = symbol

    def get_scope(self, name):
        if name not in self.symbols:
            self.symbols[name] = SymbolTable(parent=self, name=name)
        return self.symbols[name]

    def get_symbol(self, name, symbol_type=None):
        symbol = self.symbols.get(name)
        if symbol is not None and (symbol_type is None or symbol.symbol_type == symbol_type):
            return symbol
        elif self.parent is not None:
            return self.parent.get_symbol(name, symbol_type)
        else:
            raise Exception("Symbol not found")


class RootSymbolTable:
    def __init__(self):
        self.root = SymbolTable(parent=None, name="root")
        self.current = self.root

    def add_symbol(self, symbol):
        self.current.add_symbol(symbol)

    def get_symbol(self, name, symbol_type=None):
        return self.current.get_symbol(name, symbol_type)

    def enter_scope(self, name):
        self.current = self.current.get_scope(name)

    def exit_scope(self):
        self.current = self.current.parent
