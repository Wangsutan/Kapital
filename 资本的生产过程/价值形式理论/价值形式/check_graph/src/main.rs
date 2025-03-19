use petgraph::graph::DiGraph;
use petgraph::stable_graph::NodeIndex;
use petgraph::visit::EdgeRef;
use rayon::prelude::*; // 引入 rayon 并行库
use regex::Regex;
use std::collections::{HashMap, HashSet};
use std::fs;
use std::sync::mpsc; // 用于线程间通信

fn main() {
    let directory = "../graphs_generated";
    if let Err(e) = process_dot_files(directory) {
        eprintln!("处理文件时出错: {}", e);
    }
}

fn process_dot_files(directory: &str) -> Result<(), Box<dyn std::error::Error>> {
    // 收集所有需要处理的文件路径
    let paths: Vec<_> = fs::read_dir(directory)?
        .filter_map(|entry| {
            let entry = entry.ok()?;
            let path = entry.path();
            if path.extension().and_then(|s| s.to_str()) == Some("dot") {
                Some(path)
            } else {
                None
            }
        })
        .collect();

    // 创建通道
    let (sender, receiver) = mpsc::channel();

    // 使用 rayon 并行处理文件
    paths.par_iter().for_each_with(sender, |s, path| {
        let file_name = path.file_name().unwrap().to_str().unwrap().to_string();
        let dot_content = fs::read_to_string(path).unwrap();
        if let Some(graph) = parse_dot(&dot_content) {
            let output = validate_graph_output(&graph);
            s.send((file_name, output)).unwrap(); // 发送文件名和输出
        } else {
            eprintln!("无法解析 DOT 文件: {:?}", path);
        }
    });

    // 主线程接收并打印输出
    let mut results = Vec::new();
    for (file_name, output) in receiver {
        results.push((file_name, output));
    }

    // 按文件名排序并统一输出
    results.sort_by(|a, b| a.0.cmp(&b.0));
    for (file_name, output) in results {
        println!("\n=== 文件: {} ===", file_name);
        println!("{}", output);
    }

    Ok(())
}

fn parse_dot(dot_content: &str) -> Option<DiGraph<String, String>> {
    let mut di_graph = DiGraph::<String, String>::new();
    let mut node_map = HashMap::new();

    // 正则表达式匹配节点和边
    let node_pattern = Regex::new(r#""((?:\\"|[^"])*)""#).unwrap();
    let edge_pattern = Regex::new(
        r#""((?:\\"|[^"])*)"\s*->\s*"((?:\\"|[^"])*)"\s*(\[label="((?:\\"|[^"])*)")?\]?"#,
    )
    .unwrap();

    for line in dot_content.lines() {
        let line = line.trim();
        if line.is_empty() || line.starts_with("//") || line.contains("rankdir") {
            continue;
        }

        // 解析边
        if let Some(caps) = edge_pattern.captures(line) {
            let source = caps[1].replace(r#"\""#, "\"");
            let target = caps[2].replace(r#"\""#, "\"");
            let label = caps
                .get(4)
                .map_or("".to_string(), |m| m.as_str().replace(r#"\""#, "\""));

            let source_idx = *node_map
                .entry(source.clone())
                .or_insert_with(|| di_graph.add_node(source));
            let target_idx = *node_map
                .entry(target.clone())
                .or_insert_with(|| di_graph.add_node(target));
            di_graph.add_edge(source_idx, target_idx, label);
        }
        // 解析孤立节点
        else if let Some(caps) = node_pattern.captures(line) {
            let node = caps[1].replace(r#"\""#, "\"");
            node_map
                .entry(node.clone())
                .or_insert_with(|| di_graph.add_node(node));
        }
    }

    Some(di_graph)
}

/// 生成验证图的输出字符串
fn validate_graph_output(graph: &DiGraph<String, String>) -> String {
    let mut output = String::new();

    output.push_str(&format!("有无自身交换: {}\n", check_self_loops(graph)));
    output.push_str(&format!("有无重复交换: {}\n", check_duplicate_edges(graph)));

    let (is_complete, missing_edges) = check_complete_graph(graph);
    output.push_str(&format!(
        "每个商品是否直接交换所有其他节点: {}\n",
        is_complete
    ));
    if !is_complete {
        output.push_str("\n缺失的边：\n");
        for (node, missing) in missing_edges {
            output.push_str(&format!("节点 `{}` 未连接到: {:?}\n", graph[node], missing));
        }
    }

    let currencies = find_currencies(graph);
    output.push_str(&format!("货币形式数量: {}\n", currencies.len()));
    if !currencies.is_empty() {
        output.push_str(&format!("货币形式为: {}\n", currencies.join(", ")));
    }

    output
}

/// 检查图中是否存在自环
fn check_self_loops(graph: &DiGraph<String, String>) -> bool {
    graph
        .edge_references()
        .any(|edge| edge.source() == edge.target())
}

/// 检查图中是否存在重复边
fn check_duplicate_edges(graph: &DiGraph<String, String>) -> bool {
    let mut edge_set = HashSet::new();
    for edge in graph.edge_references() {
        let key = (edge.source(), edge.target());
        if edge_set.contains(&key) {
            return true;
        }
        edge_set.insert(key);
    }
    false
}

/// 检查图是否是完全图（并行化）
fn check_complete_graph(graph: &DiGraph<String, String>) -> (bool, Vec<(NodeIndex, Vec<String>)>) {
    let nodes: Vec<NodeIndex> = graph.node_indices().collect();
    let is_complete = std::sync::Mutex::new(true);
    let missing_edges = std::sync::Mutex::new(Vec::new());

    // 并行遍历节点
    nodes.par_iter().for_each(|&node| {
        let out_edges: HashSet<NodeIndex> = graph.edges(node).map(|edge| edge.target()).collect();
        let expected: HashSet<NodeIndex> = nodes.iter().filter(|&&n| n != node).cloned().collect();
        let missing: Vec<String> = expected
            .difference(&out_edges)
            .map(|&n| graph[n].clone())
            .collect();

        if !missing.is_empty() {
            *is_complete.lock().unwrap() = false;
            missing_edges.lock().unwrap().push((node, missing));
        }
    });

    (
        is_complete.into_inner().unwrap(),
        missing_edges.into_inner().unwrap(),
    )
}

/// 查找图中的货币形式（并行化）
fn find_currencies(graph: &DiGraph<String, String>) -> Vec<String> {
    let total_nodes = graph.node_count();
    let total_nodes_min = 3;

    // 将 NodeIndices 转换为 Vec<NodeIndex>，然后使用 par_iter
    let nodes: Vec<NodeIndex> = graph.node_indices().collect();

    nodes
        .par_iter() // 并行迭代器
        .filter(|&&node| {
            graph.edges(node).count() <= 3
                && graph
                    .edges_directed(node, petgraph::Direction::Incoming)
                    .count()
                    == total_nodes - 1
                && total_nodes > total_nodes_min
        })
        .map(|&node| graph[node].clone())
        .collect()
}
