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
    def __init__(self, name, symbol_type):
        super().__init__(name, symbol_type)

class VariableSymbol(Symbol):
    def __init__(self, name, symbol_type):
        super().__init__(name, symbol_type)


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
