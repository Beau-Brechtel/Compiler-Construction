from instruction import Instruction
from assemblyInstruction import AssemblyInstruction

class assembler:

    def __init__(self):
        self.assembly_instructions = []
        self.variable_map = {}
        self.size_to_allocate = 0
        

    def isNumeric(self, value):
        try:
            float(value)
            return True
        except (ValueError, TypeError):
            return False

    def mapVariables(self, instructions):
        self.variable_map = {}
        offset = 0

        for instr in instructions:
            if instr.result:
                offset += 4
                self.variable_map[instr.result] = -offset
                
        self.size_to_allocate = ((offset + 15) // 16) * 16
        return self.variable_map

    def addInstruction(self, operation=None, destination=None, source=None, label=None):
        instr = AssemblyInstruction(operation, destination, source, label)
        self.assembly_instructions.append(instr)

    def assemble(self, instructions):
        
        for instr in instructions:
            
            # New function so it has to setup stack frame
            if instr.label and not instr.label.startswith('%'):
                self.addInstruction(label=instr.label)
                self.mapVariables(instructions)
                self.addInstruction("push", "rbp")
                self.addInstruction("mov",  "rbp", "rsp")
                if self.size_to_allocate > 0:
                    self.addInstruction("sub", "rsp", str(self.size_to_allocate))
            elif instr.label:
                self.addInstruction(label=instr.label)

            if instr.operator == '=':
                destination = f"[rbp{self.variable_map[instr.result]}]"
                if self.isNumeric(instr.arg1):
                    self.addInstruction("mov", destination, str(instr.arg1))
                else:
                    source = f"[rbp{self.variable_map[instr.arg1]}]"
                    self.addInstruction("mov", "eax", source)
                    self.addInstruction("mov", destination, "eax")

            elif instr.operator in ('+', '-', '*', '<', '>', '==', '!='):
                destination = f"[rbp{self.variable_map[instr.result]}]"

                if self.isNumeric(instr.arg1):
                    self.addInstruction("mov", "eax", str(instr.arg1))
                else:
                    source1 = f"[rbp{self.variable_map[instr.arg1]}]"
                    self.addInstruction("mov", "eax", source1)
                
                if self.isNumeric(instr.arg2):
                    source2 = str(instr.arg2)
                else:
                    source2 = f"[rbp{self.variable_map[instr.arg2]}]"

                if instr.operator == '+':
                    self.addInstruction("add", "eax", source2)
                elif instr.operator == '-':
                    self.addInstruction("sub", "eax", source2)
                elif instr.operator == '*':
                    self.addInstruction("imul", "eax", source2) 
                elif instr.operator == '<':
                    self.addInstruction("cmp", "eax", source2)
                    self.addInstruction("setl", "al")
                    self.addInstruction("movzx", "eax", "al")
                elif instr.operator == '>':
                    self.addInstruction("cmp", "eax", source2)
                    self.addInstruction("setg", "al")
                    self.addInstruction("movzx", "eax", "al")
                elif instr.operator == '==':
                    self.addInstruction("cmp", "eax", source2)
                    self.addInstruction("sete", "al")
                    self.addInstruction("movzx", "eax", "al")
                elif instr.operator == '!=':
                    self.addInstruction("cmp", "eax", source2)
                    self.addInstruction("setne", "al")
                    self.addInstruction("movzx", "eax", "al")
                
                
                self.addInstruction("mov", destination, "eax")

            elif instr.operator == '/':
                destination = f"[rbp{self.variable_map[instr.result]}]"

                if self.isNumeric(instr.arg1):
                    self.addInstruction("mov", "eax", str(instr.arg1))
                else:
                    source1 = f"[rbp{self.variable_map[instr.arg1]}]"
                    self.addInstruction("mov", "eax", source1)

                self.addInstruction("cdq")

                if self.isNumeric(instr.arg2):
                    source2 = str(instr.arg2)
                    self.addInstruction("mov", "ecx", source2)
                    self.addInstruction("idiv", "ecx")
                else:
                    source2 = f"[rbp{self.variable_map[instr.arg2]}]"
                    self.addInstruction("idiv", source2)

                self.addInstruction("mov", destination, "eax")
            
            elif instr.operator == 'return':
                if instr.arg1:
                    if self.isNumeric(instr.arg1):
                        self.addInstruction("mov", "eax", str(instr.arg1))
                    else:
                        source = f"[rbp{self.variable_map[instr.arg1]}]"
                        self.addInstruction("mov", "eax", source)
            elif instr.operator == 'if':
                if self.isNumeric(instr.arg1):
                    self.addInstruction("mov", "eax", str(instr.arg1))
                else:
                    source = f"[rbp{self.variable_map[instr.arg1]}]"
                    self.addInstruction("mov", "eax", source)

                self.addInstruction("cmp", "eax", "0")
                self.addInstruction("jne", instr.arg2)      
                self.addInstruction("jmp", instr.result)

            elif instr.operator == 'goto':
                self.addInstruction("jmp", instr.result)

            elif instr.function_call:
                pass


            
        self.addInstruction("mov", "rsp", "rbp")
        self.addInstruction("pop", "rbp")
        self.addInstruction("ret")

        return self.assembly_instructions