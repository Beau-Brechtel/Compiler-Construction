import instruction
from lexer import TokenType
from lexer import Token
import AST

class TAC:
    def __init__(self):
        self.instructions = []
        self.temp_var_count = 1

    # Helper function to generate temporary variable names
    def generate_fresh_variable(self):
        var_name = f"t{self.temp_var_count}"
        self.temp_var_count += 1
        return var_name

    # Helper function to generate unique labels names
    def generate_fresh_label(self):
        label_name = f"L{self.temp_var_count}"
        self.temp_var_count += 1
        return label_name

    # Function to add a new instruction to the TAC list
    def add_instruction(self, label=None, operator=None, arg1=None, arg2=None, result=None):
        instr = instruction.Instruction(label, operator, arg1, arg2, result)
        self.instructions.append(instr)
        return instr

    # Function to get all generated instructions in compiler.py
    def get_instructions(self):
        return self.instructions
    
    # Returns a list of all children of node
    def children(self, node):
        children = []
        current = node.down if node else None
        while current is not None:
            children.append(current)
            current = current.right
        return children

    # Returns the first child of node
    def get_first_child(self, node):
        return node.down if node and node.down else None
    
    # Returns the nth child of node starting with 0
    def get_nth_child(self, node, n):
        current = node.down if node else None
        for _ in range(n):
            if current is None:
                return None
            current = current.right
        return current

    # Generates TAC for a given AST node
    def generate_TAC(self, node, label=None):
        # If node is none that means we are at a leaf and can go back up
        if node is None:
            return None
        
        token_type = node.get_token().type
        
        # Parsing tokens just represent that its children are a list of statements or delcarations
        if token_type == TokenType.PARSING_TOKEN:
            for child in self.children(node):
                self.generate_TAC(child)
            return None
        
        # Handles function definitions 
        if token_type == TokenType.MAIN:
            function_label = "main"
            self.add_instruction(label=function_label)
            self.generate_TAC(self.get_first_child(node))
            return None
        
        # Handles variable declarations
        if token_type == TokenType.ASSIGN:
            left = self.get_first_child(node)
            right = self.get_nth_child(node, 1)
            right_result = self.generate_TAC(right)
            self.add_instruction(operator='=', arg1=right_result, result=left.get_token().value)
            return left.get_token().value
        
        # Handles binary operations
        if token_type in {TokenType.PLUS, TokenType.MINUS, TokenType.MULTIPLY, TokenType.DIVIDE}:
            left = self.get_first_child(node)
            right = self.get_nth_child(node, 1)
            left_result = self.generate_TAC(left)
            right_result = self.generate_TAC(right)
            temp_var = self.generate_fresh_variable()
            self.add_instruction(operator=node.get_token().value, arg1=left_result, arg2=right_result, result=temp_var)
            return temp_var
        
        # Handles return statements
        if token_type == TokenType.RETURN:
            expr_node = self.get_first_child(node)
            expr_result = self.generate_TAC(expr_node)
            self.add_instruction(operator=node.get_token().value, arg1=expr_result)
            return None
        
        # Handles leaf nodes like numbers and identifiers
        if token_type in {TokenType.NUMBER, TokenType.IDENTIFIER, TokenType.FLOATING_NUMBER, TokenType.CHARACTER}:
            return node.get_token().value
        
        return None
        

