use std::env;

#[derive(Debug)]

struct Soil {
    name: String,
    area_sum: f32,
    area_used: f32,
    investment_sum: f32,
    product_num_sum: f32,
    product_num_per_area: f32,
    product_num_per_investment_per_area: f32,
}

impl Soil {
    pub fn new(name: String, area_sum: f32, investment_sum: f32, product_num_sum: f32) -> Self {
        Soil {
            name,
            area_sum,
            area_used: 0.0,
            investment_sum,
            product_num_sum,
            product_num_per_area: product_num_sum / area_sum,
            product_num_per_investment_per_area: product_num_sum / investment_sum / area_sum,
        }
    }
}

fn get_min_soil(soil_list: &mut [Soil], product_demand: f32) -> (usize, f32, f32) {
    let mut i: usize = soil_list.len() - 1;
    let mut product_supply_possible: f32 = 0.0;
    let mut supply_demand_rate: f32;
    loop {
        product_supply_possible += soil_list[i].product_num_sum;
        println!(
            "[{}]\tproduct_supply_possible: {:.2}",
            i, product_supply_possible
        );
        soil_list[i].area_used = soil_list[i].area_sum;
        supply_demand_rate = product_supply_possible / product_demand;

        if product_supply_possible >= product_demand {
            return (i, product_supply_possible, supply_demand_rate);
        } else if (i == 0) && (product_supply_possible < product_demand) {
            return (i, product_supply_possible, supply_demand_rate);
        }
        i -= 1;
    }
}

fn get_product_price(
    soil_investment: f32,
    soil_product_num: f32,
    profit_rate: f32,
    supply_demand_rate: f32,
) -> f32 {
    let product_price: f32 =
        (1.00 + profit_rate) * soil_investment / soil_product_num / supply_demand_rate;
    return product_price;
}

