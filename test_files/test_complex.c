// Simpler test file to test parser grammar
// Tests: basic functions, variables, control structures, expressions

// Global variables
int globalVar = 10;
float pi = 3.14;

// Simple function with parameters
int add(int a, int b) {
    int result = a + b;
    return result;
}

// Function with control structure
int checkValue(int x) {
    if (x > 5) {
        return 1;
    } else {
        return 0;
    }
}

// Function with loop
int countUp(int limit) {
    int count = 0;
    int i = 0;
    
    while (i < limit) {
        count = count + 1;
        i = i + 1;
    }
    
    return count;
}

// Main function
int main() {
    int localVar = 20;
    int sum = add(localVar, globalVar);
    
    if (sum > 25) {
        int result = checkValue(sum);
        return result;
    } else {
        return countUp(5);
    }
}