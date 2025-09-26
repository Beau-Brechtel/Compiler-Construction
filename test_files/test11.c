int globalVar = 10;
float pi = 3.14;
char letter = 'A';

int add(int a, int b) {
    return a + b;
}


int main() {
    int localVar = 5;
    int result = add(localVar, globalVar);
    add(3, 4);

    return localVar + globalVar;
}