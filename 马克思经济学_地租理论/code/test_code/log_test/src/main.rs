fn product_force(
    // $$of \times (\log_{base} (af \cdot (x -lr)) + ud)$$
    x: f64,
    base: f64,
    left_right_translate: f64,
    up_down_translate: f64,
    abscissa_flexible: f64,
    ordinate_flexible: f64,
) -> f64 {
    let result: f64 = ordinate_flexible
        * ((abscissa_flexible * (x - left_right_translate)).log(base) + up_down_translate);
    return result;
}

fn main() {
    println!("Hello, log!");
    let x: f64 = 4.0;
    let base: f64 = 16.0;
    let result = x.log(base);
    println!("{}", result);

    let test_num: f64 = product_force(16.0, 2.0, 0.0, 0.0, 4.0, 2.0);
    println!("{}", test_num);
}
