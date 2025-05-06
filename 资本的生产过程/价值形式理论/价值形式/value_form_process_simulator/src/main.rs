use anyhow::{Context, Result, anyhow};
use glob::glob;
use petgraph::{Graph, algo};
use rand::Rng;
use rayon::prelude::*;
use std::process::Command;
use std::{
    collections::{HashMap, HashSet},
    fs::{self, File},
    io::Write as _,
    path::Path,
};

const PRODUCTS: [&str; 8] = [
    "Gold", "Silver", "Fish", "Meat", "Grain", "Cloth", "Wood", "Salt",
];

struct NodeLayout {
    pos: (f64, f64),
    color: String,
}

fn generate_time_step(
    t: usize,
    products: &[String],
    layout: &HashMap<String, NodeLayout>,
    output_dir: &str,
) -> Result<()> {
    let dir_path = Path::new(output_dir);
    fs::create_dir_all(dir_path)?;

    let dot_path = dir_path.join(format!("exchange_{:02}.dot", t));
    let bidirectional_path = dir_path.join(format!("bidirectional_{:02}.json", t));
    let cycles_path = dir_path.join(format!("cycles_{:02}.json", t));

    let mut dot_file = File::create(&dot_path)?;
    let mut bidirectional_file = File::create(&bidirectional_path)?;
    let mut cycles_file = File::create(&cycles_path)?;

    writeln!(dot_file, "digraph {{")?;
    writeln!(dot_file, "    layout=neato;")?;
    writeln!(dot_file, "    overlap=false;")?;
    writeln!(dot_file, "    splines=true;")?;

    let mut rng = rand::rng();
    let graph = Graph::<String, ()>::new();

    let mut edges = Vec::new();
    let exchange_prob = 0.25;

    for src in products {
        for dst in products {
            if src != dst && rng.random_bool(exchange_prob) {
                edges.push((src.clone(), dst.to_string()));
            }
        }
    }

    // Detect bidirectional edges
    let mut bidirectional = HashSet::new();
    let mut edge_set = HashSet::new();
    for (src, dst) in &edges {
        let reverse = (dst.to_string(), src.to_string());
        if edge_set.contains(&reverse) {
            let mut pair = [src.to_string(), dst.to_string()];
            pair.sort();
            bidirectional.insert(pair);
        }
        edge_set.insert((src.to_string(), dst.to_string()));
    }

    // Write bidirectional edges to JSON
    let bidirectionals: Vec<Vec<&str>> = bidirectional
        .iter()
        .map(|pair| vec![pair[0].as_str(), pair[1].as_str()])
        .collect();
    serde_json::to_writer_pretty(&mut bidirectional_file, &bidirectionals)?;

    // Find cycles and write to JSON
    let cycles = find_simple_cycles(&graph);
    serde_json::to_writer_pretty(&mut cycles_file, &cycles)?;

    // Write nodes to DOT file
    for product in products {
        let layout_info = layout.get(product).unwrap();
        writeln!(
            dot_file,
            "    {} [pos=\"{},{}\", style=filled, fillcolor=\"{}\"];",
            product, layout_info.pos.0, layout_info.pos.1, layout_info.color
        )?;
    }

    // Write edges to DOT file
    for (src, dst) in edges {
        let is_bidirectional = bidirectional.contains(&[src.clone(), dst.clone()])
            || bidirectional.contains(&[dst.clone(), src.clone()]);
        let color = if is_bidirectional {
            "#00ff00"
        } else {
            "#ff0000"
        };
        writeln!(
            dot_file,
            "    {} -> {} [color=\"{}\", arrowsize=0.8];",
            src, dst, color
        )?;
    }

    writeln!(dot_file, "}}")?;
    Ok(())
}

fn find_simple_cycles(graph: &Graph<String, ()>) -> Vec<Vec<String>> {
    let mut cycles = Vec::new();
    let scc = algo::kosaraju_scc(graph);

    for component in scc {
        if component.len() >= 3 {
            let mut names: Vec<_> = component.iter().map(|&n| graph[n].clone()).collect();
            names.sort();
            names.dedup();
            cycles.push(names);
        }
    }

    cycles
}

fn exponential_exchange_difficulty(n: usize, base: f64, k: f64) -> Result<f64> {
    if n < 3 {
        return Err(anyhow!("Nodes must be at least 3, got {}", n));
    }
    if base <= 1.0 {
        return Err(anyhow!("Base must be >1, got {:.1}", base));
    }

    let difficulty = k * base.powf((n - 2) as f64);
    if difficulty.is_infinite() {
        return Err(anyhow!("Result overflow (n={}, base={})", n, base));
    }

    Ok(difficulty)
}

fn render_dot_files(output_dir: &str) -> Result<()> {
    let dot_files: Vec<_> = glob(&format!("{}/*.dot", output_dir))?
        .filter_map(|p| p.ok())
        .collect();

    dot_files.par_iter().try_for_each(|path| {
        let output = path.with_extension("png");
        Command::new("dot")
            .arg("-Tpng")
            .arg(path)
            .arg("-o")
            .arg(&output)
            .status()
            .with_context(|| format!("Failed to render {:?}", path))?;
        Ok(())
    })
}

