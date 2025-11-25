from instruction import Instruction
from assemblyInstruction import AssemblyInstruction
from SymbolTable import symbol_table

# Used chatgpt to help figure out how to convert to assembly and to check output
class assembler:

    def __init__(self, symbol_table):
        self.assembly_instructions = []
        self.variable_map = {}
        self.size_to_allocate = 0
        self.symbol_table = symbol_table
        

    # See if an argument is numeric
    def isNumeric(self, value):
        try:
            float(value)
            return True
        except (ValueError, TypeError):
            return False
    
    # Format memory address with proper signs
    def format_memory_address(self, variable):
        offset = self.variable_map[variable]
        if offset >= 0:
            return f"[rbp+{offset}]"
        else:
            return f"[rbp{offset}]"  

    # Map all the variables in order to allocate space on stack
    def mapVariables(self, instructions, function_name):
        self.variable_map = {}
        offset = 0
        variables_seen = set()
        in_target_function = False

        # Find instructions belonging to the target function
        for instr in instructions:
            
            if instr.label == function_name:
                in_target_function = True
                continue
            
            
            if instr.label and not instr.label.startswith('%') and instr.label != function_name and in_target_function:
                break
            
            
            if in_target_function:
                
                if instr.result and not self.isNumeric(instr.result):
                    variables_seen.add(instr.result)
                if instr.arg1 and not self.isNumeric(instr.arg1):
                    variables_seen.add(instr.arg1)
                if instr.arg2 and not self.isNumeric(instr.arg2):
                    variables_seen.add(instr.arg2)

        # Map function parameters at positive offsets 
        function_params = self.symbol_table.get_function_params(function_name)
        param_names = set()
        param_offset = 16  
        if function_params is not None:
            for params in function_params:
                self.variable_map[params.name] = param_offset
                param_names.add(params.name)  
                param_offset += 8  

        # Map local variables at negative offsets
        for var in variables_seen:
            if var not in param_names:  
                offset += 4
                self.variable_map[var] = -offset
                
        self.size_to_allocate = ((offset + 15) // 16) * 16
        return self.variable_map

    def addInstruction(self, operation=None, destination=None, source=None, label=None):
        instr = AssemblyInstruction(operation, destination, source, label)
        self.assembly_instructions.append(instr)

    def assemble(self, instructions):
        in_function = False
        
        for i, instr in enumerate(instructions):
            
            # Set up stack frame on function lables otherewise just add label
            if instr.label is not None and not instr.label.startswith('%'):

                # Add epilogue for previous function
                if i > 0 and in_function:
                    self.addInstruction("mov", "rsp", "rbp")
                    self.addInstruction("pop", "rbp")
                    self.addInstruction("ret")
                
                # Start new function
                self.addInstruction(label=instr.label)
                self.mapVariables(instructions, instr.label)
                self.addInstruction("push", "rbp")
                self.addInstruction("mov",  "rbp", "rsp")
                if self.size_to_allocate > 0:
                    self.addInstruction("sub", "rsp", str(self.size_to_allocate))
                in_function = True
            elif instr.label:
                self.addInstruction(label=instr.label)

            # Translate TAC setting to assembly
            if instr.operator == '=':
                destination = self.format_memory_address(instr.result)
                if self.isNumeric(instr.arg1):
                    self.addInstruction("mov", destination, str(instr.arg1))
                else:
                    source = self.format_memory_address(instr.arg1)
                    self.addInstruction("mov", "rax", source)
                    self.addInstruction("mov", destination, "rax")

            # Translate TAC arithmatic operations(not division) to assembly
            elif instr.operator in ('+', '-', '*', '<', '>', '==', '!='):
                destination = self.format_memory_address(instr.result)

                if self.isNumeric(instr.arg1):
                    self.addInstruction("mov", "rax", str(instr.arg1))
                else:
                    source1 = self.format_memory_address(instr.arg1)
                    self.addInstruction("mov", "rax", source1)
                
                if self.isNumeric(instr.arg2):
                    source2 = str(instr.arg2)
                else:
                    source2 = self.format_memory_address(instr.arg2)


                if instr.operator == '+':
                    self.addInstruction("add", "rax", source2)
                elif instr.operator == '-':
                    self.addInstruction("sub", "rax", source2)
                elif instr.operator == '*':
                    self.addInstruction("imul", "rax", source2)
                elif instr.operator == '<':
                    self.addInstruction("cmp", "rax", source2)
                    self.addInstruction("setl", "al")
                    self.addInstruction("movzx", "rax", "al")
                elif instr.operator == '>':
                    self.addInstruction("cmp", "rax", source2)
                    self.addInstruction("setg", "al")
                    self.addInstruction("movzx", "rax", "al")
                elif instr.operator == '==':
                    self.addInstruction("cmp", "rax", source2)
                    self.addInstruction("sete", "al")
                    self.addInstruction("movzx", "rax", "al")
                elif instr.operator == '!=':
                    self.addInstruction("cmp", "rax", source2)
                    self.addInstruction("setne", "al")
                    self.addInstruction("movzx", "rax", "al")

                self.addInstruction("mov", destination, "rax")

            # Translate TAC division to assembly
            elif instr.operator == '/':
                destination = self.format_memory_address(instr.result)

                if self.isNumeric(instr.arg1):
                    self.addInstruction("mov", "rax", str(instr.arg1))
                else:
                    source1 = self.format_memory_address(instr.arg1)
                    self.addInstruction("mov", "rax", source1)

                self.addInstruction("cdq")

                if self.isNumeric(instr.arg2):
                    source2 = str(instr.arg2)
                    self.addInstruction("mov", "rcx", source2)
                    self.addInstruction("idiv", "rcx")
                else:
                    source2 = self.format_memory_address(instr.arg2)
                    self.addInstruction("idiv", source2)

                self.addInstruction("mov", destination, "rax")
            
            # Translate TAC return to assembly
            elif instr.operator == 'return':
                if instr.arg1:
                    if self.isNumeric(instr.arg1):
                        self.addInstruction("mov", "rax", str(instr.arg1))
                    else:
                        source = self.format_memory_address(instr.arg1)
                        self.addInstruction("mov", "rax", source)

            # Translate TAC if to assembly
            elif instr.operator == 'if':
                if self.isNumeric(instr.arg1):
                    self.addInstruction("mov", "rax", str(instr.arg1))
                else:
                    source = self.format_memory_address(instr.arg1)
                    self.addInstruction("mov", "rax", source)

                self.addInstruction("cmp", "rax", "0")
                self.addInstruction("jne", instr.arg2)      
                self.addInstruction("jmp", instr.result)

            # Translate TAC goto to assembly
            elif instr.operator == 'goto':
                self.addInstruction("jmp", instr.result)

            # Translate TAC function call to assembly
            elif instr.function_call:
                # Handle Parameters
                number_of_params = 0
                if instr.arg2:
                    params = instr.arg2.split(',')
                    for param in reversed(params):
                        number_of_params += 1
                        if self.isNumeric(param):
                            self.addInstruction("mov", "rax", str(param))
                        else:
                            source = self.format_memory_address(param)
                            self.addInstruction("mov", "rax", source)
                        self.addInstruction("push", "rax")

                # Call function
                self.addInstruction("call", instr.arg1)

                destination = self.format_memory_address(instr.result)
                self.addInstruction("mov", destination, "rax")

                # Clean up parameters from stack (
                if number_of_params > 0:
                    self.addInstruction("add", "rsp", str(number_of_params * 8))

                    

            
        # Add final epilogue
        if in_function:
            self.addInstruction("mov", "rsp", "rbp")
            self.addInstruction("pop", "rbp")
            self.addInstruction("ret")

        return self.assembly_instructions