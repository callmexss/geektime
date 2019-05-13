#include <stdio.h>
#include <time.h>
#include <stdlib.h>


int add(int a, int b)
{
    return a + b;
}

int main(int argc, const char *argv[])
{
    srand(time(NULL));
    int x = rand() % 5;
    int y = rand() % 10;
    int u = add(x, y);
    printf("u = %d\n", u);
    return 0;
}
