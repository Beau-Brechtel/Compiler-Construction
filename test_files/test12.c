// Test file for algebraic simplification optimization
// Tests various algebraic identities and simplifications
int main() {
    int x;
    int y;
    int z;
    int result1;
    int result2;
    int result3;
    int result4;
    int result5;
    int result6;
    int result7;
    int result8;
    
    x = 10;
    y = 5;
    
    // Test 1: Addition with zero (x + 0 = x)
    result1 = x + 0;
    
    // Test 2: Subtraction with zero (x - 0 = x)
    result2 = x - 0;
    
    // Test 3: Multiplication by one (x * 1 = x)
    result3 = x * 1;
    
    // Test 4: Division by one (x / 1 = x)
    result4 = x / 1;
    
    // Test 5: Multiplication by zero (x * 0 = 0)
    result5 = x * 0;
    
    // Test 6: Zero subtraction (0 - x = -x, but may not optimize)
    result6 = 0 - x;
    
    // Test 7: Complex expression with identities
    result7 = (x * 1) + (y * 0) + (z - 0);
    
    // Test 8: Nested identities
    result8 = ((x + 0) * 1) / 1;
    
    return result1 + result2 + result3 + result4 + result5 + result6 + result7 + result8;
}