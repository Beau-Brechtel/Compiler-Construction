import sys
import os

# Import compiler components
try:
    from lexer import Lexer
except ImportError:
    print("Warning: Lexer not found or not properly implemented")
    Lexer = None


def run_lexer(input_file, output_file):
    """
    Args:
        input_file: Path to the source code file
        output_file: Optional path for token output
    """

    # Check if Lexer is available
    if not Lexer:
        print("Error: Lexer not available")
        return False
    
    # Tries to read input file and run lexer
    try:
        # Check if input file exists
        if not os.path.exists(input_file):
            print(f"Error: Input file '{input_file}' not found")
            return False
        
        # Read source code
        with open(input_file, 'r') as f:
            source_code = f.read()
        
        # Initialize and run lexer
        lexer = Lexer()
        tokens = lexer.tokenize(source_code)
        
        # Output tokens
        if output_file:
            with open(output_file, 'w') as f:
                for token in tokens:
                    f.write(f"{token}\n")
            print(f"Tokens written to: {output_file}")
        else:
            print("Tokens:")
            for token in tokens:
                print(token)
        
        return True
    
    except Exception as e:
        print(f"Error during lexical analysis: {e}")
        return False


def main():
    """
    Entry point for the compiler.
    """
    print("=== Compiler Toolkit ===")
    print("Available commands:")
    print("  1 - Run Lexer (tokenize source code)")
    print("  2 - Run Parser (coming next)")
    print("  q - Quit")
    
    while True:
        command = input("\nEnter command: ").strip().lower()

        # End program
        if command == 'q' or command == 'quit':
            print("Goodbye!")
            sys.exit(0)
            
        # Run lexer
        if command == '1':
            # Get input file from user
            while True:
                input_file = input("Enter the path to the source code file: ").strip()
                
                if not input_file:
                    print("Please enter a file path.")
                    continue
                    
                if not os.path.exists(input_file):
                    print(f"Error: File '{input_file}' not found. Please try again.")
                    continue
                    
                break
            
            # Ask if user wants to save output to file
            save_to_file = input("Save tokens to file? (y/n): ").strip().lower()
            output_file = None
            
            if save_to_file in ['y', 'yes']:
                output_file = input("Enter output file path (or press Enter for 'LexerOutput.txt'): ").strip()
                if not output_file:
                    output_file = "LexerOutput.txt"

            # Run lexer
            success = run_lexer(input_file, output_file)
            
            if success:
                print("\nLexical analysis completed successfully!")
            else:
                print("\nLexical analysis failed.")
            
            continue
        
        elif command in ['2']:
            print("This feature is not yet implemented.")
            continue
        
        else:
            print("Not a valid command. Please try again.")
            continue


if __name__ == "__main__":
    main()