# https://matthewmacfarquhar.medium.com/build-your-own-programming-language-part-4-the-symbol-table-69f47ea394ad 
# Somewhat based symbol table off this but tried to simplify it
# Basically just a dictionary of dictionaries with some ease of use things

class symbol_table:
    def __init__(self):
        self.scopes = {}  

    # Add a new symbol to the table
    def add_symbol(self,name, type, scope, kind):
        if scope not in self.scopes:
            self.scopes[scope] = {}
        if name in self.scopes[scope]:
            raise Exception(f"Symbol {name} already declared in scope {scope}")
        self.scopes[scope][name] = symbol_table_entry(name, type, scope, kind)

    # Lookup a symbol in the table
    def lookup(self, name, scope):
        if scope in self.scopes and name in self.scopes[scope]:
            return self.scopes[scope][name]
        if 'global' in self.scopes and name in self.scopes['global']:
            return self.scopes['global'][name]
        return None
    
    # Get all the parameters of a function
    def get_function_params(self, function_name):
        params = []
        if function_name in self.scopes:
            for symbol_entry in self.scopes[function_name].values():
                if symbol_entry.kind == "parameter":
                    params.append(symbol_entry)
        return params if params else None
    
    # Print the entire symbol table
    def print_table(self):
        if not self.scopes:
            print("Symbol table is empty")
            return
            
        for scope_name, scope_symbols in self.scopes.items():
            print(f"Scope: {scope_name}")
            for symbol_entry in scope_symbols.values():
                print(f"  {symbol_entry}")
            print()

# Symbol table entry class
# Name - name of the symbol
# Type - data type of the symbol 
# Scope - scope in which the symbol is defined
# Kind - kind of symbol variable vs function
class symbol_table_entry:
    def __init__(self, name, type, scope, kind):
        self.name = name
        self.type = type
        self.scope = scope
        self.kind = kind

    def __str__(self):
        return f"Name: {self.name}, Type: {self.type}, Scope: {self.scope}, Kind: {self.kind}"