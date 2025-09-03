from lexer import Token, TokenType
from typing import List, Optional, Dict, Any

# Simple syntax tree node - just a dictionary with type and data
class SyntaxTree:
    def __init__(self, node_type: str, **data):
        self.type = node_type
        self.data = data
    
    def __repr__(self):
        return f"SyntaxTree({self.type}, {self.data})"

class ParseError(Exception):
    def __init__(self, message: str, token: Token):
        self.message = message
        self.token = token
        super().__init__(f"{message} at line {token.line}, column {token.column}")

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.current = 0
    
    def current_token(self) -> Token:
        """Get the current token"""
        if self.current < len(self.tokens):
            return self.tokens[self.current]
        return self.tokens[-1]  # Return EOF token
    
    def peek_token(self) -> Token:
        """Peek at the next token without consuming it"""
        if self.current + 1 < len(self.tokens):
            return self.tokens[self.current + 1]
        return self.tokens[-1]  # Return EOF token
    
    def advance(self) -> Token:
        """Consume and return the current token"""
        token = self.current_token()
        if self.current < len(self.tokens) - 1:
            self.current += 1
        return token
    
    def match(self, token_type: TokenType) -> bool:
        """Check if current token matches the given type"""
        return self.current_token().type == token_type
    
    def consume(self, token_type: TokenType, error_message: str) -> Token:
        """Consume a token of the expected type or raise an error"""
        if self.match(token_type):
            return self.advance()
        raise ParseError(error_message, self.current_token())
    
    # Grammar rule: program -> func_decl_list
    def parse_program(self) -> SyntaxTree:
        """Parse the entire program"""
        func_decls = self.parse_func_decl_list()
        return SyntaxTree("program", functions=func_decls)
    
    # Grammar rule: func_decl_list -> func_decl | func_decl_list func_decl
    def parse_func_decl_list(self) -> List[SyntaxTree]:
        """Parse a list of function declarations"""
        func_decls = []
        
        while not self.match(TokenType.EOF):
            func_decl = self.parse_func_decl()
            func_decls.append(func_decl)
        
        return func_decls
    
    # Grammar rule: func_decl -> type IDENTIFIER () { stmt_list }
    def parse_func_decl(self) -> SyntaxTree:
        """Parse a function declaration"""
        # Parse return type
        return_type = self.parse_type()
        
        # Parse function name
        name_token = self.consume(TokenType.IDENTIFIER, "Expected function name")
        
        # Parse parentheses
        self.consume(TokenType.LEFT_PAREN, "Expected '(' after function name")
        self.consume(TokenType.RIGHT_PAREN, "Expected ')' after function parameters")
        
        # Parse function body
        self.consume(TokenType.LEFT_BRACE, "Expected '{' to start function body")
        stmt_list = self.parse_stmt_list()
        self.consume(TokenType.RIGHT_BRACE, "Expected '}' to end function body")
        
        return SyntaxTree("function", return_type=return_type, name=name_token.value, statements=stmt_list)
    
    # Grammar rule: stmt_list -> stmt | stmt_list stmt
    def parse_stmt_list(self) -> List[SyntaxTree]:
        """Parse a list of statements"""
        statements = []
        
        while not self.match(TokenType.RIGHT_BRACE) and not self.match(TokenType.EOF):
            stmt = self.parse_stmt()
            statements.append(stmt)
        
        return statements
    
    # Grammar rule: stmt -> return_stmt | var_decl | assignment | if_stmt | while_stmt | for_stmt
    def parse_stmt(self) -> SyntaxTree:
        """Parse a single statement"""
        if self.match(TokenType.RETURN):
            return self.parse_return_stmt()
        elif self.match(TokenType.IF):
            return self.parse_if_stmt()
        elif self.match(TokenType.WHILE):
            return self.parse_while_stmt()
        elif self.match(TokenType.FOR):
            return self.parse_for_stmt()
        elif self.match(TokenType.INT) or self.match(TokenType.FLOAT) or \
             self.match(TokenType.CHAR) or self.match(TokenType.DOUBLE):
            return self.parse_var_decl()
        elif self.match(TokenType.IDENTIFIER):
            return self.parse_assignment()
        else:
            raise ParseError("Expected statement", self.current_token())
    
    # Grammar rule: return_stmt -> "return" Expression ;
    def parse_return_stmt(self) -> SyntaxTree:
        """Parse a return statement"""
        self.consume(TokenType.RETURN, "Expected 'return'")
        expression = self.parse_expression()
        self.consume(TokenType.SEMICOLON, "Expected ';' after return statement")
        return SyntaxTree("return", expression=expression)
    
    # Grammar rule: var_decl -> type IDENTIFIER = Expression ; | type IDENTIFIER ;
    def parse_var_decl(self) -> SyntaxTree:
        """Parse a variable declaration"""
        var_type = self.parse_type()
        name_token = self.consume(TokenType.IDENTIFIER, "Expected variable name")
        
        initial_value = None
        if self.match(TokenType.ASSIGN):
            self.advance()  # consume '='
            initial_value = self.parse_expression()
        
        self.consume(TokenType.SEMICOLON, "Expected ';' after variable declaration")
        return SyntaxTree("var_decl", var_type=var_type, name=name_token.value, initial_value=initial_value)
    
    # Grammar rule: assignment -> IDENTIFIER = Expression ;
    def parse_assignment(self) -> SyntaxTree:
        """Parse an assignment statement"""
        name_token = self.consume(TokenType.IDENTIFIER, "Expected identifier")
        self.consume(TokenType.ASSIGN, "Expected '=' in assignment")
        expression = self.parse_expression()
        self.consume(TokenType.SEMICOLON, "Expected ';' after assignment")
        return SyntaxTree("assignment", identifier=name_token.value, expression=expression)
    
    # Grammar rule: if_stmt -> if ( Expression ) { stmt_list } | if ( Expression ) { stmt_list } else { stmt_list }
    def parse_if_stmt(self) -> SyntaxTree:
        """Parse an if statement"""
        self.consume(TokenType.IF, "Expected 'if'")
        self.consume(TokenType.LEFT_PAREN, "Expected '(' after 'if'")
        condition = self.parse_expression()
        self.consume(TokenType.RIGHT_PAREN, "Expected ')' after if condition")
        
        self.consume(TokenType.LEFT_BRACE, "Expected '{' after if condition")
        then_stmts = self.parse_stmt_list()
        self.consume(TokenType.RIGHT_BRACE, "Expected '}' after if body")
        
        else_stmts = None
        if self.match(TokenType.ELSE):
            self.advance()  # consume 'else'
            self.consume(TokenType.LEFT_BRACE, "Expected '{' after 'else'")
            else_stmts = self.parse_stmt_list()
            self.consume(TokenType.RIGHT_BRACE, "Expected '}' after else body")
        
        return SyntaxTree("if", condition=condition, then_stmts=then_stmts, else_stmts=else_stmts)
    
    # Grammar rule: while_stmt -> while ( Expression ) { stmt_list }
    def parse_while_stmt(self) -> SyntaxTree:
        """Parse a while statement"""
        self.consume(TokenType.WHILE, "Expected 'while'")
        self.consume(TokenType.LEFT_PAREN, "Expected '(' after 'while'")
        condition = self.parse_expression()
        self.consume(TokenType.RIGHT_PAREN, "Expected ')' after while condition")
        
        self.consume(TokenType.LEFT_BRACE, "Expected '{' after while condition")
        body_stmts = self.parse_stmt_list()
        self.consume(TokenType.RIGHT_BRACE, "Expected '}' after while body")
        
        return SyntaxTree("while", condition=condition, body_stmts=body_stmts)
    
    # Grammar rule: for_stmt -> for ( var_decl | assignment ; Expression ; assignment ) { stmt_list }
    def parse_for_stmt(self) -> SyntaxTree:
        """Parse a for statement"""
        self.consume(TokenType.FOR, "Expected 'for'")
        self.consume(TokenType.LEFT_PAREN, "Expected '(' after 'for'")
        
        # Parse initialization (var_decl or assignment)
        if self.match(TokenType.INT) or self.match(TokenType.FLOAT) or \
           self.match(TokenType.CHAR) or self.match(TokenType.DOUBLE):
            init = self.parse_var_decl()
        else:
            init = self.parse_assignment()
        
        # Parse condition
        condition = self.parse_expression()
        self.consume(TokenType.SEMICOLON, "Expected ';' after for condition")
        
        # Parse update (assignment without semicolon)
        update_name = self.consume(TokenType.IDENTIFIER, "Expected identifier in for update")
        self.consume(TokenType.ASSIGN, "Expected '=' in for update")
        update_expr = self.parse_expression()
        update = SyntaxTree("assignment", identifier=update_name.value, expression=update_expr)
        
        self.consume(TokenType.RIGHT_PAREN, "Expected ')' after for clauses")
        
        # Parse body
        self.consume(TokenType.LEFT_BRACE, "Expected '{' after for clauses")
        body_stmts = self.parse_stmt_list()
        self.consume(TokenType.RIGHT_BRACE, "Expected '}' after for body")
        
        return SyntaxTree("for", init=init, condition=condition, update=update, body_stmts=body_stmts)
    
    # Grammar rule: type -> int | float | char | double
    def parse_type(self) -> str:
        """Parse a type specifier"""
        if self.match(TokenType.INT):
            self.advance()
            return "int"
        elif self.match(TokenType.FLOAT):
            self.advance()
            return "float"
        elif self.match(TokenType.CHAR):
            self.advance()
            return "char"
        elif self.match(TokenType.DOUBLE):
            self.advance()
            return "double"
        else:
            raise ParseError("Expected type specifier", self.current_token())
    
    # Grammar rule: Expression -> Expression OPERATOR NUM | NUM
    def parse_expression(self) -> SyntaxTree:
        """Parse an expression with left-associative operators"""
        left = self.parse_primary()
        
        while self.match(TokenType.PLUS) or self.match(TokenType.MINUS) or \
              self.match(TokenType.MULTIPLY) or self.match(TokenType.DIVIDE) or \
              self.match(TokenType.EQUAL) or self.match(TokenType.NOT_EQUAL) or \
              self.match(TokenType.LESS_THAN) or self.match(TokenType.GREATER_THAN):
            
            operator_token = self.advance()
            right = self.parse_primary()
            left = SyntaxTree("binary_op", left=left, operator=operator_token.value, right=right)
        
        return left
    
    def parse_primary(self) -> SyntaxTree:
        """Parse a primary expression (number or identifier)"""
        if self.match(TokenType.NUMBER):
            token = self.advance()
            return SyntaxTree("number", value=token.value)
        elif self.match(TokenType.IDENTIFIER):
            token = self.advance()
            return SyntaxTree("identifier", name=token.value)
        elif self.match(TokenType.LEFT_PAREN):
            self.advance()  # consume '('
            expr = self.parse_expression()
            self.consume(TokenType.RIGHT_PAREN, "Expected ')' after expression")
            return expr
        else:
            raise ParseError("Expected number, identifier, or '('", self.current_token())

    