use std::env;
use std::f32::consts::E;
use std::process;

#[derive(Debug)]

struct Soil {
    name: String,
    area_sum: f32,
    area_used: f32,
    investment_sum: f32,
    investment_actual: f32,
    product_num_sum: f32,
    product_num_actual: f32,
    product_value_actual: f32,
    product_num_per_area: f32,
    product_num_per_investment_per_area: f32,
    rent_abs_per_area: f32,
    super_profit: f32,
}

impl Soil {
    pub fn new(
        name: String,
        area_sum: f32,
        investment_sum: f32,
        product_num_sum: f32,
        rent_abs_per_area: f32,
    ) -> Self {
        Soil {
            name,
            area_sum,
            area_used: 0.0,
            investment_sum,
            investment_actual: 0.0,
            product_num_sum,
            product_num_actual: 0.0,
            product_value_actual: 0.0,
            product_num_per_area: product_num_sum / area_sum,
            product_num_per_investment_per_area: product_num_sum / investment_sum / area_sum,
            rent_abs_per_area: rent_abs_per_area,
            super_profit: 0.0,
        }
    }
}

fn product_force(x: f32, arr: &mut [f32; 5]) -> f32 {
    /*
    - `base`为底数。
    - `left_right_translate`为左右平移量，缩写为`lr`。
    - `up_down_translate`为上下平移量，缩写为`ud`。
    - `abscissa_flexible`为横坐标伸缩量，缩写为`af`。
    - `ordinate_flexible`为纵坐标伸缩量，缩写为`of`。
    */
    let base: f32 = arr[0];
    let lr: f32 = arr[1];
    let ud: f32 = arr[2];
    let af: f32 = arr[3];
    let of: f32 = arr[4];

    if !(base > 1.0
        && af > 0.0
        && of > 0.0
        && (x >= (1.0 + lr) / af)
        && (x > (base.powf(-1.0 * ud / of) + lr) / af))
    {
        println!("Do not satisfy the function of product force.\nExit!");
        process::exit(1);
    } else {
        return of * (af * x - lr).log(base) + ud;
    }
}

fn get_min_soil(soils: &mut [Soil], product_demand: f32) -> (usize, f32, f32) {
    let mut i: usize = soils.len() - 1;
    let mut product_supply_possible: f32 = 0.0;
    let mut supply_rate_of_demand: f32;
    loop {
        soils[i].area_used = soils[i].area_sum;

        product_supply_possible += soils[i].product_num_sum;
        supply_rate_of_demand = product_supply_possible / product_demand;

        if !(i > 0 && product_supply_possible < product_demand) {
            return (i, product_supply_possible, supply_rate_of_demand);
        }

        i -= 1;
    }
}

fn get_product_price(
    soil_rent_abs: f32,
    soil_investment: f32,
    soil_product_num: f32,
    profit_rate: f32,
    supply_rate_of_demand: f32,
) -> f32 {
    println!(
        "soil_rent_abs: {}\nsoil_investment: {}\nsoil_product_num: {}\nprofit_rate: {}\nsupply_rate_of_demand: {}",
        soil_rent_abs, soil_investment, soil_product_num, profit_rate, supply_rate_of_demand
    );
    let product_price: f32 = (soil_investment + soil_investment * profit_rate + soil_rent_abs)
        / soil_product_num
        / supply_rate_of_demand;

    return product_price;
}

