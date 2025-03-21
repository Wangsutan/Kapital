use rayon::prelude::*;
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::fs;
use std::io::{self, Write};
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

/// 从TOML值中提取商品信息的函数
fn extract_goods(value: &Value) -> Vec<[String; 2]> {
    let mut goods_map = HashMap::new(); // 用于去重的 HashMap
    for (key, table) in value.as_table().unwrap().iter() {
        if let Some(array) = table.as_array() {
            for item in array {
                if let Some(item_table) = item.as_table() {
                    if let Some(product_name) =
                        item_table.get("Product Name").and_then(|v| v.as_str())
                    {
                        if let Some(exchange_rate) =
                            item_table.get("Exchange Ratio").and_then(|v| v.as_array())
                        {
                            let from = exchange_rate[0].as_str().unwrap().trim_matches('"');
                            let to = exchange_rate[1].as_str().unwrap().trim_matches('"');

                            // 添加商品和兑换比例
                            goods_map.insert(product_name.to_string(), to.to_string());
                            goods_map.insert(key.to_string(), from.to_string());
                        }
                    }
                }
            }
        }
    }

    // 将 HashMap 转换为 Vec<[String; 2]>
    goods_map.into_iter().map(|(k, v)| [k, v]).collect()
}

/// 创建单个交换关系表的函数
fn create_single_change_table(
    one: &[String; 2],
    another: &[String; 2],
) -> toml::map::Map<String, Value> {
    let mut single_change_table = toml::map::Map::new();

    // 向等价物表中添加等价物名称
    let good_equivalent_form_of_value = toml::Value::String(another[0].to_string());
    single_change_table.insert("Product Name".to_string(), good_equivalent_form_of_value);

    // 向等价物表中添加 Exchange Ratio
    let quantity_good_equivalent_form_of_value = toml::Value::String(another[1].to_string());
    let quantity_good_relative_form_of_value = toml::Value::String(one[1].to_string());
    single_change_table.insert(
        "Exchange Ratio".to_string(),
        toml::Value::Array(vec![
            quantity_good_relative_form_of_value,
            quantity_good_equivalent_form_of_value,
        ]),
    );

    single_change_table
}

/// 处理单个文件生成完整交换关系表
fn process_file(input_path: &Path, output_path: &str, file_name: &str) -> io::Result<()> {
    // 读取输入文件
    let content = fs::read_to_string(input_path)?;
    let value: Value = toml::from_str(&content)
        .map_err(|e| io::Error::new(io::ErrorKind::Other, e.to_string()))?;
    let goods = extract_goods(&value);

    // 生成输出文件名
    let output_path = Path::new(output_path).join(format!("{}_complete.toml", file_name));
    // 初始化输出文件
    fs::write(&output_path, "")?;
    let mut file = std::fs::OpenOptions::new()
        .append(true) // 设置追加模式
        .create(true) // 如果文件不存在则创建
        .open(output_path)?;

    // 遍历 goods 数据，生成排列组合
    for one in &goods {
        let mut toml_table = toml::map::Map::new(); // 该表存放某种商品的交换关系
        for another in &goods {
            // 创建一个某种商品的等价物数组表
            let mut equivalent_array_table = Vec::new();
            // 避免自身交换
            if one != another {
                let single_change_table = create_single_change_table(one, another);
                // 将等价物表增添到某种商品的等价物数组表中
                equivalent_array_table.push(toml::Value::Table(single_change_table));
            }
            // 将等价物数组表插入到主表中
            if !equivalent_array_table.is_empty() {
                // 插入相对价值物和等价物相关数据
                let good_relative_form_of_value = one[0].to_string();
                toml_table.insert(
                    good_relative_form_of_value,
                    toml::Value::Array(equivalent_array_table),
                );

                // 将生成的 TOML 数据追加写入到文件
                let toml_string = toml::to_string_pretty(&toml_table)
                    .map_err(|e| io::Error::new(io::ErrorKind::Other, e.to_string()))?;
                file.write_all(toml_string.as_bytes())?;
                file.write_all(b"\n")?; // 添加换行符以分隔不同的条目
            }
        }
    }

    Ok(())
}

fn main() -> io::Result<()> {
    // 遍历指定目录下的所有toml文件
    let dir = "../"; // 指定要遍历的目录

    // 收集所有需要处理的文件路径
    let paths: Vec<_> = WalkDir::new(dir)
        .min_depth(1)
        .into_iter()
        .filter_map(|e| e.ok())
        .filter(|entry| {
            let path = entry.path();
            let file_name = path.file_name().unwrap().to_str().unwrap();
            path.extension().map_or(false, |ext| ext == "toml")
                && !file_name.contains("Cargo")
                && !file_name.contains("complete")
                && !file_name.contains("test")
        })
        .map(|entry| entry.path().to_path_buf())
        .collect();

    // 生成输出路径
    let output_path = Path::new(dir).join("datas_completed");
    fs::create_dir_all(&output_path)?; // 确保输出目录存在

    // 使用 rayon 并行处理文件
    let results: Vec<_> = paths
        .par_iter() // 并行迭代器
        .filter_map(|path| {
            let file_name = path.file_name().unwrap().to_str().unwrap();
            match process_file(path, output_path.to_str().unwrap(), file_name) {
                Ok(_) => None,
                Err(e) => Some(format!("处理文件 {:?} 时出错: {}", path, e)),
            }
        })
        .collect();

    // 打印所有错误信息
    if !results.is_empty() {
        for result in results {
            eprintln!("{}", result);
        }
    }

    Ok(())
}