fn main() {
    println!("General Program of Differential Rent!\n");

    let profit_rate: f32 = 0.20; // very basic parameter

    // get 2 parameters from console
    let args: Vec<String> = env::args().collect();

    let input_string = &args[1];
    let product_demand: f32 = match input_string.trim().parse() {
        Ok(product_demand) => product_demand,
        Err(_) => {
            println!("Not right data.");
            return;
        }
    };
    println!("product_demand: {:.2}\n", product_demand);

    let input_string = &args[2];
    let if_need_supply_demand_balance: bool = match input_string.trim().parse() {
        Ok(if_need_supply_demand_balance) => if_need_supply_demand_balance,
        Err(_) => {
            println!("Not right data.");
            return;
        }
    };

    // initialize list of soils
    let mut soil_list = vec![
        Soil::new("soil_A".to_string(), 4.0, 200.0, 4.0),
        Soil::new("soil_B".to_string(), 4.0, 200.0, 8.0),
        Soil::new("soil_C".to_string(), 2.0, 100.0, 6.0),
        Soil::new("soil_D".to_string(), 2.0, 100.0, 8.0),
    ];

    soil_list.sort_by(|a, b| {
        a.product_num_per_investment_per_area
            .partial_cmp(&b.product_num_per_investment_per_area)
            .unwrap()
    });

    println!("List of Types of Soils:");
    for i in 0..soil_list.len() {
        print!("{} ", soil_list[i].name);
    }
    println!("");

    // get mininum soil
    let ptr_min: usize;
    let product_supply_possible: f32;
    let mut supply_demand_rate: f32;
    (ptr_min, product_supply_possible, supply_demand_rate) =
        get_min_soil(&mut soil_list, product_demand);

    println!("\nmininum soil: {}", soil_list[ptr_min].name);
    println!("supply_demand_rate: {:.2}", supply_demand_rate);
    println!("product_supply_possible: {:.2}", product_supply_possible);

    // ensure the supply demand rate
    println!("\nsupply_demand_rate and if_need_supply_demand_balance");
    if supply_demand_rate > 1.0 {
        println!("supply > demand");
        if if_need_supply_demand_balance {
            println!("Keep them balance by limit the used areas of soils!\n");
            supply_demand_rate = 1.0;
        } else {
            println!("May reduce the price!\nBut we keep them balance\nto simplify the economic relationship.\nAnd it is really reasonable to do so.\n");
            supply_demand_rate = 1.0;
        }
    } else if supply_demand_rate < 1.0 {
        println!("supply < demand");
        if if_need_supply_demand_balance {
            println!("Keep them balance by import and so on!\n");
            supply_demand_rate = 1.0;
        } else {
            println!("Raise the price!\n");
        }
    }

    // get the price of product
    let product_price: f32 = get_product_price(
        soil_list[ptr_min].investment_sum,
        soil_list[ptr_min].product_num_sum,
        profit_rate,
        supply_demand_rate,
    );
    println!("product_price: {:.2}", product_price);

    // get the imagine equilibrium price
    let product_price_equilibrium: f32 = get_product_price(
        soil_list[ptr_min].investment_sum,
        soil_list[ptr_min].product_num_sum,
        profit_rate,
        1.0,
    );
    println!(
        "product_price_equilibrium: {:.2}\n",
        product_price_equilibrium
    );

    // get the actual used area of mininum soil
    let supply_overflow_min_soil: f32 = if product_supply_possible - product_demand > 0.0 {
        product_supply_possible - product_demand
    } else {
        0.0
    };
    let product_supply: f32 = product_supply_possible - supply_overflow_min_soil;
    println!("product_supply:{:.2}", product_supply);

    let area_overflow_min_soil: f32 =
        supply_overflow_min_soil / soil_list[ptr_min].product_num_per_area;
    soil_list[ptr_min].area_used -= area_overflow_min_soil;
    println!(
        "soil_list[ptr_min].area_used: {:.2}",
        soil_list[ptr_min].area_used
    );

    // calc datas of soils
    let mut product_value_total: f32 = 0.0;
    let mut super_profit_individual: f32;
    let mut super_profit_total: f32 = 0.0;

    let soil_columns: [&str; 9] = [
        "soil_name",
        "area_used",
        "product_num_per_area",
        "product_num_individual",
        "investment",
        "product_price",
        "product_price_equilibrium",
        "product_value_individual",
        "super_profit_individual",
    ];
    let mut soil_indexs: Vec<&str> = vec![];
    let mut soil_datas: Vec<Vec<f32>> = vec![];

    for i in 0..soil_list.len() {
        let product_num_individual: f32 =
            soil_list[i].area_used * soil_list[i].product_num_per_area;

        let product_value_individual: f32 = product_price * product_num_individual;

        let product_value_image: f32 = soil_list[i].area_used
            * soil_list[ptr_min].product_num_per_area
            * product_price_equilibrium;

        super_profit_individual = product_value_individual - product_value_image;

        soil_indexs.push(&soil_list[i].name);
        soil_datas.push(vec![
            soil_list[i].area_used,
            soil_list[i].product_num_per_area,
            product_num_individual,
            soil_list[i].investment_sum * (soil_list[i].area_used / soil_list[i].area_sum),
            product_price,
            product_price_equilibrium,
            product_value_individual,
            super_profit_individual,
        ]);

        product_value_total += product_value_individual;
        super_profit_total += super_profit_individual;
    }

    println!("\nproduct_value_total: {:.2}", product_value_total);
    println!("super_profit_total: {:.2}", super_profit_total);

    // show datas of soil:
    println!();
    for idx in 0..soil_columns.len() {
        print!("{}, ", soil_columns[idx]);
    }
    println!();

    for i in 0..soil_indexs.len() {
        print!("{}, ", soil_indexs[i]);
        for j in 00..soil_datas[i].len() {
            print!("{}, ", soil_datas[i][j]);
        }
        println!();
    }

    // transform super profit to rent
    let transform_rate_from_super_profit_to_rent: f32 = 1.0;
    let rent_possible = super_profit_total * transform_rate_from_super_profit_to_rent;
    let rent_total: f32 = if rent_possible > 0.0 {
        rent_possible
    } else {
        0.0
    };
    println!("\nrent_total: {:.2}\n", rent_total);

    let mut area_used_total: f32 = 0.0;
    for i in 0..soil_list.len() {
        area_used_total += soil_list[i].area_used;
    }
    println!("area_used_total: {:.2}", area_used_total);

    let rent_per_area_avg: f32 = rent_total / area_used_total;
    println!("rent_per_area_avg: {:.2}", rent_per_area_avg);

    let mut investment_total: f32 = 0.0;
    for i in 0..soil_list.len() {
        investment_total +=
            soil_list[i].investment_sum * (soil_list[i].area_used / soil_list[i].area_sum);
    }
    println!("\ninvestment_total: {:.2}", investment_total);

    let rent_per_capital_avg: f32 = rent_total / investment_total;
    println!(
        "rent_per_capital_avg: {:.2}%",
        rent_per_capital_avg * 100.00
    );
}
