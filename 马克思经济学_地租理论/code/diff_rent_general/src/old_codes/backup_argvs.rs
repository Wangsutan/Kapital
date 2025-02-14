    let mut input_string = String::new();
    println!("Please input product demand(f32):");
    io::stdin()
        .read_line(&mut input_string)
        .ok()
        .expect("Failed to read line");

    let product_demand: f32 = match input_string.trim().parse() {
        Ok(product_demand) => product_demand,
        Err(_) => {
            println!("Not right data.");
            return;
        }
    };

    let mut input_string = String::new();
    println!("Please ensure if_need_demand_supply_balance\n(true or false):");
    io::stdin()
        .read_line(&mut input_string)
        .ok()
        .expect("Failed to read line");

    let if_need_demand_supply_balance: bool = match input_string.trim().parse() {
        Ok(if_need_demand_supply_balance) => if_need_demand_supply_balance,
        Err(_) => {
            println!("Not right data.");
            return;
        }
    };
