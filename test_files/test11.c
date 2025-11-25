int add(int a, int b, int c, int d, int e, int f, int g) {
    return a + b + f + g;
}


int main() {
    int localVar = 5;
    int result = add(localVar, 7, 8, 9, 10, 11, 12);

    return localVar + 10 + result;
}