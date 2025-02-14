#include <stdio.h>

double calc_free_captial(double labour_period, double circulating_period, double flüssiges_Kapital_per_week, int n)
{
    return (circulating_period - labour_period * (n - 1)) * flüssiges_Kapital_per_week;
}

int main(void)
{
    double flüssiges_Kapital_per_week = 100;
    double labour_period = 3.5;
    double circulating_period = 8;

    int n = 1;
    while (calc_free_captial(labour_period, circulating_period, flüssiges_Kapital_per_week, n) >= 0)
    {
        n += 1;
    }
    printf("n = %d\n", n - 1);
    printf("True result: %.2f\n", calc_free_captial(labour_period, circulating_period, flüssiges_Kapital_per_week, n - 1));

    return 0;
}
