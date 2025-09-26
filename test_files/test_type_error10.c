// Test file: Type mismatch - complex expression with mixed types
int main() {
    int a;
    int b;
    char c;
    int result;
    
    a = 10;
    b = 3;
    c = 'X';
    
    result = (a * b) + c;  // Error: mixing int, float, and char in expression
    
    return result;
}