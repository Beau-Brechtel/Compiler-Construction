// Test file: Type mismatch - comparing different types
int main() {
    int age;
    float height;
    char initial;
    
    age = 25;
    height = 5.8;
    initial = 'J';
    
    if (age == height) {    // Error: cannot compare int and float
        return 1;
    }
    
    if (initial > age) {    // Error: cannot compare char and int
        return 2;
    }
    
    return 0;
}