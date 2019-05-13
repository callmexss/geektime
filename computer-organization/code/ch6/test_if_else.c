#include <time.h>
#include <stdlib.h>


int main(int argc, const char *argv[])
{
    srand(time(NULL));
    int r = rand() % 2;
    int a = 10;

    if (r == 0)
    {
        a = 1;
    }
    else
    {
        a = 2;
    }
    
    return 0;
}
