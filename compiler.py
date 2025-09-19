import sys
import os
import argparse
import lexer
import parser
import AST
import SymbolTable
from Errors import LexerError
from Errors import ParsingError

# Sets up and runs the lexer
# input: source code as string
def run_lexer(source_code, print_tokens=True):
    
    # Tries to run lexer
    try:
        
        # Initialize and run lexer
        # Returns list of token objects
        my_lexer = lexer.Lexer()
        tokens = my_lexer.tokenize(source_code)

        # Output tokens
        if print_tokens:
            print("Tokens:")
            for token in tokens:
                print(token)
        
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
def run_parser(tokens, print_AST=True):

    try:

        # Initialize and run parser
        # Returns AST 
        my_parser = parser.Parser()
        AST, my_symbol_table = my_parser.parse(tokens)

        if print_AST:
            print("AST:")
            AST.print_tree()
            print()
            my_symbol_table.print_table()

        return AST

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
    arg_parser.add_argument('-l', '--lexer', action='store_true', help='Run lexer and print tokens')
    arg_parser.add_argument('-p', '--parser', action='store_true', help='Run parser (not implemented yet)')
    args = arg_parser.parse_args()
    
    # See if input file exists
    if not os.path.exists(args.input_file):
        print(f"Error: Input file '{args.input_file}' not found")
        return

    # Read source code
    with open(args.input_file, 'r') as f:
        source_code = f.read()

    # Run lexer
    if args.lexer:
        print(f"Running lexer on: {args.input_file}")
        tokens = run_lexer(source_code)
        if tokens == None:
            sys.exit(1)

    # Run parser
    if args.parser:
        tokens = run_lexer(source_code, False)
        if tokens == None:
            sys.exit(1)

        print("Running parser on output tokens")
        AST = run_parser(tokens)
        if AST == None:
            sys.exit(1)


if __name__ == "__main__":
    main()