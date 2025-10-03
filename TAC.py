import instruction
from lexer import TokenType
from lexer import Token
import AST
import SymbolTable
class TAC:
    def __init__(self, symbol_table):
        self.instructions = []
        self.temp_var_count = 1
        self.temp_label_count = 1
        self.symbol_table = symbol_table

    # Helper function to generate temporary variable names
    def generate_fresh_variable(self):
        var_name = f"t{self.temp_var_count}"
        self.temp_var_count += 1
        return var_name

    # Helper function to generate unique labels names
    def generate_fresh_label(self):
        label_name = f"L{self.temp_label_count}"
        self.temp_label_count += 1
        return label_name

    # Function to add a new instruction to the TAC list
    def add_instruction(self, label=None, operator=None, arg1=None, arg2=None, result=None):
        instr = instruction.Instruction(label, operator, arg1, arg2, result)
        self.instructions.append(instr)
        return instr
    
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
    
    def identifier_is_function(self, identifier, scope):
        entry = self.symbol_table.lookup(identifier, scope)
        return entry is not None and entry.kind == 'function'
        
    # Returns the nth child of node starting with 0
    def get_nth_child(self, node, n):
        current = node.down if node else None
        for _ in range(n):
            if current is None:
                return None
            current = current.right
        return current

    # Generates TAC for a given AST node
    def generate_TAC(self, node, label=None, scope ='global'):
        # If node is none that means we are at a leaf and can go back up
        if node is None:
            return None
        
        # Get the type of the token to determine what to do
        token_type = node.get_token().type
        
        if token_type == TokenType.PARSING_TOKEN:
            if node.get_token().value == "IfStmt":
                end_label = self.generate_TAC_for_if(node, scope)
                self.add_instruction(label=end_label)
                return None
            else:
                for child in self.children(node):
                    self.generate_TAC(child, scope=scope)
                return None

        # Handles function definitions
        if token_type == TokenType.IDENTIFIER and self.identifier_is_function(node.get_token().value, scope):
            function_label = node.get_token().value
            self.add_instruction(label=function_label)
            self.generate_TAC(self.get_first_child(node), scope=function_label)
            return None

        if token_type == TokenType.ASSIGN:
            return self.generate_TAC_for_assignment(node, scope)
        
        if token_type in {TokenType.PLUS, TokenType.MINUS, TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.GREATER_THAN, TokenType.LESS_THAN, TokenType.EQUAL, TokenType.NOT_EQUAL}:
            return self.generate_TAC_for_expression(node, scope=scope)
        
        if token_type == TokenType.RETURN:
            return self.generate_TAC_for_return(node, scope)
        
        if token_type == TokenType.WHILE:
            end_label = self.generate_TAC_for_while(node, scope)
            self.add_instruction(label=end_label)
            return None

        if token_type == TokenType.FOR:
            end_label = self.generate_TAC_for_for(node, scope)
            self.add_instruction(label=end_label)
            return None

        # Handles leaf nodes like numbers and identifiers
        if token_type in {TokenType.NUMBER, TokenType.IDENTIFIER, TokenType.FLOATING_NUMBER, TokenType.CHARACTER}:
            return node.get_token().value
        
        return None
    
    # Handles TAC Generation for declerations
    def generate_TAC_for_assignment(self, node, scope):
        left = self.get_first_child(node)
        right = self.get_nth_child(node, 1)
        right_result = self.generate_TAC(right, scope=scope)
        self.add_instruction(operator='=', arg1=right_result, result=left.get_token().value)
        return left.get_token().value

    # Handles TAC Generation for return statements
    def generate_TAC_for_return(self, node, scope):
        # Get the expression node that will be returned
        expr_node = self.get_first_child(node)
        expr_result = self.generate_TAC(expr_node, scope=scope)
        self.add_instruction(operator=node.get_token().value, arg1=expr_result)
        return None

    # Handles TAC Generation for binary expressions
    def generate_TAC_for_expression(self, node, scope):
            # Get the left and right child nodes
            left = self.get_first_child(node)
            right = self.get_nth_child(node, 1)

            # Recursively generate TAC for left and right 
            left_result = self.generate_TAC(left, scope=scope)
            right_result = self.generate_TAC(right, scope=scope)

            # Create a new temporary variable to hold the result and add the instruction
            temp_var = self.generate_fresh_variable()
            self.add_instruction(operator=node.get_token().value, arg1=left_result, arg2=right_result, result=temp_var)
           
            # Send the temp variable back up so that it can be used to set variables to the right value
            return temp_var

    # Handles TAC Generation for if statements    
    def generate_TAC_for_if(self, node, scope):
        # Get the condition, if body, and else body nodes
        if_node = self.get_first_child(node)
        condition_node = self.get_first_child(if_node)
        else_node = self.get_nth_child(node, 1)
        condition_result = self.generate_TAC(condition_node, scope=scope)

        # Generate Labels for the if-else structure
        if_label = self.generate_fresh_label()
        else_label = self.generate_fresh_label() if else_node else None
        end_label = self.generate_fresh_label()

        # Generate TAC for the if-else structure
        self.add_instruction(operator= "if", arg1=condition_result, arg2=if_label, result= else_label if else_label else end_label)
        self.add_instruction(label=if_label)
        self.generate_TAC(self.get_nth_child(if_node, 1), scope=scope)
        self.add_instruction(operator='goto', result=end_label)
        
        # If there is an else node, generate TAC for it
        if else_node:
            self.add_instruction(label=else_label)
            self.generate_TAC(self.get_first_child(else_node), scope=scope)
            self.add_instruction(operator='goto', result=end_label)

        return end_label

    # Handles TAC Generation for while loops
    def generate_TAC_for_while(self, node, scope):
        # Get the condition and body nodes
        conditon_node = self.get_first_child(node)
        body_node = self.get_nth_child(node, 1)

        # Generate Labels for the loop
        start_label = self.generate_fresh_label()
        body_label = self.generate_fresh_label()
        end_label = self.generate_fresh_label()

        # Generate TAC for the loop
        self.add_instruction(label=start_label)
        condition_result = self.generate_TAC(conditon_node, scope=scope)
        self.add_instruction(operator="if", arg1=condition_result, arg2=body_label, result=end_label)
        self.add_instruction(label=body_label)
        self.generate_TAC(body_node, scope=scope)
        self.add_instruction(operator='goto', result=start_label)
        return end_label

    # Handles TAC Generation for for loops
    def generate_TAC_for_for(self, node, scope):
        # Add the initialization part to last label
        self.generate_TAC(self.get_first_child(node), scope=scope) 

        # Get the condition, increment, and body nodes
        condition_node = self.get_nth_child(node, 1)
        increment_node = self.get_nth_child(node, 2)
        body_node = self.get_nth_child(node, 3)

        # Generate Labels for the loop
        start_label = self.generate_fresh_label()
        body_label = self.generate_fresh_label()
        end_label = self.generate_fresh_label()

        # Generate TAC for the loop
        self.add_instruction(label=start_label)
        condition_result = self.generate_TAC(condition_node, scope=scope)
        self.add_instruction(operator="if", arg1=condition_result, arg2=body_label, result=end_label)
        self.add_instruction(label=body_label)
        self.generate_TAC(body_node, scope=scope)
        self.generate_TAC(increment_node, scope=scope)
        self.add_instruction(operator='goto', result=start_label)
        return end_label