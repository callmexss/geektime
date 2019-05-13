#include <stdio.h>


int add(int a, int b)
{
    return a + b;
}

int main(int argc, const char *argv[])
{
    int a = 5;
    int b = 10;
    int u = add(a, b);
    return 0;
}
