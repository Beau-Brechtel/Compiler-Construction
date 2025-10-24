# https://www.geeksforgeeks.org/compiler-design/basic-blocks-in-compiler-design/
# https://www.geeksforgeeks.org/python/networkx-python-software-package-study-complex-networks/
# https://www.geeksforgeeks.org/python/networkx-python-software-package-study-complex-networks/

import instruction
import networkx as nx

class BasicBlockGenerator:
    def __init__(self,):
        self.instructions = []
        self.basic_blocks = {}
        self.label_in_block = {}
        self.instruction_index = 0  
        self.counter = 0
        self.graph = nx.DiGraph()

    def get_next_block_id(self):
        block_id = f'B{self.counter}'
        self.counter += 1
        return block_id

    def generate_basic_blocks(self, instructions):
        self.instructions = instructions
        self.instruction_index = 0
        self.counter = 0
        
        while self.instruction_index < len(self.instructions):
            block_id = self.generate_one_block()
            self.graph.add_node(block_id)
        
        self.build_graph()
        return self.basic_blocks, self.graph
    
    def generate_one_block(self):
            
        block_id = self.get_next_block_id()
        instructions_in_block = []
        
        while self.instruction_index < len(self.instructions):
            current_instr = self.instructions[self.instruction_index]
            
            # Make sure we aren't just looking at the the first instruction(label)
            if current_instr.label is not None and len(instructions_in_block) > 0:
                break

            if current_instr.label is not None:
                    self.label_in_block[current_instr.label] = block_id
                
            instructions_in_block.append(current_instr)
            self.instruction_index += 1
            
            # If this was a branch/jump instruction, end the block
            if current_instr.operator in ["if", "goto"]:
                break
        
        self.basic_blocks[block_id] = instructions_in_block
        return block_id
    
    def build_graph(self):
        
        block_ids = list(self.basic_blocks.keys())
        
        for i, block_id in enumerate(block_ids):
            instructions = self.basic_blocks[block_id]
            if not instructions:
                continue
                
            last_instr = instructions[-1]
            
            if last_instr.operator == "if":

                true_jump = self.label_in_block.get(last_instr.arg2)
                false_jump = self.label_in_block.get(last_instr.result)
                
                if true_jump:
                    self.graph.add_edge(block_id, true_jump, label="true")
                if false_jump:
                    self.graph.add_edge(block_id, false_jump, label="false")
                    
            elif last_instr.operator == "goto":
                target = self.label_in_block.get(last_instr.result)
                if target:
                    self.graph.add_edge(block_id, target, label="goto")
    
    def print_control_flow_graph(self):
        print("\nControl Flow Graph:")
        print("Nodes:", list(self.graph.nodes()))
        print("Edges:", list(self.graph.edges()))
        
        print("\nBasic Blocks:")
        for block_id, instructions in self.basic_blocks.items():
            print(f"{block_id}:")
            for instr in instructions:
                print(f"  {instr}")
