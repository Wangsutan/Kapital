use rayon::prelude::*; // 引入 rayon 并行库
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::fs;
use std::io::{self};
use std::path::Path;
use toml::Value;
use walkdir::WalkDir;

#[derive(Serialize, Deserialize, Debug)]
struct Product {
    #[serde(rename = "Product Name")]
    product_name: String,
    #[serde(rename = "Exchange Ratio")]
    exchange_rate: Vec<String>,
}

/// 从TOML值中提取商品信息的函数，并判断每种key下的product_name是否有重复
fn check_same_goods(value: &Value) -> Vec<String> {
    let mut errors = Vec::new();
    let mut key_product_map: HashMap<String, Vec<(String, usize)>> = HashMap::new(); // 记录每种key下的product_name及其行号

    for (key, table) in value.as_table().unwrap().iter() {
        if let Some(array) = table.as_array() {
            for (index, item) in array.iter().enumerate() {
                if let Some(item_table) = item.as_table() {
                    if let Some(product_name) =
                        item_table.get("Product Name").and_then(|v| v.as_str())
                    {
                        // 判断每种key下的product_name是否有重复
                        let key_entry =
                            key_product_map.entry(key.to_string()).or_insert(Vec::new());

                        // 检查是否重复
                        if let Some((_, line)) =
                            key_entry.iter().find(|(name, _)| name == product_name)
                        {
                            errors.push(format!(
                                "在相对价值物 {} 下，等价物 {} 重复，首次出现在第 {} 行，当前行号为 {}",
                                key, product_name, line, index + 1
                            ));
                        } else {
                            key_entry.push((product_name.to_string(), index + 1)); // 记录行号
                        }
                    }
                }
            }
        }
    }

    errors
}

fn process_file(input_path: &Path) -> io::Result<Vec<String>> {
    // 读取输入文件
    let content = fs::read_to_string(input_path)?;
    let value: Value = toml::from_str(&content)
        .map_err(|e| io::Error::new(io::ErrorKind::Other, e.to_string()))?;

    let errors = check_same_goods(&value);

    Ok(errors)
}

fn main() -> io::Result<()> {
    // 收集所有需要处理的文件路径
    let paths: Vec<_> = WalkDir::new("../")
        .min_depth(1)
        .into_iter()
        .filter_map(|e| e.ok())
        .filter(|entry| {
            let path = entry.path();
            let file_name = path.file_name().unwrap().to_str().unwrap();

            // 过滤条件：toml文件，排除Cargo.toml和complete文件
            path.extension().map_or(false, |e| e == "toml")
                && file_name != "Cargo.toml"
                && !file_name.contains("complete")
        })
        .map(|entry| entry.path().to_path_buf())
        .collect();

    // 使用 rayon 并行处理文件
    let results: Vec<_> = paths
        .par_iter() // 并行迭代器
        .filter_map(|path| match process_file(path) {
            Ok(errors) if !errors.is_empty() => Some(format!(
                "文件 {} 错误信息：\n  {}",
                path.display(),
                errors.join("\n  ")
            )),
            _ => None,
        })
        .collect();

    // 打印所有错误信息
    for result in results {
        println!("{}", result);
    }

    Ok(())
}
