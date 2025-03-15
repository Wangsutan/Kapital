use serde::{Deserialize, Serialize};
use std::fs;
use std::io::{self, Write};
use std::path::Path;
use toml::Value;
use walkdir::WalkDir;

#[derive(Serialize, Deserialize, Debug)]
struct Product {
    #[serde(rename = "产品名称")] // 自定义序列化和反序列化时的字段名称
    product_name: String,
    #[serde(rename = "交换比例")] // 自定义序列化和反序列化时的字段名称
    exchange_rate: Vec<String>,
}

/// 从TOML值中提取商品信息的函数
fn extract_goods(value: &Value) -> Vec<[String; 2]> {
    let mut goods = Vec::new();
    for (key, table) in value.as_table().unwrap().iter() {
        if let Some(array) = table.as_array() {
            for item in array {
                if let Some(item_table) = item.as_table() {
                    if let Some(product_name) = item_table.get("产品名称").and_then(|v| v.as_str())
                    {
                        if let Some(exchange_rate) =
                            item_table.get("交换比例").and_then(|v| v.as_array())
                        {
                            let from = exchange_rate[0].as_str().unwrap().trim_matches('"');
                            let to = exchange_rate[1].as_str().unwrap().trim_matches('"');
                            // println!("{}, {}, {}, {}", key, from, product_name, to);
                            goods.push([product_name.to_string(), to.to_string()]);
                            // 避免重复添加基础商品
                            if !goods.contains(&[key.to_string(), from.to_string()]) {
                                goods.push([key.to_string(), from.to_string()]);
                            }
                        }
                    }
                }
            }
        }
    }
    goods
}

/// 创建单个交换关系表的函数
fn create_single_change_table(
    one: &[String; 2],
    another: &[String; 2],
) -> toml::map::Map<String, Value> {
    let mut single_change_table = toml::map::Map::new();

    // 向等价物表中添加等价物名称
    let good_equivalent_form_of_value = toml::Value::String(another[0].to_string());
    single_change_table.insert("产品名称".to_string(), good_equivalent_form_of_value);

    // 向等价物表中添加交换比例
    let quantity_good_equivalent_form_of_value = toml::Value::String(another[1].to_string());
    let quantity_good_relative_form_of_value = toml::Value::String(one[1].to_string());
    single_change_table.insert(
        "交换比例".to_string(),
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
    for entry in WalkDir::new(dir) {
        let entry = entry?;
        let path = entry.path();

        if let Some(file_name_os) = path.file_stem() {
            if let Some(file_name) = file_name_os.to_str() {
                // 过滤条件：toml文件，排除Cargo.toml和complete文件
                if path.extension().map_or(false, |e| e == "toml")
                    && !file_name.contains("Cargo")
                    && !file_name.contains("complete")
                    && !file_name.contains("test")
                {
                    println!("正在处理文件: {}", path.display());

                    // 生成输出路径
                    let output_path = Path::new(dir).join("datas_completed");
                    fs::create_dir_all(&output_path)?; // 确保输出目录存在

                    // 调用 process_file 函数
                    process_file(path, output_path.to_str().unwrap(), file_name)?;
                }
            } else {
                eprintln!("文件名包含无效的 UTF-8 字符: {}", path.display());
            }
        } else {
            eprintln!("路径没有文件名: {}", path.display());
        }
    }

    println!("所有TOML文件处理完成");
    Ok(())
}