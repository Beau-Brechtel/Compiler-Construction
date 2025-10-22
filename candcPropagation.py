from instruction import Instruction

class CandCPropagation:
    def __init__(self, instructions):
        self.instructions = instructions

    def optimize(self):
        constant_values = {}
        optimized_instructions = []

        for instr in self.instructions:
            if instr.operator == '=' and instr.arg2 is None:
                # Handle both constant and copy propagation
                if instr.arg1 in constant_values:
                    # Copy propagation: resolve the value and propagate it
                    new_value = constant_values[instr.arg1]
                    constant_values[instr.result] = new_value
                    optimized_instructions.append(
                        Instruction(operator='=', arg1=new_value, arg2=None, result=instr.result)
                    )
                else:
                    # Constant propagation: store literal value
                    constant_values[instr.result] = instr.arg1
                    optimized_instructions.append(instr)
            elif instr.label is not None:
                # Create fresh scope on a new block
                optimized_instructions.append(instr)
                constant_values = {}
            else:
                if instr.arg1 in constant_values:
                    arg1 = constant_values[instr.arg1]
                else:
                    arg1 = instr.arg1

                if instr.arg2 in constant_values:
                    arg2 = constant_values[instr.arg2]
                else:
                    arg2 = instr.arg2

                optimized_instructions.append(
                    Instruction(operator=instr.operator, arg1=arg1, arg2=arg2, result=instr.result)
                )

        return optimized_instructions