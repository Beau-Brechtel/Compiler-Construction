int add(int a, int b) {
    return a + b;
}


int main() {
    int localVar = 5;
    int result = add(localVar, 7);
    add(3, 4);

    return localVar + 10 + result;
}