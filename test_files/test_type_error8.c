// Test file: Type mismatch - variable declaration with wrong initialization type
int main() {
    int count = 2.8;    // Error: cannot initialize int with float
    char grade = 95;    // Error: cannot initialize char with int
    float score = 'A';  // Error: cannot initialize float with char
    
    return count;
}