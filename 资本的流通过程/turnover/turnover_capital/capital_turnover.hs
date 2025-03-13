capital_fixed_num = 80000
capital_fixed_time = 10
capital_circulating_num = 20000
capital_circulating_time = (1 / 5)

getCapitalTotal capital_fixed_num capital_circulating_num = capital_fixed_num + capital_circulating_num
getCapitalTotalCirculating capital_fixed_num capital_fixed_time capital_circulating_num capital_circulating_time = capital_fixed_num / capital_fixed_time + capital_circulating_num / capital_circulating_time
