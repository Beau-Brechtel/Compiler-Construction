import sys
import os
import argparse
import lexer

# Sets up and runs the lexer
# input_file: Path to the source code file
def run_lexer(input_file):
    
    # Tries to read input file and run lexer
    try:
        
        # Read source code
        with open(input_file, 'r') as f:
            source_code = f.read()
        
        # Initialize and run lexer
        # Returns list of token objects
        my_lexer = lexer.Lexer()
        tokens = my_lexer.tokenize(source_code)

        # Output tokens
        print("Tokens:")
        for token in tokens:
            print(token)
        
        return True
    
    # Might add better errors later
    except Exception as e:
        print(f"Error during lexical analysis: {e}")
        return False

# Main function to handle command-line arguments and run all compiler parts
# To run compiler: python3 compiler.py [options] <input_file>
def main():

    # Command-line arguments for actually running the compiler
    parser = argparse.ArgumentParser(description='Compiler for Beau\'s C language')
    parser.add_argument('input_file', help='Input source code file')
    parser.add_argument('-l', '--lexer', action='store_true', help='Run lexer and print tokens')
    args = parser.parse_args()
    
    # See if input file exists
    if not os.path.exists(args.input_file):
        print(f"Error: Input file '{args.input_file}' not found")
        return
    
    # Run lexer
    if args.lexer:
        print(f"Running lexer on: {args.input_file}")
        success = run_lexer(args.input_file)
        if not success:
            #maybe better error handling later
            sys.exit(1)


if __name__ == "__main__":
    main()