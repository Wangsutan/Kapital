
if product_supply_possible >= product_demand {
    return (i, product_supply_possible, supply_rate_of_demand);
} else if (i == 0) && (product_supply_possible < product_demand) {
    return (i, product_supply_possible, supply_rate_of_demand);
}

if !(i > 0 && product_supply_possible < product_demand) {
    return (i, product_supply_possible, supply_rate_of_demand);
}
