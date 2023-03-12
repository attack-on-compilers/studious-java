from enum import Enum




class SymbolTable:
    def __init__(self, parent=None, name=None):
        self.name = name
        self.parent = parent
        self.symbols = {}

    def add_symbol(self, symbol):
        if symbol.name in self.symbols:
            raise Exception("Symbol already defined")
        self.symbols[symbol.name] = symbol

    def add_scope (self, name, scope):
        self.symbols[name] = scope

    def get_symbol(self, name, symbol_type=None):
        symbol = self.symbols.get(name)
        if symbol is not None and (symbol_type is None or symbol.symbol_type == symbol_type):
            return symbol
        elif self.parent is not None:
            return self.parent.get_symbol(name, symbol_type)
        else:
            raise Exception("Symbol not found")


class RootSymbolTable():
    def __init__(self):
        self.root = SymbolTable(parent=None, name="root")
        self.current = self.root

    def add_symbol(self, symbol):
        self.current.add_symbol(symbol)

    def get_symbol(self, name, symbol_type=None):
        return self.current.get_symbol(name, symbol_type)
    
    def enter_scope(self, name):
        new_scope = SymbolTable(parent=self.current, name=name)
        self.current.add_scope(name, new_scope)
        self.current = new_scope

    def exit_scope(self):
        self.current = self.current.parent
