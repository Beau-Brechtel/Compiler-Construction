import re
from enum import Enum
from dataclasses import dataclass
from typing import List, Optional


class TokenType(Enum):
    # Tokens

    # Literals
    NUMBER = "NUMBER"
    STRING = "STRING"
    IDENTIFIER = "IDENTIFIER"
    
    # Keywords 
    IF = "IF"
    ELSE = "ELSE"
    WHILE = "WHILE"
    FOR = "FOR"
    RETURN = "RETURN"
    MAIN = "MAIN"
    INT = "INT"
    FLOAT = "FLOAT"
    CHAR = "CHAR"
    DOUBLE = "DOUBLE"

    # Operators
    PLUS = "PLUS"
    MINUS = "MINUS"
    MULTIPLY = "MULTIPLY"
    DIVIDE = "DIVIDE"
    ASSIGN = "ASSIGN"
    
    # Comparison operators
    EQUAL = "EQUAL"
    NOT_EQUAL = "NOT_EQUAL"
    LESS_THAN = "LESS_THAN"
    GREATER_THAN = "GREATER_THAN"
    
    # Symbols and delimiters
    SEMICOLON = "SEMICOLON"
    COMMA = "COMMA"
    LEFT_PAREN = "LEFT_PAREN"
    RIGHT_PAREN = "RIGHT_PAREN"
    LEFT_BRACE = "LEFT_BRACE"
    RIGHT_BRACE = "RIGHT_BRACE"
    
    # Special tokens
    COMMENT = "COMMENT"
    WHITESPACE = "WHITESPACE"
    NEWLINE = "NEWLINE"
    EOF = "EOF"
    UNKNOWN = "UNKNOWN"


@dataclass
class Token:
    type: TokenType
    value: str
    line: int
    column: int
    
    def __str__(self) -> str:
        # String print out
        return f"{self.type.value}: {self.value}, At line {self.line}, column {self.column}"


class Lexer:
    
    def __init__(self):
        #Initialize Lexer
        # Token patterns 
        self.token_patterns = [
            # Keywords 
            (r'\bif\b', TokenType.IF),
            (r'\belse\b', TokenType.ELSE),
            (r'\bwhile\b', TokenType.WHILE),
            (r'\bfor\b', TokenType.FOR),
            (r'\breturn\b', TokenType.RETURN),
            (r'\bmain\b', TokenType.MAIN),
            (r'\bint\b', TokenType.INT),
            (r'\bfloat\b', TokenType.FLOAT),
            (r'\bchar\b', TokenType.CHAR),
            (r'\bdouble\b', TokenType.DOUBLE),

            # Numbers
            (r'\d+\.\d+', TokenType.NUMBER),  
            (r'\d+', TokenType.NUMBER),       
            
            # Identifiers
            (r'[a-zA-Z_][a-zA-Z0-9_]*', TokenType.IDENTIFIER),
            
            # String literals
            (r'"[^"]*"', TokenType.STRING),
            (r"'[^']*'", TokenType.STRING),
            
            # Two-character operators 
            (r'==', TokenType.EQUAL),
            (r'!=', TokenType.NOT_EQUAL),
            
            # Single-character operators and delimiters
            (r'\+', TokenType.PLUS),
            (r'-', TokenType.MINUS),
            (r'\*', TokenType.MULTIPLY),
            (r'/', TokenType.DIVIDE),
            (r'=', TokenType.ASSIGN),
            (r'<', TokenType.LESS_THAN),
            (r'>', TokenType.GREATER_THAN),
            (r';', TokenType.SEMICOLON),
            (r',', TokenType.COMMA),
            (r'\(', TokenType.LEFT_PAREN),
            (r'\)', TokenType.RIGHT_PAREN),
            (r'\{', TokenType.LEFT_BRACE),
            (r'\}', TokenType.RIGHT_BRACE),
            
            # Whitespace and newlines
            (r'[ \t]+', TokenType.WHITESPACE),
            (r'\n', TokenType.NEWLINE),
        ]
        
        # Compile all regex patterns 
        self.compiled_patterns = [(re.compile(pattern), token_type) 
                                for pattern, token_type in self.token_patterns]
    
    def tokenize(self, source_code: str) -> List[Token]:
        # Tokenize the given source code and return a list of tokens
    
        # Create empty token list
        tokens = []
        
        # Handle comments first by removing them from the entire source
        source_code = self._remove_comments(source_code)
        
        lines = source_code.split('\n')
        
        # Loop through each line 
        for line_num, line in enumerate(lines, 1):
            column = 1
            position = 0

            # Loop through the line
            while position < len(line):
                match_found = False

                # Try to match each pattern by going through all compiled patterns
                for pattern, token_type in self.compiled_patterns:
                    match = pattern.match(line, position)
                    if match:
                        value = match.group(0)
                        
                        # Skip whitespace tokens
                        if token_type == TokenType.WHITESPACE or token_type == TokenType.NEWLINE:
                            position = match.end()
                            column += len(value)
                            match_found = True
                            break
                        
                        # Create token for tokens that are not whitespace
                        token = Token(token_type, value, line_num, column)
                        tokens.append(token)
                        
                        # Move position forward
                        position = match.end()
                        column += len(value)
                        match_found = True
                        break
                
                # If no pattern matched, go to UNKNOWN token
                if not match_found:
                    unknown_char = line[position]
                    token = Token(TokenType.UNKNOWN, unknown_char, line_num, column)
                    tokens.append(token)
                    position += 1
                    column += 1
        
        # Add EOF token
        final_line = len(lines)
        final_column = len(lines[-1]) + 1 if lines else 1
        tokens.append(Token(TokenType.EOF, '', final_line, final_column))
        
        return tokens
    
    def _remove_comments(self, source_code: str) -> str:
        # Remove multi-line comments /* ... */
        multiline_comment = re.compile(r'/\*.*?\*/', re.DOTALL)
        source_code = multiline_comment.sub('', source_code)
        
        # Remove single-line comments // ...
        oneline_comment = re.compile(r'//.*')
        source_code = oneline_comment.sub('', source_code)

        return source_code
