from enum import Enum


DELIMERTER = ","


class VariableScope(Enum):
    PRIVATE = 1
    PUBLIC = 2
    PARAMETER = 3


class VariableType(Enum):
    BYTE = "BYTE"
    SHORT = "SHORT"
    INT = "INT"
    LONG = "LONG"
    CHAR = "CHAR"
    FLOAT = "FLOAT"
    DOUBLE = "DOUBLE"
    BOOLEAN = "BOOLEAN"


VariableDataTypes = [
    VariableType.BYTE.value,
    VariableType.SHORT.value,
    VariableType.INT.value,
    VariableType.LONG.value,
    VariableType.CHAR.value,
    VariableType.FLOAT.value,
    VariableType.DOUBLE.value,
    VariableType.BOOLEAN.value,
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


class Symbol:
    def __init__(self, name, symbol_type):
        self.name = name
        self.symbol_type = symbol_type


class ClassSymbol(Symbol):
    def __init__(self, name, parent_symbol_table, scope=VariableScope.PRIVATE, parent_class=None):
        super().__init__(name, "class")
        self.symbol_table = SymbolTable(parent=parent_symbol_table, name=name + " symbol table")
        self.scope = scope
        self.parent_class = parent_class

    def __str__(self):
        return DELIMERTER.join([self.name, self.symbol_type, self.symbol_table.name, self.scope, self.parent_class])


class MethodSymbol(Symbol):
    def __init__(self, name, return_type, parent, scope=VariableScope.PRIVATE):
        super().__init__(name, "method")
        self.symbol_table = SymbolTable(parent=parent, name=name + " symbol table")
        self.return_type = return_type
        self.scope = scope

    def __str__(self):
        return DELIMERTER.join([self.name, self.symbol_type, self.symbol_table.name, self.return_type, self.scope])


class BlockSymbol(Symbol):
    def __init__(self, name, parent):
        super().__init__(name, "block")
        self.symbol_table = SymbolTable(parent=parent, name=name + " symbol table")

    def __str__(self):
        return DELIMERTER.join([self.name, self.symbol_type, self.symbol_table.name])


class InterfaceSymbol(Symbol):
    def __init__(self, name, parent):
        super().__init__(name, "interface")
        self.symbol_table = SymbolTable(parent=parent, name=name + " symbol table")

    def __str__(self):
        return DELIMERTER.join([self.name, self.symbol_type, self.symbol_table.name])


class VariableSymbol(Symbol):
    def __init__(self, name, data_type, scope=VariableScope.PRIVATE, dims=1):
        super().__init__(name, "variable")
        self.data_type = data_type
        self.scope = scope
        self.dims = dims

    def __str__(self):
        return DELIMERTER.join([self.name, self.symbol_type, self.data_type, self.scope, str(self.dims)])


# Added temporarily
class PackageSymbol(Symbol):
    def __init__(self, name):
        super().__init__(name, "package")

    def __str__(self):
        return DELIMERTER.join([self.name, self.symbol_type])


# Added temporarily
class ImportSymbol(Symbol):
    def __init__(
        self,
        name,
    ):
        super().__init__(name, "import")

    def __str__(self):
        return DELIMERTER.join([self.name, self.symbol_type])


class SymbolTable:
    def __init__(self, parent=None, name=None):
        self.name = name
        self.parent = parent
        self.symbols = {}

    def add_symbol(self, symbol):
        if symbol.name in self.symbols:
            raise Exception("Symbol already defined")
        self.symbols[symbol.name] = symbol

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
        self.current = self.current.get_symbol(name)

    def exit_scope(self):
        self.current = self.current.parent
