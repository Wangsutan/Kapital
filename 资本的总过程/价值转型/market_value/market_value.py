def calc_market_value(good_quantities, good_values):
    weighted_values_sum = sum(q * v for q, v in zip(good_quantities, good_values))
    good_quantity_total = sum(good_quantities)
    market_value = weighted_values_sum / good_quantity_total

    return market_value


if __name__ == "__main__":
    good_quantities = [100, 150, 200, 80, 120]
    good_values = [10, 15, 5, 20, 25]

    market_value = calc_market_value(good_quantities, good_values)
    print(f"Market Value: {market_value:.2f}")
