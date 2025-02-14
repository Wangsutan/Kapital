#include <stdio.h>
#include <stdbool.h>

typedef struct Soil {
    char type;
    double capitalAdvanced;
    double productNum;
    double productValue;
    double profitNum;
    double profitValue;
    double rentNum;
    double rentValue;
} SOIL;

bool ifUseSoil(double productMarketPrice, double profitRateNecessary, SOIL soilType);
double getProductPriceNecessary(double profitRateNecessary, double capitalAdvanced, double productNum);

int main(void) {
    double wheatMarketPrice = 60.00;
    double wheatPricePerQuarter = wheatMarketPrice;
    double capitalAdvancedGeneral = 50.00;

    SOIL soilA = {
        .type = 'A',
        .capitalAdvanced = capitalAdvancedGeneral,
        .productNum = 1.00,
    };

    SOIL soilB = {
        .type = 'B',
        .capitalAdvanced = capitalAdvancedGeneral,
        .productNum = 2.00,
    };

    double profitValueOrig = wheatMarketPrice * soilA.productNum - soilA.capitalAdvanced;

    soilB.productValue = soilB.productNum * wheatPricePerQuarter;
    double profitRate = soilB.productValue / soilB.capitalAdvanced - 1;
    printf("profitRate: %lf\n", profitRate);

    soilB.profitValue = soilB.productNum * wheatPricePerQuarter - soilB.capitalAdvanced;
    printf("soilB.profitValue: %lf\n", soilB.profitValue);

    soilB.profitNum = soilB.profitValue / wheatPricePerQuarter;
    printf("soilB.profitNum: %lf\n", soilB.profitNum);

    soilB.rentValue = soilB.profitValue - profitValueOrig;
    printf("soilB.rentValue: %lf\n", soilB.rentValue);

    soilB.rentNum = soilB.rentValue / wheatPricePerQuarter;
    printf("soilB.rentNum: %lf\n", soilB.rentNum);

    double profitRateNecessary = 0.2000;

    double wheatPricePerQuarterNecessaryOfTypeA = getProductPriceNecessary(profitRateNecessary, soilA.capitalAdvanced, soilA.productNum);
    printf("wheatPricePerQuarterNecessaryOfTypeA: %lf\n", wheatPricePerQuarterNecessaryOfTypeA);

    double wheatPricePerQuarterNecessaryOfTypeB = getProductPriceNecessary(profitRateNecessary, soilB.capitalAdvanced, soilB.productNum);
    printf("wheatPricePerQuarterNecessaryOfTypeB: %lf\n", wheatPricePerQuarterNecessaryOfTypeB);

    bool canProduce = ifUseSoil(31.00, profitRateNecessary, soilB);
    if (canProduce) printf("canProduce: true\n"); else printf("canProduce: false\n");

    return 0;
}

bool ifUseSoil(double productMarketPrice, double profitRateNecessary, SOIL soilType) {
    bool canProduce = false;
    printf("Market Price of Production is %lf.\n", productMarketPrice);
    double producepriceNecessary = getProductPriceNecessary(profitRateNecessary, soilType.capitalAdvanced, soilType.productNum);
    if (productMarketPrice >= producepriceNecessary) {
        printf("Type %c of Soil Can Be Used!\n", soilType.type);
        canProduce = true;
    } else {
        printf("Type %c of Soil Cannot Be Used!\n", soilType.type);
        canProduce = false;
    }
    return canProduce;
}

double getProductPriceNecessary(double profitRateNecessary, double capitalAdvanced, double productNum) {
    double priceNecessary = (1 + profitRateNecessary) * capitalAdvanced / productNum;
    return priceNecessary;
}
