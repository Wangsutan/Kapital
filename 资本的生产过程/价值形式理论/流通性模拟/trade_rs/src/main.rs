use rand::Rng;
use std::collections::{HashMap, HashSet};

#[derive(Debug)]
struct Market {
    liquidity: HashMap<String, f64>, // 商品流通性，格式：{商品名称: 流通性评分}
}

impl Market {
    fn new() -> Self {
        Market {
            liquidity: HashMap::new(),
        }
    }

    fn set_liquidity(&mut self, good: &str, change: f64) {
        // 设置商品流通性
        let entry = self.liquidity.entry(good.to_string()).or_insert(0.0);
        *entry += change;
    }

    fn change_liquidity(&mut self, one: &MarketAgent, another: &MarketAgent) {
        // 执行交易，更新商品流通性
        // 获取所有库存和需求商品
        let goods_inventory_all: HashSet<_> = one
            .inventory
            .keys()
            .chain(another.inventory.keys())
            .collect();
        let goods_need_all: HashSet<_> = one.need.keys().chain(another.need.keys()).collect();

        // 找出双方可以交易的商品
        let tradable_goods_one: HashSet<_> = one
            .inventory
            .keys()
            .filter(|&good| another.need.contains_key(good))
            .collect();
        let tradable_goods_another: HashSet<_> = one
            .need
            .keys()
            .filter(|&good| another.inventory.contains_key(good))
            .collect();
        let tradable_goods_all: HashSet<_> = tradable_goods_one
            .union(&tradable_goods_another)
            .cloned()
            .collect();

        // 更新商品流通性
        for good in goods_inventory_all {
            if tradable_goods_all.contains(&good) {
                self.set_liquidity(&good, 1.0); // 可交易的商品流通性增加
            } else {
                self.set_liquidity(&good, -1.0); // 不可交易的商品流通性减少
            }
        }

        for good in goods_need_all {
            if tradable_goods_all.contains(&good) {
                self.set_liquidity(&good, 0.2); // 可交易的需求商品流通性增加
            } else {
                self.set_liquidity(&good, 1.0); // 不可交易的需求商品流通性增加
            }
        }
    }
}

#[derive(Debug)]
struct MarketAgent {
    name: String,
    goods_list: Vec<String>,
    inventory_prob: HashMap<String, f64>,
    need_prob: HashMap<String, f64>,
    inventory: HashMap<String, i32>,
    need: HashMap<String, i32>,
}

impl MarketAgent {
    fn new(
        name: String,
        goods_list: Vec<String>,
        inventory_prob: HashMap<String, f64>,
        need_prob: HashMap<String, f64>,
    ) -> Self {
        MarketAgent {
            name,
            goods_list,
            inventory_prob,
            need_prob,
            inventory: HashMap::new(),
            need: HashMap::new(),
        }
    }

    fn print_info(&self) {
        println!("Agent Name: {}", self.name);
        println!("Inventory:");
        for (good, quantity) in &self.inventory {
            println!("  - {}: {}", good, quantity);
        }
        println!("Need:");
        for (good, quantity) in &self.need {
            println!("  - {}: {}", good, quantity);
        }
    }

    fn generate_random_goods(&mut self) {
        // 随机生成库存和需求商品
        self.inventory.clear(); // 清空当前库存
        self.need.clear(); // 清空当前需求

        let mut rng = rand::rng();
        for good in &self.goods_list {
            // 随机决定商品是出现在库存还是需求中
            let random_location: &str = if rng.random_bool(0.5) {
                "inventory"
            } else {
                "need"
            };

            match random_location {
                "inventory" => {
                    if rng.random::<f64>() < *self.inventory_prob.get(good).unwrap_or(&0.0) {
                        *self.inventory.entry(good.to_string()).or_insert(0) += 1;
                    }
                }
                "need" => {
                    if rng.random::<f64>() < *self.need_prob.get(good).unwrap_or(&0.0) {
                        *self.need.entry(good.to_string()).or_insert(0) += 1;
                    }
                }
                _ => {}
            }
        }
    }
}

fn simulate_trading(market: &mut Market, agents: &mut Vec<MarketAgent>, trade_times: usize) {
    // 模拟交易
    let mut rng = rand::rng();

    for i in 0..trade_times {
        println!("第 {} 次交易", i + 1);
        println!("-----------------------------");
        // 随机选择两个不同的索引
        let one_idx = rng.random_range(0..agents.len());
        let another_idx = loop {
            let idx = rng.random_range(0..agents.len());
            if idx != one_idx {
                break idx;
            }
        };

        // 安全地获取两个不同的可变引用
        let (one, another) = if one_idx < another_idx {
            let (left, right) = agents.split_at_mut(another_idx);
            (&mut left[one_idx], &mut right[0])
        } else {
            let (left, right) = agents.split_at_mut(one_idx);
            (&mut right[0], &mut left[another_idx])
        };

        // 生成随机库存和需求
        one.generate_random_goods();
        one.print_info();
        another.generate_random_goods();
        another.print_info();

        // 更新商品流通性
        market.change_liquidity(one, another);
    }
}

fn main() {
    // 示例商品列表和概率
    let goods_list: Vec<String> = vec!["贝壳", "小麦", "铁", "木材", "上衣"]
        .into_iter()
        .map(|s| s.to_string())
        .collect();
    let inventory_prob: HashMap<String, f64> = vec![
        ("贝壳".to_string(), 0.6),
        ("小麦".to_string(), 0.3),
        ("铁".to_string(), 0.2),
        ("木材".to_string(), 0.2),
        ("上衣".to_string(), 0.2),
    ]
    .into_iter()
    .collect();
    let need_prob: HashMap<String, f64> = vec![
        ("贝壳".to_string(), 0.6),
        ("小麦".to_string(), 0.3),
        ("铁".to_string(), 0.2),
        ("木材".to_string(), 0.2),
        ("上衣".to_string(), 0.2),
    ]
    .into_iter()
    .collect();

    // 创建市场
    let mut market = Market::new();

    // 随机生成市场主体数量
    let num_agents = rand::rng().random_range(3..=10);
    let mut agents: Vec<MarketAgent> = (0..num_agents)
        .map(|i| {
            MarketAgent::new(
                format!("Agent{}", i + 1),
                goods_list.clone(),
                inventory_prob.clone(),
                need_prob.clone(),
            )
        })
        .collect();

    // 模拟交易
    println!("开始模拟交易。");
    let trade_times = 1000000;
    println!("交易次数： {}", trade_times);
    simulate_trading(&mut market, &mut agents, trade_times);

    // 打印最终商品流通性（按值排序）
    let mut sorted_liquidity: Vec<(&String, &f64)> = market.liquidity.iter().collect();
    sorted_liquidity.sort_by(|a, b| b.1.partial_cmp(a.1).unwrap());

    println!("\n最终的商品流通性（按值排序）:");
    for (good, liquidity) in sorted_liquidity {
        println!("{}:\t{:.2}", good, liquidity);
    }
}
