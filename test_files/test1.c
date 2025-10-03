int main() {
    int x = 10;
    int y = 20;

    if (x > 5) {
        y = y + 5;
    } else if( x < 5) {
        y = y - 5;
    } else {
        y = y * 2;
    }

    return y;
}
