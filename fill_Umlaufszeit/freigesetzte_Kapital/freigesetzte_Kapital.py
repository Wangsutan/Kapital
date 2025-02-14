def calc_free_captial(labour_period, circulating_period, n):
    return (circulating_period - labour_period * (n - 1)) * flüssiges_Kapital_per_week


flüssiges_Kapital_per_week = 100
labour_period = 5
circulating_period = 5

n = 1
while calc_free_captial(labour_period, circulating_period, n) >= 0:
    n += 1

print("n =", n - 1)
print("True result:", calc_free_captial(labour_period, circulating_period, n - 1))
