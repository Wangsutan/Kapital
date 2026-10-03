#include <stdio.h>

/*
 * > 《评论家季刊》说：资本逃避动乱和纷争，它的本性是胆怯的。这是真的，但还不是全部真理。资本害怕没有利润或利润太少，就像自然界害怕真空一样。一旦有适当的利润，资本就胆大起来.如果有10%的利润，它就保证到处被使用；有20%的利润，它就活跃起来；有50%的利润，它就铤而走险；为了100%的利润，它就敢践踏一切人间法律；有300%的利润，它就敢犯任何罪行，甚至冒绞首的危险。如果动乱和纷争能带来利润，它就会鼓励动乱和纷争。走私和贩卖奴隶就是证明。（托·约·邓宁《工联和罢工》1860年伦敦版第35、36页）
 */

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
