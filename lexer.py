import re
from enum import Enum
from typing import List
from Errors import LexerError


class TokenType(Enum):

    # Literals
    NUMBER = "NUMBER"
    FLOATING_NUMBER = "FLOATING_NUMBER"
    STRING = "STRING"
    CHARACTER = "CHARACTER"
    IDENTIFIER = "IDENTIFIER"
    INVALID_IDENTIFIER = "INVALID_IDENTIFIER"
    
    # Keywords 
    IF = "IF"
    ELSE = "ELSE"
    WHILE = "WHILE"
    FOR = "FOR"
    RETURN = "RETURN"
    MAIN = "MAIN"

    # Keywords - data types
    INT = "INT"
    FLOAT = "FLOAT"
    CHAR = "CHAR"
    BOOL = "BOOL"
    VOID = "VOID"

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
    
    # Other
    WHITESPACE = "WHITESPACE"
    UNKNOWN = "UNKNOWN"
    PARSING_TOKEN = "PARSING_TOKEN"  


class Token:
    def __init__(self, type: TokenType, value: str, line: int, column: int):
        self.type = type
        self.value = value
        self.line = line
        self.column = column
    
    def __str__(self) -> str:
        # String print out
        if self.type == TokenType.PARSING_TOKEN:
            return f""
        return f"{self.type.value}: {self.value}, At line {self.line}, column {self.column}"
    


class Lexer:
    
    def __init__(self):
        # Initialize Lexer
        # Token patterns
        # Regular Expressions created with help from Copilot
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
            (r'\bbool\b', TokenType.BOOL),
            (r'\bvoid\b', TokenType.VOID),

            # Invalid identifiers
            (r'\d+[a-zA-Z_][a-zA-Z0-9_]*', TokenType.INVALID_IDENTIFIER),
            
            # Numbers
            (r'\d+\.\d+', TokenType.FLOATING_NUMBER),  
            (r'\d+', TokenType.NUMBER),       
            
            # Identifiers
            (r'[a-zA-Z_][a-zA-Z0-9_]*', TokenType.IDENTIFIER),
            
            # String literals and character literals
            (r'"[^"]*"', TokenType.STRING),
            (r"'[^']*'", TokenType.CHARACTER),

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
            
            # Whitespace
            (r'[ \t]+', TokenType.WHITESPACE),
        ]
        
        # Compile all regex patterns 
        self.compiled_patterns = [(re.compile(pattern), token_type) for pattern, token_type in self.token_patterns]
    
    # Tokenize the given source code and return a list of tokens
    def tokenize(self, source_code: str) -> List[Token]:
    
        # Create empty token list that we will end up returning
        tokens = []
        
        # Handle comments first by removing them from the entire source
        source_code = self._remove_comments(source_code)
        
        # Split source code into lines for line/column tracking
        lines = source_code.split('\n')
        
        # Loop through all the lines 
        for line_num, line in enumerate(lines, 1):
            position = 0

            # Going through each line
            while position < len(line):
                match_found = False

                # Try to match each pattern by going through all compiled patterns
                for pattern, token_type in self.compiled_patterns:
                    match = pattern.match(line, position)
                    if match:
                        value = match.group(0)
                        
                        # Skip whitespace tokens
                        if token_type == TokenType.WHITESPACE:
                            position = match.end()
                            match_found = True
                            break
                        
                        # Handle invalid identifiers
                        if token_type == TokenType.INVALID_IDENTIFIER:
                            raise LexerError(f"Invalid identifier '{value}'", line_num, position + 1)
                        
                        # Create token for tokens that are not whitespace
                        token = Token(token_type, value, line_num, position + 1) 
                        tokens.append(token)
                        
                        # Move position forward
                        position = match.end()
                        match_found = True
                        break
                
                # If no pattern matched, throw error for unknown character
                if not match_found:
                    unknown_char = line[position]
                    raise LexerError(f"Unknown character seen during tokenization: '{unknown_char}'", line_num, position + 1)

        return tokens
    
    # Takes in source code string and removes all comments
    # Returns source code as a string without comments
    def _remove_comments(self, source_code: str) -> str:
        # Remove multi-line comments 
        multiline_comment = re.compile(r'/\*.*?\*/', re.DOTALL)
        source_code = multiline_comment.sub('', source_code)
        
        # Remove single-line comments 
        oneline_comment = re.compile(r'//.*')
        source_code = oneline_comment.sub('', source_code)

        return source_code
