from lexer import Token

# https://github.com/wumphlett/COMP-3220/blob/main/HW-4/AST.rb
# Based AST implementation off of COMP 3220 AST tree given in class
class AST:

    def __init__(self, token):
        self.token = token
        self.down = None
        self.right = None

    def add_child(self, child_node):
        if(child_node is None):
            return 
        t = self.down
        if(t is None):
            self.down = child_node
        else:
            while(t.right is not None):
                t = t.right
            t.right = child_node
        return
    
    def print_tree(self, level=0):
        print('  ' * level + str(self.token))
        child = self.down
        while child is not None:
            child.print_tree(level + 1)
            child = child.right

    def get_token(self):
        return self.token
    
   

    