fn create_gif_animation(output_dir: &str) -> Result<()> {
    let output_path = format!("{}/dynamic_exchange.gif", output_dir);

    // 获取已排序的PNG文件列表
    let mut png_files: Vec<_> = glob(&format!("{}/*.png", output_dir))?
        .filter_map(|p| p.ok())
        .collect();

    // 按数字顺序排序文件（如exchange_00.png, exchange_01.png）
    png_files.sort_by(|a, b| {
        let num_a = a
            .file_stem()
            .and_then(|s| s.to_str())
            .and_then(|s| s.split('_').last())
            .and_then(|s| s.parse::<i32>().ok())
            .unwrap_or(0);

        let num_b = b
            .file_stem()
            .and_then(|s| s.to_str())
            .and_then(|s| s.split('_').last())
            .and_then(|s| s.parse::<i32>().ok())
            .unwrap_or(0);

        num_a.cmp(&num_b)
    });

    // 构建convert命令参数
    let mut cmd = Command::new("magick");
    cmd.arg("-delay").arg("100").arg("-loop").arg("0");

    for file in &png_files {
        cmd.arg(file);
    }
    cmd.arg(&output_path);

    // 执行并检查结果
    let status = cmd.status().with_context(|| {
        format!(
            "Failed to generate GIF with ImageMagick. Files: {:?}",
            png_files
        )
    })?;

    if !status.success() {
        return Err(anyhow!("convert command exited with code: {}", status));
    }

    Ok(())
}

fn main() -> Result<()> {
    let output_dir = "./datas_dynamic_graphs";
    let time_steps = 10;
    let products: Vec<String> = PRODUCTS.iter().map(|s| s.to_string()).collect();

    fs::create_dir_all(output_dir)?;

    // Generate random layout
    let mut rng = rand::rng();
    let mut layout = HashMap::new();
    for product in &products {
        let pos = (rng.random_range(0.0..10.0), rng.random_range(0.0..10.0));
        let color = match product.as_str() {
            "Gold" => "gold".to_owned(),
            "Silver" => "silver".to_owned(),
            _ => format!("#{:06x}", rng.random::<u32>() & 0xFFFFFF),
        };
        layout.insert(product.clone(), NodeLayout { pos, color });
    }

    // Generate time steps in parallel
    (0..time_steps)
        .into_par_iter()
        .try_for_each(|t| generate_time_step(t, &products, &layout, output_dir))?;

    // Generate node distribution plots
    for t in 0..time_steps {
        let bidirectional_path = format!("{}/bidirectional_{:02}.json", output_dir, t);
        let cycles_path = format!("{}/cycles_{:02}.json", output_dir, t);

        let bidirectional: Vec<Vec<String>> = if let Ok(file) = fs::File::open(&bidirectional_path)
        {
            serde_json::from_reader(file).unwrap_or_default()
        } else {
            Vec::new()
        };

        let cycles: Vec<Vec<String>> = if let Ok(file) = fs::File::open(&cycles_path) {
            serde_json::from_reader(file).unwrap_or_default()
        } else {
            Vec::new()
        };

        let non_exchangeable = products.len() - bidirectional.len() - cycles.len();

        // 改进输出格式，使用固定宽度列
        println!(
            "时间步长 {:02}\n\
            双向交换: {:<30?}\n\
            环式交换: {:<30?}\n\
            非可交换: {:<5}\n\
            ===============================",
            t, bidirectional, cycles, non_exchangeable
        );
    }

    // Render and create animation
    render_dot_files(output_dir)?;
    create_gif_animation(output_dir)?;

    println!(
        "Exchange difficulty: {}",
        exponential_exchange_difficulty(3, 2.0, 1.0)?
    );

    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;
    use anyhow::Result;
    use approx::assert_relative_eq;

    #[test]
    fn test_normal_cases() -> Result<()> {
        assert_relative_eq!(exponential_exchange_difficulty(3, 2.0, 1.0)?, 2.0);
        assert_relative_eq!(
            exponential_exchange_difficulty(5, 3.0, 2.0)?,
            2.0 * 3.0f64.powi(3)
        );
        assert_relative_eq!(
            exponential_exchange_difficulty(10, 1.5, 0.5)?,
            0.5 * 1.5f64.powi(8),
            epsilon = 1e-10
        );
        Ok(())
    }

    #[test]
    fn test_edge_cases() {
        // 合法最小值
        assert!(exponential_exchange_difficulty(3, 1.0001, 1.0).is_ok());
    }

    #[test]
    fn test_invalid_inputs() {
        // 测试非法节点数
        let case = exponential_exchange_difficulty(2, 2.0, 1.0);
        assert!(case.is_err());
        assert_eq!(
            case.unwrap_err().to_string(),
            "Nodes must be at least 3, got 2"
        );

        // 测试边界base值
        let case1 = exponential_exchange_difficulty(5, 1.0, 1.0);
        assert!(case1.is_err());
        assert_eq!(
            case1.unwrap_err().to_string(),
            "Base must be >1, got 1.0" // 注意浮点格式化
        );

        // 测试负数base
        let case2 = exponential_exchange_difficulty(5, -2.0, 1.0);
        assert!(case2.is_err());
    }

    #[test]
    fn test_overflow_protection() {
        // 大基数测试
        let case1 = exponential_exchange_difficulty(10, 1e200, 1.0);
        assert!(case1.is_err());
        assert!(case1.unwrap_err().to_string().contains("overflow"));

        // 大系数测试
        let case2 = exponential_exchange_difficulty(10, 2.0, f64::MAX);
        assert!(case2.is_err());
    }

    #[test]
    fn test_special_values() {
        // 无穷大处理
        let case = exponential_exchange_difficulty(3, f64::INFINITY, 1.0);
        assert!(case.is_err());
    }
}
