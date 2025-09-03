import sys
import os
import argparse

# Import compiler components
try:
    from lexer import Lexer
except ImportError:
    print("Warning: Lexer not found or not properly implemented")
    Lexer = None

def run_lexer(input_file):
    """
    Args:
        input_file: Path to the source code file
    """
    
    # Tries to read input file and run lexer
    try:
        
        # Read source code
        with open(input_file, 'r') as f:
            source_code = f.read()
        
        # Initialize and run lexer
        lexer = Lexer()
        tokens = lexer.tokenize(source_code)
        
        # Output tokens 
        print("Tokens:")
        for token in tokens:
            print(token)
        
        return True
    
    # Might add better errors later
    except Exception as e:
        print(f"Error during lexical analysis: {e}")
        return False

def main():
    """
    To run: python3 compiler.py [options] <input_file>
    """
    parser = argparse.ArgumentParser(description='Compiler for Beau\'s C language')

    # Command-line arguments
    parser.add_argument('input_file', help='Input source code file')
    parser.add_argument('-l', '--lexer', action='store_true', 
                       help='Run lexer and print tokens')
    
    # If no arguments provided show help
    if len(sys.argv) == 1:
        parser.print_help()
        return
    
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