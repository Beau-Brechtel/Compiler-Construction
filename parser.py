import AST
import SymbolTable
from lexer import TokenType, Token
from Errors import ParsingError

class Parser:
    def __init__(self):
        self.tokens = []
        self.current_token_index = 0
        self.lookahead = None
        self.symbol_table = SymbolTable.symbol_table()  

    # Move to the next token 
    def consume(self):
        if self.current_token_index < len(self.tokens):
            self.lookahead = self.tokens[self.current_token_index]
            self.current_token_index += 1
        else:
            self.lookahead = None
        
    # Make sure the current token matches the expected type    
    def match(self, expected_type):
        if self.lookahead is None:
            raise ParsingError(f"Expected {expected_type.value} but reached end of input", 0, 0)
        elif self.lookahead.type != expected_type:
            raise ParsingError(f"Expected {expected_type.value} found {self.lookahead.value}", self.lookahead.line, self.lookahead.column)
        self.consume()

    # Main parse function that starts the parsing process
    def parse(self, tokens):
        self.tokens = tokens
        
        # Initialize lookahead token
        self.consume()

        # Create root of AST 
        program_token = Token(TokenType.PARSING_TOKEN, "Program", None, None)
        program_root = AST.AST(program_token)

        # Start looping through tokens and building AST
        while self.lookahead is not None:
            decl = self.parse_decl()
            if decl is not None:
                program_root.add_child(decl)

        # Return AST tree and symbol table
        return program_root, self.symbol_table

    def parse_decl(self, scope = "global"):
        type = self.lookahead.value
        if self.lookahead.type not in [TokenType.INT, TokenType.FLOAT, TokenType.CHAR, TokenType.BOOL, TokenType.VOID]:
            raise ParsingError(f"Unexpected type {type}", self.lookahead.line, self.lookahead.column)
        self.match(self.lookahead.type)

        # Get function/variable name
        token = self.lookahead 
        if self.lookahead.type not in [TokenType.IDENTIFIER, TokenType.MAIN]:
            raise ParsingError(f"Expected name but found {self.lookahead.value}", self.lookahead.line, self.lookahead.column)
        self.match(self.lookahead.type)

        if self.lookahead.type == TokenType.LEFT_PAREN:
            self.symbol_table.add_symbol(token.value, type, scope, "function")
            return self.parse_func_decl(token)
        else:
            self.symbol_table.add_symbol(token.value, type, scope, "variable")
            return self.parse_var_decl("global", token, type)

    # Parses a single function declaration
    def parse_func_decl(self, func_token):
        
        # Use the actual function name token
        func_decl = AST.AST(func_token)

        self.match(TokenType.LEFT_PAREN)
        if self.lookahead.type != TokenType.RIGHT_PAREN:
            self.parse_params(func_token.value)
        self.match(TokenType.RIGHT_PAREN)

        self.match(TokenType.LEFT_BRACE)

        # Parse function body with the scope set as function name
        func_decl.add_child(self.parse_stmt_list(func_token.value))

        self.match(TokenType.RIGHT_BRACE)

        return func_decl

    # Parses function parameters
    def parse_params(self, scope):

        type = self.lookahead.value
        if self.lookahead.type not in [TokenType.INT, TokenType.FLOAT, TokenType.CHAR, TokenType.BOOL]:
            raise ParsingError(f"Unexpected type {type}", self.lookahead.line, self.lookahead.column)
        self.match(self.lookahead.type)
        arg_token = self.lookahead
        self.match(TokenType.IDENTIFIER)
        self.symbol_table.add_symbol(arg_token.value, type, scope, "variable")

        if self.lookahead.type == TokenType.COMMA:
            self.match(TokenType.COMMA)
            self.parse_params(scope)
        else:
            return

    # Parses a list of statements
    def parse_stmt_list(self, scope):
        stmt_list_token = Token(TokenType.PARSING_TOKEN, "StmtList", None, None)
        stmt_list = AST.AST(stmt_list_token)

        while self.lookahead is not None and self.lookahead.type != TokenType.RIGHT_BRACE:
            stmt = self.parse_stmt(scope)
            if stmt is not None:
                stmt_list.add_child(stmt)

        return stmt_list

    # Parses a single statement
    def parse_stmt(self, scope):

        if self.lookahead.type == TokenType.RETURN:
            return self.parse_return_stmt(scope)
        elif self.lookahead.type == TokenType.IF:
            return self.parse_IF_stmt(scope)
        elif self.lookahead.type == TokenType.WHILE:
            return self.parse_while_stmt(scope)
        elif self.lookahead.type == TokenType.FOR:
            return self.parse_for_stmt(scope)
        elif self.lookahead.type in [TokenType.INT, TokenType.FLOAT, TokenType.CHAR, TokenType.BOOL]:
            return self.parse_decl(scope)
        elif self.lookahead.type == TokenType.IDENTIFIER:
            return self.parse_expr_stmt(scope)
        else:
            raise ParsingError(f"Unexpected token {self.lookahead.value} in statement", self.lookahead.line, self.lookahead.column)

    # Parses an if statement
    def parse_IF_stmt(self, scope):
        # Match if token
        if_token_list = Token(TokenType.PARSING_TOKEN, "IfStmt", None, None)
        if_stmt_list = AST.AST(if_token_list)
        if_stmt = (AST.AST(self.lookahead)) 
        self.match(TokenType.IF)

        # Match boolean expression
        self.match(TokenType.LEFT_PAREN)
        if_stmt.add_child(self.parse_bool_expr(scope, "bool"))  
        self.match(TokenType.RIGHT_PAREN)

        self.match(TokenType.LEFT_BRACE)
        if_stmt.add_child(self.parse_stmt_list(scope))
        self.match(TokenType.RIGHT_BRACE)

        if_stmt_list.add_child(if_stmt)

        # Check for optional else part
        if self.lookahead.type == TokenType.ELSE:
            else_stmt = AST.AST(self.lookahead)
            self.match(TokenType.ELSE)

            # Check if else is another if
            if self.lookahead.type == TokenType.IF:
                else_stmt.add_child(self.parse_IF_stmt(scope))
            else:
                self.match(TokenType.LEFT_BRACE)
                else_stmt.add_child(self.parse_stmt_list(scope))
                self.match(TokenType.RIGHT_BRACE)
            if_stmt_list.add_child(else_stmt)

        return if_stmt_list

    def parse_while_stmt(self, scope):
        pass

    def parse_for_stmt(self, scope):
        pass

    # Parses a variable declaration
    def parse_var_decl(self, scope, variable_name, variable_type):

        # Check for optional initialization
        if self.lookahead.type == TokenType.ASSIGN:
            variable_declaration = AST.AST(self.lookahead)  
            self.match(TokenType.ASSIGN)

            variable_declaration.add_child(AST.AST(variable_name))
            variable_declaration.add_child(self.parse_bool_expr(scope, variable_type))
            self.match(TokenType.SEMICOLON)
            return variable_declaration
        else:
            self.match(TokenType.SEMICOLON)

    # Parses an expression statement/assignment
    def parse_expr_stmt(self, scope):
        identifier_token = self.lookahead
        self.match(TokenType.IDENTIFIER)
        valid = self.symbol_table.lookup(identifier_token.value, scope)
        if valid is None:
            raise ParsingError(f"Undeclared variable {identifier_token.value}", identifier_token.line, identifier_token.column)

        expr_stmt = AST.AST(self.lookahead)  
        self.match(TokenType.ASSIGN)

        variable_type = valid.type  
        expr_stmt.add_child(AST.AST(identifier_token))
        expr_stmt.add_child(self.parse_bool_expr(scope, variable_type))
        self.match(TokenType.SEMICOLON)
        return expr_stmt

    # Parses a return statement
    def parse_return_stmt(self, scope):
        # Get the return token and match it
        return_token = self.lookahead
        self.match(TokenType.RETURN)
        return_stmt = AST.AST(return_token)

        # Get the return type from the symbol table 
        return_type = self.symbol_table.lookup(self.lookahead.value, scope)

        # Parse the expression part of return 
        return_stmt.add_child(self.parse_bool_expr(scope, return_type.type))
        self.match(TokenType.SEMICOLON)
     
        return return_stmt
    
    # Parses a boolean expression
    def parse_bool_expr(self, scope, type):
        left = self.parse_expr(scope, type)
        if self.lookahead.type in [TokenType.EQUAL, TokenType.NOT_EQUAL, TokenType.LESS_THAN, TokenType.GREATER_THAN]:
            bool_operator = AST.AST(self.lookahead)
            self.match(self.lookahead.type)

            right = self.parse_expr(scope, type)
            bool_operator.add_child(left)
            bool_operator.add_child(right)
            return bool_operator
        else:
            if type == "bool":
                raise ParsingError(f"Expected boolean operator but found {self.lookahead.value}", self.lookahead.line, self.lookahead.column)
            else:
                return left

    # Parses an expression
    def parse_expr(self, scope, type):
        term = self.parse_term(scope, type)

        # See if there's an etail 
        if self.lookahead.type in [TokenType.PLUS, TokenType.MINUS]:
            etail = self.parse_etail(scope, term, type)
            return etail
        else:
            return term

    # Parses a term
    def parse_term(self, scope, type):
        factor = self.parse_factor(scope, type)

        # See if there's a ttail
        if self.lookahead.type in [TokenType.MULTIPLY, TokenType.DIVIDE]:
            ttail = self.parse_ttail(scope, factor, type)
            return ttail
        else:
            return factor

    # Parses a factor
    def parse_factor(self, scope, type):

        # Parenthesis
        if self.lookahead.type == TokenType.LEFT_PAREN:
            self.match(TokenType.LEFT_PAREN)
            expr = self.parse_bool_expr(scope, type)
            self.match(TokenType.RIGHT_PAREN)
            return expr
        # Ints
        elif self.lookahead.type == TokenType.NUMBER:
            if type != "int" and type != "bool":
                raise ParsingError(f"Cannot convert {type} to int", self.lookahead.line, self.lookahead.column)
            number_token = self.lookahead
            self.match(TokenType.NUMBER)
            return AST.AST(number_token)
        # Identifiers/Vars
        elif self.lookahead.type == TokenType.IDENTIFIER:
            identifier_token = self.lookahead
            self.match(TokenType.IDENTIFIER)
            valid = self.symbol_table.lookup(identifier_token.value, scope)
            
            # make sure variable is declared and types match
            if valid is None :
                raise ParsingError(f"Undeclared variable {identifier_token.value}", identifier_token.line, identifier_token.column)
            elif valid.type != type and type != "bool":
                raise ParsingError(f"Type mismatch: expected {type} but found {valid.type}", identifier_token.line, identifier_token.column)
            return AST.AST(identifier_token)
        # Floats
        elif self.lookahead.type == TokenType.FLOATING_NUMBER:
            if type != "float" and type != "bool":
                raise ParsingError(f"Cannot convert {type} to float", self.lookahead.line, self.lookahead.column)
            float_token = self.lookahead
            self.match(TokenType.FLOATING_NUMBER)
            return AST.AST(float_token)
        
        # Chars
        elif self.lookahead.type == TokenType.CHARACTER:
            if type != "char" and type != "bool":
                raise ParsingError(f"Cannot convert {type} to char", self.lookahead.line, self.lookahead.column)
            char_token = self.lookahead
            self.match(TokenType.CHARACTER)
            return AST.AST(char_token)

    # Parses etail for right side of expressions
    def parse_etail(self, scope, left, type):
        etail = AST.AST(self.lookahead)
        etail.add_child(left)
        self.match(self.lookahead.type)
        term = self.parse_term(scope, type)
        if self.lookahead.type in [TokenType.PLUS, TokenType.MINUS]:
            next_etail = self.parse_etail(scope, term, type)
            etail.add_child(next_etail)
            return etail
        else:
            etail.add_child(term)
            return etail

    # Parses ttail for right side of terms
    def parse_ttail(self, scope, left, type):
        ttail = AST.AST(self.lookahead)
        ttail.add_child(left)
        self.match(self.lookahead.type)
        factor = self.parse_factor(scope, type)
        if self.lookahead.type in [TokenType.MULTIPLY, TokenType.DIVIDE]:
            next_ttail = self.parse_ttail(scope, factor, type)
            ttail.add_child(next_ttail)
            return ttail
        else:
            ttail.add_child(factor)
            return ttail
