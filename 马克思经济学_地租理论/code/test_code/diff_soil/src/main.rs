fn main() {
    println!("Get Minimum Soil!");

    let mut soil_types = [2.0, 8.5, 6.0, 20.5];
    soil_types.sort_by(|a, b| a.partial_cmp(b).unwrap());
    soil_types.reverse();
    println!("{:?}", soil_types);

    let soil_demand:f32 = 30.0;
    let mut soil_min_used:f32 = 0.0;
    let mut production_total:f32 = 0.0;
    for (i, v) in soil_types.iter().enumerate() {
        production_total += v;
        if production_total >= soil_demand {
            println!("soil_min: {}", i);
            soil_min_used = soil_demand - (production_total - v);
            break;
        }
    }
    println!{"soil_min_used: {}", soil_min_used};
}
