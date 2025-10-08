from instruction import Instruction

class ConstantFoldingOptimization:
    def __init__(self, instructions):
        self.instructions = instructions

    def is_numeric(self, value):
        if isinstance(value, str):
            try:
                if '.' in value:
                    float(value)
                    return True
                else:
                    int(value)
                    return True
            except ValueError:
                return False
        return False
    
    def get_numeric_value(self, value):
        print(value)
        if isinstance(value, (int, float)):
            return value
        if isinstance(value, str):
            if '.' in value:
                return float(value)
            else:
                return int(value)
        return None

    def optimize(self):
        optimized_instructions = []
        for instr in self.instructions:
            if (instr.operator in ('+', '-', '*', '/') and 
                self.is_numeric(instr.arg1) and self.is_numeric(instr.arg2)):
                
                num1 = self.get_numeric_value(instr.arg1)
                num2 = self.get_numeric_value(instr.arg2)
                
                if instr.operator == '+':
                    result = num1 + num2
                elif instr.operator == '-':
                    result = num1 - num2
                elif instr.operator == '*':
                    result = num1 * num2
                elif instr.operator == '/':
                    if isinstance(num1, int) and isinstance(num2, int) and num1 % num2 == 0:
                        result = num1 // num2
                    else:
                        result = num1 / num2
                    
                optimized_instructions.append(Instruction(operator='=', arg1=result, arg2=None, result=instr.result))
            else:
                optimized_instructions.append(instr)
        return optimized_instructions