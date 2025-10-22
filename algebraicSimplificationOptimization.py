from instruction import Instruction

class AlgebraicSimplificationOptimization:
    def __init__(self, instructions):
        self.instructions = instructions

    def optimize(self):
        optimized_instructions = []
        for instr in self.instructions:
            # x + 0 = x
            # 0 + x = x
            if instr.operator == '+':
                if instr.arg1 == '0' or instr.arg1 == 0:
                    optimized_instructions.append(
                        Instruction(operator='=', arg1=instr.arg2, arg2=None, result=instr.result)
                    )
                elif instr.arg2 == '0' or instr.arg2 == 0:
                    optimized_instructions.append(
                        Instruction(operator='=', arg1=instr.arg1, arg2=None, result=instr.result)
                    )
                else:
                    optimized_instructions.append(instr)
            
            # x - 0 = x
            # x - x = 0
            elif instr.operator == '-':
                if instr.arg2 == '0' or instr.arg2 == 0:
                    optimized_instructions.append(
                        Instruction(operator='=', arg1=instr.arg1, arg2=None, result=instr.result)
                    )
                elif instr.arg1 == instr.arg2:
                    optimized_instructions.append(
                        Instruction(operator='=', arg1='0', arg2=None, result=instr.result)
                    )
                else:
                    optimized_instructions.append(instr)
            
            # x * 1 = x
            # 1 * x = x 
            # x * 0 = 0 
            # 0 * x = 0
            elif instr.operator == '*':
                if instr.arg1 == '1' or instr.arg1 == 1:
                    optimized_instructions.append(
                        Instruction(operator='=', arg1=instr.arg2, arg2=None, result=instr.result)
                    )
                elif instr.arg2 == '1' or instr.arg2 == 1:
                    optimized_instructions.append(
                        Instruction(operator='=', arg1=instr.arg1, arg2=None, result=instr.result)
                    )
                elif instr.arg1 == '0' or instr.arg1 == 0 or instr.arg2 == '0' or instr.arg2 == 0:
                    optimized_instructions.append(
                        Instruction(operator='=', arg1='0', arg2=None, result=instr.result)
                    )
                else:
                    optimized_instructions.append(instr)
            
            # x / 1 = x
            # x / x = 1 
            # 0 / x = 0
            elif instr.operator == '/':
                if instr.arg2 == '1' or instr.arg2 == 1:
                    optimized_instructions.append(
                        Instruction(operator='=', arg1=instr.arg1, arg2=None, result=instr.result)
                    )
                elif instr.arg1 == instr.arg2 and instr.arg1 != '0' and instr.arg1 != 0:
                    optimized_instructions.append(
                        Instruction(operator='=', arg1='1', arg2=None, result=instr.result)
                    )
                elif instr.arg1 == '0' or instr.arg1 == 0:
                    optimized_instructions.append(
                        Instruction(operator='=', arg1='0', arg2=None, result=instr.result)
                    )
                else:
                    optimized_instructions.append(instr)
                    
            else:
                optimized_instructions.append(instr)
        
        return optimized_instructions