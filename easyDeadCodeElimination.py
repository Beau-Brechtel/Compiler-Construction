class EasyDeadCodeElimination:
    def __init__(self, instructions):
        self.instructions = instructions
        
    def optimize(self):
        used_vars = set()
        
        for instr in self.instructions:
            if instr.arg1:
                used_vars.add(instr.arg1)
            if instr.arg2:
                used_vars.add(instr.arg2)
        
        
        for instr in self.instructions:

            if instr.operator in ["if", "call"]:
                instr.is_dead = False  
            elif instr.result and instr.result not in used_vars:
                instr.is_dead = True
            else:
                instr.is_dead = False

        self.instructions = [instr for instr in self.instructions if not instr.is_dead]

        return self.instructions