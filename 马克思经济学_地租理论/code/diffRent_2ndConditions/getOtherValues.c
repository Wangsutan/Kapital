#include <stdio.h>

typedef struct Soil {
    char type[8];
    double capitalAdvanced;
    double productNum;
    double productValue;
    double profitNum;
    double profitValue;
    double profitRate;
    double rentNum;
    double rentValue;
    double productPrice;
} SOIL;

void getOtherValues(SOIL* soilType, double productionMarketPrice, double profitValueOrig, double productPriceOld);
void showValues(SOIL* soilType);

int main(void) {
    double capitalAdvancedGeneral = 50.00;
    double wheatMarketPrice = 60.00;
    const double wheatProductPriceOld = wheatMarketPrice;

    SOIL soilA = {
        .type = "A",
        .capitalAdvanced = capitalAdvancedGeneral,
        .productNum = 1.00,
    };

    /*
     * 如果决定市场价格的最低级别土地的小麦产量上升，
     * 那么在单位价值产出、资本投入等因素不变的情况下，
     * 小麦市场价值因这个产量上升而下降。
     * 此时，小麦每夸特的生产价格就等于单位价值产出（不变）除以产量（增加），
     * 因此，这个价格就下跌。
     */

    soilA.productNum = 1.00 + (1.00 / 3.00);
    // printf("soilA.productNum: %.2lf\n", soilA.productNum);
    wheatMarketPrice = wheatMarketPrice / soilA.productNum;
    printf("wheatProductPriceOld: %.2lf\nwheatMarketPrice: %.2lf\n",
           wheatProductPriceOld, wheatMarketPrice);

    SOIL soilA_prime = {
        .type = "A\'",
        .capitalAdvanced = capitalAdvancedGeneral,
        .productNum = 1.00 + (2.00 / 3.00),
    };

    SOIL soilB = {
        .type = "B",
        .capitalAdvanced = capitalAdvancedGeneral,
        .productNum = 2.00,
    };

    SOIL soilB_prime = {
        .type = "B\'",
        .capitalAdvanced = capitalAdvancedGeneral,
        .productNum = 2.00 + (1.00 / 3.00),
    };

    SOIL soilB_double_prime = {
        .type = "B\'\'",
        .capitalAdvanced = capitalAdvancedGeneral,
        .productNum = 2.00 + (2.00 / 3.00),
    };

    SOIL soilC = {
        .type = "C",
        .capitalAdvanced = capitalAdvancedGeneral,
        .productNum = 3.00,
    };

    SOIL soilD = {
        .type = "D",
        .capitalAdvanced = capitalAdvancedGeneral,
        .productNum = 4.00,
    };

    double profitValueOrig = wheatMarketPrice * soilA.productNum - soilA.capitalAdvanced;
    printf("profitValueOrig: %.2lf\n", profitValueOrig);

    getOtherValues(&soilA, wheatMarketPrice, profitValueOrig, wheatProductPriceOld);
    getOtherValues(&soilA_prime, wheatMarketPrice, profitValueOrig, wheatProductPriceOld);
    getOtherValues(&soilB, wheatMarketPrice, profitValueOrig, wheatProductPriceOld);
    getOtherValues(&soilB_prime, wheatMarketPrice, profitValueOrig, wheatProductPriceOld);
    getOtherValues(&soilB_double_prime, wheatMarketPrice, profitValueOrig, wheatProductPriceOld);
    getOtherValues(&soilC, wheatMarketPrice, profitValueOrig, wheatProductPriceOld);
    getOtherValues(&soilD, wheatMarketPrice, profitValueOrig, wheatProductPriceOld);

    printf("type\tcapitalAdvanced\tproductNum\tproductValue\tprofitNum\tprofitValue\tprofitRate\trentNum\trentValue\tproductPrice\n");
    showValues(&soilA);
    showValues(&soilA_prime);
    showValues(&soilB);
    showValues(&soilB_prime);
    showValues(&soilB_double_prime);
    showValues(&soilC);
    showValues(&soilD);

    return 0;
}

void getOtherValues(SOIL* soilType, double productionMarketPrice, double profitValueOrig, double productPriceOld) {
    soilType -> productValue = soilType -> productNum * productionMarketPrice;
    soilType -> profitRate = soilType -> productValue / soilType -> capitalAdvanced - 1;
    soilType -> profitValue = soilType -> productValue - soilType -> capitalAdvanced;
    soilType -> profitNum = soilType -> profitValue / productionMarketPrice;
    soilType -> rentValue = soilType -> profitValue - profitValueOrig;
    soilType -> rentNum = soilType -> rentValue / productionMarketPrice;
    soilType -> productPrice = productPriceOld / soilType -> productNum;
}

void showValues(SOIL* soilType) {
    printf("%s\t%.2lf\t%.2lf\t%.2lf\t%.2lf\t%.2lf\t%.2lf\t%.2lf\t%.2lf\t%.2lf\n",
        soilType ->  type,
        soilType ->  capitalAdvanced,
        soilType ->  productNum,
        soilType ->  productValue,
        soilType ->  profitNum,
        soilType ->  profitValue,
        soilType ->  profitRate,
        soilType ->  rentNum,
        soilType ->  rentValue,
        soilType -> productPrice
    );
}
