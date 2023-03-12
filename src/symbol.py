from enum import Enum


class SymbolType(Enum):
    VARIABLE = "variable"
    METHOD = "method"
    CLASS = "class"
    PACKAGE = "package"


class Symbol:
    def __init__(self, name, symbol_type):
        self.name = name
        self.symbol_type = symbol_type


class VariableSymbol(Symbol):
    def __init__(self, name, type):
        super().__init__(name, SymbolType.VARIABLE)
        self.type = type
        self.scope_level = None
        self.is_initialized = False
        self.is_final = False
        self.is_static = False
        self.is_array = False


class MethodSymbol(Symbol):
    def __init__(self, name, return_type):
        super().__init__(name, SymbolType.METHOD)
        self.return_type = return_type
        self.scope_level = None
        self.parameters = []
        self.is_static = False


class ClassSymbol(Symbol):
    def __init__(self, name):
        super().__init__(name, SymbolType.CLASS)
        self.scope_level = None
        self.fields = SymbolTable()
        self.methods = SymbolTable()
        self.parent = None
        self.interfaces = []
        self.is_interface = False


class PackageSymbol(Symbol):
    def __init__(self, name):
        super().__init__(name, SymbolType.PACKAGE)
        self.scope_level = None
        self.classes = SymbolTable()
        self.subpackages = SymbolTable()


class SymbolTable:
    def __init__(self, parent=None):
        self.parent = parent
        self.symbols = {}

    def add_symbol(self, symbol):
        self.symbols[symbol.name] = symbol

    def get_symbol(self, name, symbol_type=None):
        symbol = self.symbols.get(name)
        if symbol is not None and (symbol_type is None or symbol.symbol_type == symbol_type):
            return symbol
        elif self.parent is not None:
            return self.parent.get_symbol(name, symbol_type)
        else:
            return None


class Java_SymbolTable:
    def __init__(self):
        self.packages = SymbolTable()
        self.imports = []
        self.current_scope = None
        self.current_class = None
        self.current_method = None
        self.current_package = None

    def insert(self, symbol):
        if isinstance(symbol, VariableSymbol):
            self.current_scope.add_symbol(symbol)
        elif isinstance(symbol, MethodSymbol):
            self.current_class.methods.add_symbol(symbol)
        elif isinstance(symbol, ClassSymbol):
            self.current_package.classes.add_symbol(symbol)
        elif isinstance(symbol, PackageSymbol):
            self.packages.add_symbol(symbol)

    def lookup(self, name, symbol_type=None):
        symbol = None
        if symbol_type is None or symbol_type == SymbolType.VARIABLE:
            symbol = self.current_scope.get_symbol(name, SymbolType.VARIABLE)
            if symbol is not None:
                return symbol
        if symbol_type is None or symbol_type == SymbolType.METHOD:
            symbol = self.current_class.methods.get_symbol(name, SymbolType.METHOD)
            if symbol is not None:
                return symbol
        if symbol_type is None or symbol_type == SymbolType.CLASS:
            symbol = self.current_package.classes.get_symbol(name, SymbolType.CLASS)
            if symbol is not None:
                return symbol
        if symbol_type is None or symbol_type == SymbolType.PACKAGE:
            symbol = self.packages.get_symbol(name, SymbolType.PACKAGE)
            if symbol is not None:
                return symbol
        if symbol is None and self.current_class.parent is not None:
            symbol = self.lookup(name, symbol_type, self.current_class.parent)
        return symbol    
       
