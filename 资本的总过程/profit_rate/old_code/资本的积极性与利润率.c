#include <stdio.h>

int main(void)
{
    double profit_rate_margin[] = {0.05, 0.10, 0.20, 0.50, 1.00, 3.00};
    
    double real_profit_rate;
    printf("请输入实际的利润率（单位%，输入q退出）：\n");
    while (scanf("%lf", &real_profit_rate))
    {
        printf("如果有%.2lf%%的利润率，", real_profit_rate);

        if (real_profit_rate < profit_rate_margin[0] * 100)
            printf("资本就没有积极性。\n");
        else if (real_profit_rate < profit_rate_margin[1] * 100)
            printf("资本就胆大起来。\n");
        else if (real_profit_rate < profit_rate_margin[2] * 100)
            printf("资本就保证到处被使用。\n");
        else if (real_profit_rate < profit_rate_margin[3] * 100)
            printf("资本就活跃起来。\n");
        else if (real_profit_rate < profit_rate_margin[4] * 100)
            printf("资本就铤而走险。\n");
        else if (real_profit_rate < profit_rate_margin[5] * 100)
            printf("资本就敢践踏一切人间法律。\n");
        else
            printf("资本就敢犯任何罪行，甚至冒绞首的危险。\n");
        printf("请输入实际的利润率（单位%，输入q退出）：\n");
    }
    return 0;
}
