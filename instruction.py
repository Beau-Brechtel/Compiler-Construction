# https://www.geeksforgeeks.org/compiler-design/three-address-code-compiler/
# Used for object design of what an instruction is
class Instruction:
    def __init__(self, label=None, operator=None, arg1=None, arg2=None, result=None):
        self.label = label
        self.operator = operator
        self.arg1 = arg1
        self.arg2 = arg2
        self.result = result

    def __str__(self):
        parts = []
        if self.label is not None:
            parts.append(f"\n{self.label}:")
            
        if self.operator == 'if':
            parts.append(f"if {self.arg1} goto {self.arg2} else goto {self.result}")
        elif self.operator == 'call':
            parts.append(f"{self.result} = {self.arg1}({self.arg2})")
        elif self.operator == 'goto':
            parts.append(f"goto {self.result}")
        elif self.result is not None and self.operator == '=':
            parts.append(f"{self.result} = {self.arg1}")
        elif self.result is not None and self.arg1 is not None and self.arg2 is not None and self.operator is not None:
            parts.append(f"{self.result} = {self.arg1} {self.operator} {self.arg2}")
        elif self.operator == 'return':
            parts.append(f"return {self.arg1}")
        elif self.operator is not None or self.result is not None or self.arg1 is not None or self.arg2 is not None:
            instruction_parts = []
            if self.result is not None:
                instruction_parts.append(f"{self.result}")
            if self.arg1 is not None:
                instruction_parts.append(f"{self.arg1}")
            if self.operator is not None:
                instruction_parts.append(f"{self.operator}")
            if self.arg2 is not None:
                instruction_parts.append(f"{self.arg2}")
            parts.append(' '.join(instruction_parts))
        
        return ' '.join(parts)
    
    def to_string_simple(self):
        """Simple string representation showing all components with labels and None values"""
        return (f"label:{self.label} operator:{self.operator} "
                f"arg1:{self.arg1} arg2:{self.arg2} result:{self.result}\n")
    
