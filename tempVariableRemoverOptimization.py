from instruction import Instruction

class tempVarRemover:
    def __init__(self, instructions):
        self.instructions = instructions
    
    def optimize(self):
        optimized_instructions = []
        
        for i in range(len(self.instructions)):
            instr = self.instructions[i]
            prev_instr = self.instructions[i-1] if i > 0 else None
            if instr.operator == '=' and prev_instr and instr.arg1 == prev_instr.result and instr.arg2 is None:
                optimized_instructions[-1].result = instr.result
            else:
                optimized_instructions.append(instr)

        return optimized_instructions
        