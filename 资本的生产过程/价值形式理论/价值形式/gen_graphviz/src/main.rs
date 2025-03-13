use std::fs;
use std::io::{self};
use std::process::Command;
use toml::Value;
use walkdir::WalkDir;

fn create_dot(value: Value) -> String {
    let mut dot = format!("digraph 价值形式理论 {{\n    rankdir=LR;\n    node [shape=record];\n");
    for (good_relative_form_of_value, table_good_equivalent_form_of_value) in
        value.as_table().unwrap().iter()
    {
        if let Some(equivalent_array_table) = table_good_equivalent_form_of_value.as_array() {
            for equivalent in equivalent_array_table {
                if let Some(equivalent_table) = equivalent.as_table() {
                    if let Some(good_equivalent) =
                        equivalent_table.get("产品名称").and_then(|v| v.as_str())
                    {
                        if let Some(exchange_rate) =
                            equivalent_table.get("交换比例").and_then(|v| v.as_array())
                        {
                            let quantity_good_relative =
                                exchange_rate[0].as_str().unwrap().trim_matches('"');
                            let quantity_good_equivalent =
                                exchange_rate[1].as_str().unwrap().trim_matches('"');
                            dot.push_str(&format!(
                                "    \"{} {}\" -> \"{} {}\";\n",
                                quantity_good_relative,
                                good_relative_form_of_value,
                                quantity_good_equivalent,
                                good_equivalent
                            ));
                        }
                    }
                }
            }
        }
    }
    dot.push_str("}\n");

    dot
}

fn main() -> io::Result<()> {
    let dir = "../../"; // 指定要遍历的目录

    for entry in WalkDir::new(dir) {
        let entry = entry?;
        let path = entry.path();
        if path.extension().map_or(false, |e| e == "toml")
            && path.file_name().unwrap() != "Cargo.toml"
        {
            let file_name = path.file_stem().unwrap().to_str().unwrap();
            let content = fs::read_to_string(path)?;
            let value: Value = toml::from_str(&content)?;

            let dot: String = create_dot(value);

            // 输出 DOT 描述到文件
            let output_path = format!("{}/{}.dot", dir, file_name);
            fs::write(&output_path, dot)?;

            // 调用外部命令将 dot 文件转换成 png 图像
            let output_img_path = format!("{}/{}.png", dir, file_name);
            let status = Command::new("dot")
                .arg("-Tpng")
                .arg(&output_path)
                .arg("-o")
                .arg(&output_img_path)
                .status()?;

            if !status.success() {
                return Err(io::Error::new(
                    io::ErrorKind::Other,
                    "Failed to execute dot command",
                ));
            }
        }
    }

    Ok(())
}
