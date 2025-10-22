// Test file for constant and copy propagation optimization
// Tests various scenarios of propagating constants and copying variables
int main() {
    int a;
    int b;
    int c;
    int d;
    int e;
    int f;
    int g;
    int h;
    int result1;
    int result2;
    int result3;
    int result4;
    int result5;
    
    // Test 1: Simple constant propagation
    a = 42;
    result1 = a + 8;    // Should become: result1 = 42 + 8 = 50
    
    // Test 2: Simple copy propagation  
    b = a;              // b should get value 42 (copy from a)
    result2 = b * 2;    // Should become: result2 = 42 * 2 = 84
    
    // Test 3: Chain copy propagation
    c = b;              // c should get value 42 (copy from b)
    d = c;              // d should get value 42 (copy from c)  
    e = d;              // e should get value 42 (copy from d)
    result3 = e - 10;   // Should become: result3 = 42 - 10 = 32
    
    // Test 4: Mixed constant and copy propagation
    f = 100;            // Constant
    g = f;              // Copy f's value (100)
    h = g + f;          // Should become: h = 100 + 100 = 200
    result4 = h / 4;    // Should become: result4 = 200 / 4 = 50
    
    // Test 5: Variable reassignment (should stop propagation)
    a = 999;            // a gets new value, old propagation should stop
    result5 = a + 1;    // Should use new value: result5 = 999 + 1 = 1000
    
    // Test 6: Copy after reassignment
    b = a;              // b should now get 999 (new value of a)
    c = b + a;          // Should become: c = 999 + 999 = 1998
    
    return result1 + result2 + result3 + result4 + result5 + c;
}