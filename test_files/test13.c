// Test file for constant propagation optimization
// Tests propagating constant values through variables
int main() {
    int a;
    int b;
    int c;
    int d;
    int x;
    int y;
    int z;
    int result1;
    int result2;
    int result3;
    int result4;
    
    // Test 1: Simple constant propagation
    a = 5;
    b = a;          // b should become 5
    c = b + 3;      // c should become 5 + 3 = 8
    
    // Test 2: Chain of constant propagation
    x = 10;
    y = x;          // y should become 10
    z = y;          // z should become 10
    result1 = z * 2; // result1 should become 10 * 2 = 20
    
    // Test 3: Constant propagation with expressions
    d = 7;
    result2 = d - 3; // result2 should become 7 - 3 = 4
    result3 = d * d; // result3 should become 7 * 7 = 49
    
    // Test 4: Mixed constant and variable usage
    result4 = a + d; // result4 should become 5 + 7 = 12
    
    // Test 5: Variable reassignment (should stop propagation)
    a = 15;         // a is now 15, previous propagation of a=5 should stop
    b = a + 1;      // b should become 15 + 1 = 16 (new value of a)
    
    return result1 + result2 + result3 + result4 + b;
}