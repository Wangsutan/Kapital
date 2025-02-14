#include <stdio.h>

double getCapitalImage(double income_annual, double interest_rate_annual);

int main(void) {
    double interest_rate_annual = 0.0500;
    printf("interest_rate_annual: %lf\n", interest_rate_annual);

    double rent_annual;
    printf("Input annual rent: ");
    scanf("%lf", &rent_annual);

    double land_value = getCapitalImage(rent_annual, interest_rate_annual);
    printf("value of land: %lf\n", land_value);

    double price_show_by_earnings_annual1 = land_value / rent_annual;
    printf("price_show_by_earnings_annual1: %lf\n", price_show_by_earnings_annual1);

    /*
     * price_show_by_earnings_annual = land_value / rent_annual
     * = capital_image / rent_annual
     * = (rent_annual / interest_rate_annual) / rent_annual
     * = 1 / interest_rate_annual
     * 因此马克思说，「这不过是地租资本化的另一种表现。」
     */

    double price_show_by_earnings_annual2 = 1 / interest_rate_annual;
    printf("price_show_by_earnings_annual2: %lf\n", price_show_by_earnings_annual2);

    if (price_show_by_earnings_annual1 == price_show_by_earnings_annual2) {
        printf("Marx is RIGHT on this topic.\n");
    } else {
        printf("Marx is WRONG on this topic.\n");
    }

    return 0;
}

double getCapitalImage(double income_annual, double interest_rate_annual) {
    double capital_image = income_annual / interest_rate_annual;
    return capital_image;
}
