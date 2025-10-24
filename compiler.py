import sys
import os
import argparse
import lexer
import parser
import TAC
import AST
import SymbolTable
from Errors import LexerError
from Errors import ParsingError
import constantFoldingOptimization
import tempVariableRemoverOptimization
import algebraicSimplificationOptimization
import candcPropagation
import easyDeadCodeElimination as eas

# Sets up and runs the lexer
# input: source code as string
def run_lexer(source_code):
    
    # Tries to run lexer
    try:
        
        # Initialize and run lexer
        # Returns list of token objects
        my_lexer = lexer.Lexer()
        tokens = my_lexer.tokenize(source_code)
        
        return tokens
    
    # Handle lexer errors 
    except LexerError as e:
        print(e)
        return None
    
    # Handle other errors
    except Exception as e:
        print(f"Error during lexical analysis: {e}")
        return None

# Set up and run the parser
# input: list of tokens
def run_parser(tokens):

    try:

        # Initialize and run parser
        # Returns AST 
        my_parser = parser.Parser()
        AST, my_symbol_table = my_parser.parse(tokens)

        return AST, my_symbol_table

    # Handle parsing errors
    except ParsingError as e:
        print(e)
        return None

    # Handle other errors
    except Exception as e:
        print(f"Error during parsing: {e}")
        return None

# Main function to handle command-line arguments and run all compiler parts
# To run compiler: python3 compiler.py [options] <input_file>
def main():

    # Command-line arguments for actually running the compiler
    arg_parser = argparse.ArgumentParser(description='Compiler for Beau\'s C language')
    arg_parser.add_argument('input_file', help='Input source code file')
    arg_parser.add_argument('-l', '--lexer', action='store_true', help='Print lexer output tokens')
    arg_parser.add_argument('-p', '--parser', action='store_true', help='Print parser output AST and symbol table')
    arg_parser.add_argument('-t', '--tac', action='store_true', help='Print TAC output')
    arg_parser.add_argument('-o1', '--opt1', action='store_true', help='Enable optimization 1')
    arg_parser.add_argument('-o2', '--opt2', action='store_true', help='Enable optimization 2')
    arg_parser.add_argument('-c', '--candc', action='store_true', help='Enable constant and copy propagation optimization')
    arg_parser.add_argument('-a', '--algebraic', action='store_true', help='Enable algebraic simplification optimization')
    arg_parser.add_argument('-b', '--basicblocks', action='store_true', help='Print basic blocks generated from TAC')
    args = arg_parser.parse_args()
    
    # See if input file exists
    if not os.path.exists(args.input_file):
        print(f"Error: Input file '{args.input_file}' not found")
        return

    # Read source code
    with open(args.input_file, 'r') as f:
        source_code = f.read()

    # Run lexer
    tokens = run_lexer(source_code)
    if tokens == None:
        sys.exit(1)
    if args.lexer:
        print(f"Running lexer on: {args.input_file}")
        print("Tokens:")
        for token in tokens:
            print(token)
        print()



    # Run parser
    parser_result = run_parser(tokens)
    if parser_result == None:
        sys.exit(1)
    AST, my_symbol_table = parser_result
    if args.parser:
        print("Running parser on output tokens")
        print("AST:")
        AST.print_tree()#
        print()
        print("Symbol Table:")
        print()
        my_symbol_table.print_table()
        print()

    # Run TAC generation
    Three_Address_Code = TAC.TAC(my_symbol_table)
    Three_Address_Code.generate_TAC(AST)
    if args.tac:
        print("Three Address Code (TAC):")
        for instr in Three_Address_Code.instructions:
            print(instr)
        print()

    # Run optimizations if enabled
    if args.opt1:
        print("Running optimization 1 on TAC")
        CF = constantFoldingOptimization.ConstantFoldingOptimization(Three_Address_Code.instructions)
        optimized_instructions = CF.optimize()
        tVR = tempVariableRemoverOptimization.tempVarRemover(optimized_instructions)
        optimized_instructions = tVR.optimize()
        print("Three Address Code (TAC):")
        for instr in optimized_instructions:
            print(instr)
        print()

    if args.opt2:
        print("Running optimization 2 on TAC")
        optimized_instructions = Three_Address_Code.instructions
        tVR = tempVariableRemoverOptimization.tempVarRemover(optimized_instructions)
        optimized_instructions = tVR.optimize()  
        while True:
            previous_tac = [str(instr) for instr in optimized_instructions]
            
            ASO = algebraicSimplificationOptimization.AlgebraicSimplificationOptimization(optimized_instructions)
            optimized_instructions = ASO.optimize()
            CF = constantFoldingOptimization.ConstantFoldingOptimization(optimized_instructions)
            optimized_instructions = CF.optimize()
            CP = candcPropagation.CandCPropagation(optimized_instructions)
            optimized_instructions = CP.optimize()
            EDC = eas.EasyDeadCodeElimination(optimized_instructions)
            optimized_instructions = EDC.optimize()

            # Break if no changes were made
            current_tac = [str(instr) for instr in optimized_instructions]
            if current_tac == previous_tac:
                break
        

              
        print("Three Address Code (TAC):")
        for instr in optimized_instructions:
            print(instr)
        print()

    if args.candc:
        print("Running constant and copy propagation optimization on TAC")
        CP = candcPropagation.CandCPropagation(Three_Address_Code.instructions)
        optimized_instructions = CP.optimize()
        print("Three Address Code (TAC):")
        for instr in optimized_instructions:
            print(instr)
        print()

    if args.algebraic:
        print("Running algebraic simplification optimization on TAC")
        ASO = algebraicSimplificationOptimization.AlgebraicSimplificationOptimization(Three_Address_Code.instructions)
        optimized_instructions = ASO.optimize()
        print("Three Address Code (TAC):")
        for instr in optimized_instructions:
            print(instr)
        print()


if __name__ == "__main__":
    main()