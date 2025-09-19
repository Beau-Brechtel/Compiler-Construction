// Parser, Should cause undeclared error
int main() {
    int x = 5;
    int y = x + undeclared_var;
    return y;
}