fn main() {
    println!("General Program of Differential Rent!");

    // get 3 parameters from console
    let args: Vec<String> = env::args().collect();

    let input_string = &args[1];
    let profit_rate: f32 = match input_string.trim().parse() {
        Ok(profit_rate) => profit_rate,
        Err(_) => {
            println!("Not right data.");
            return;
        }
    };

    let input_string = &args[2];
    let product_demand: f32 = match input_string.trim().parse() {
        Ok(product_demand) => product_demand,
        Err(_) => {
            println!("Not right data.");
            return;
        }
    };

    let input_string = &args[3];
    let if_can_supply_demand_equilibrium: bool = match input_string.trim().parse() {
        Ok(if_can_supply_demand_equilibrium) => if_can_supply_demand_equilibrium,
        Err(_) => {
            println!("Not right data.");
            return;
        }
    };

    // initialize list of soils
    let mut product_pmt_a: [f32; 5] = [E, 3.0, 0.0, 1.0, 1.0];
    let mut product_pmt_b: [f32; 5] = [E, 0.0, 1.0, 1.0, 1.0];
    let mut product_pmt_c: [f32; 5] = [E, 0.0, 1.0, 2.0, 1.0];
    let mut product_pmt_d: [f32; 5] = [E, 0.0, 1.0, 2.0, 2.0];

    let mut soils = vec![
        Soil::new(
            "soil_A".to_string(),
            4.0,
            20.0,
            4.0 * product_force(20.0 / 4.0, &mut product_pmt_a),
            1.0,
        ),
        Soil::new(
            "soil_B".to_string(),
            4.0,
            18.0,
            4.0 * product_force(18.0 / 4.0, &mut product_pmt_b),
            1.0,
        ),
        Soil::new(
            "soil_C".to_string(),
            2.0,
            10.0,
            2.0 * product_force(10.0 / 2.0, &mut product_pmt_c),
            1.0,
        ),
        Soil::new(
            "soil_D".to_string(),
            2.0,
            20.0,
            2.0 * product_force(20.0 / 2.0, &mut product_pmt_d),
            1.0,
        ),
    ];

    soils.sort_by(|a, b| {
        a.product_num_per_investment_per_area
            .partial_cmp(&b.product_num_per_investment_per_area)
            .unwrap()
    });

    println!("\nList of Types of Soils:");
    for i in 0..soils.len() {
        println!("{}", soils[i].name);
    }

    // get mininum soil
    let ptr_min: usize;
    let product_supply_possible: f32;
    let mut supply_rate_of_demand: f32;

    (ptr_min, product_supply_possible, supply_rate_of_demand) =
        get_min_soil(&mut soils, product_demand);

    println!("\nmininum soil: {}", soils[ptr_min].name);
    println!("product_supply_possible: {:.2}", product_supply_possible);
    println!("product_demand: {:.2}", product_demand);
    println!(
        "supply_rate_of_demand: {:.2}%",
        supply_rate_of_demand * 100.0
    );

    // ensure the supply demand rate
    println!("\nJudge supply_rate_of_demand and if_can_supply_demand_equilibrium:");
    if supply_rate_of_demand > 1.0 {
        println!("supply > demand");
        if if_can_supply_demand_equilibrium {
            println!("Keep them balance by limit the used areas of soils!\n");
            supply_rate_of_demand = 1.0;
        } else {
            println!("May reduce the price!\nBut we keep them balance\nto simplify the economic relationship.\nAnd it is really reasonable to do so.\n");
            supply_rate_of_demand = 1.0;
        }
    } else if supply_rate_of_demand < 1.0 {
        println!("supply < demand");
        if if_can_supply_demand_equilibrium {
            println!("Keep them balance by import and so on!\n");
            supply_rate_of_demand = 1.0;
        } else {
            println!("Raise the price!\n");
        }
    } else if supply_rate_of_demand == 1.0 {
        println!("Keep them balance in default!\n");
    }

    // get the price of product
    let product_price: f32 = get_product_price(
        soils[ptr_min].rent_abs_per_area * soils[ptr_min].area_sum,
        soils[ptr_min].investment_sum,
        soils[ptr_min].product_num_sum,
        profit_rate,
        supply_rate_of_demand,
    );
    println!("Actual price: {:.2}\n", product_price);

    // get the imagine equilibrium price
    let product_price_equilibrium: f32 = get_product_price(
        soils[ptr_min].rent_abs_per_area * soils[ptr_min].area_sum,
        soils[ptr_min].investment_sum,
        soils[ptr_min].product_num_sum,
        profit_rate,
        1.0,
    );
    println!(
        "Imaginary equilibrium price: {:.2}\n",
        product_price_equilibrium
    );

    // get the actual used area of mininum soil
    let supply_overflow_min_soil: f32 = if product_supply_possible - product_demand > 0.0 {
        product_supply_possible - product_demand
    } else {
        0.0
    };

    let product_supply: f32 = product_supply_possible - supply_overflow_min_soil;
    println!("product_supply: {:.2}", product_supply);

    let area_overflow_min_soil: f32 =
        supply_overflow_min_soil / soils[ptr_min].product_num_per_area;

    soils[ptr_min].area_used -= area_overflow_min_soil;
    println!("used area of min soil: {:.2}", soils[ptr_min].area_used);

    // calc datas of soils
    let mut product_value_total: f32 = 0.0;
    let mut super_profit_total: f32 = 0.0;

    for i in 0..soils.len() {
        soils[i].investment_actual =
            soils[i].investment_sum * (soils[i].area_used / soils[i].area_sum);

        soils[i].product_num_actual = soils[i].area_used * soils[i].product_num_per_area;
        soils[i].product_value_actual = product_price * soils[i].product_num_actual;
        product_value_total += soils[i].product_value_actual;

        let product_num_as_soil_min = soils[i].area_used * soils[ptr_min].product_num_per_area;
        let product_value_as_soil_min = product_num_as_soil_min * product_price_equilibrium;

        soils[i].super_profit = soils[i].product_value_actual - product_value_as_soil_min;
        super_profit_total += soils[i].super_profit;
    }

    for soil in &soils {
        println!("{:#?}", soil);
    }

    println!("\nproduct_value_total: {:.2}", product_value_total);
    println!("super_profit_total: {:.2}", super_profit_total);

    let mut rent_abs_total: f32 = 0.0;
    for i in 0..soils.len() {
        rent_abs_total += soils[i].rent_abs_per_area * soils[i].area_used;
    }

    // transform super profit to rent
    let transform_rate_from_super_profit_to_rent: f32 = 1.0;
    let rent_diff_possible = super_profit_total * transform_rate_from_super_profit_to_rent;
    let rent_diff_total: f32 = if rent_diff_possible > 0.0 {
        rent_diff_possible
    } else {
        0.0
    };

    let rent_total: f32 = rent_abs_total + rent_diff_total;
    println!("\nrent_total: {:.2}\n", rent_total);

    let mut area_used_total: f32 = 0.0;
    for i in 0..soils.len() {
        area_used_total += soils[i].area_used;
    }
    println!("area_used_total: {:.2}", area_used_total);

    let rent_per_area_avg: f32 = rent_total / area_used_total;
    println!("rent_per_area_avg: {:.2}", rent_per_area_avg);

    let mut investment_total: f32 = 0.0;
    for i in 0..soils.len() {
        investment_total += soils[i].investment_actual;
    }
    println!("\ninvestment_total: {:.2}", investment_total);

    let rent_per_capital_avg: f32 = rent_total / investment_total;
    println!(
        "rent_per_capital_avg: {:.2}%",
        rent_per_capital_avg * 100.00
    );
}
