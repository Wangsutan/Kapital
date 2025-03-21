use petgraph::graph::DiGraph;
use petgraph::stable_graph::NodeIndex;
use petgraph::visit::EdgeRef;
use rayon::prelude::*;
use regex::Regex;
use std::collections::{HashMap, HashSet};
use std::fs;
use std::sync::mpsc; // 用于线程间通信

lazy_static::lazy_static! {
        // 孤立节点
    static ref NODE_PATTERN: Regex = Regex::new(r#""((?:\\"|[^"])*)""#).unwrap();
        // 带标签的边，有四个捕获组：1. 源节点名称，2. 目标节点名称， 3. 整个 [label="..."] 部分， 4. 标签内容
    static ref EDGE_PATTERN: Regex = Regex::new(
        r#""((?:\\"|[^"])*)"\s*->\s*"((?:\\"|[^"])*)"\s*(\[label="((?:\\"|[^"])*)")?\]?"#,
    ).unwrap();
}

fn main() {
    let directory = "../datas_graphs_generated";
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
        if let Ok(dot_content) = fs::read_to_string(path) {
            if let Some(graph) = parse_dot(&dot_content) {
                let output = validate_graph_output(&graph);
                s.send((file_name, output)).unwrap();
            } else {
                eprintln!("无法解析 DOT 文件: {:?}", path);
            }
        } else {
            eprintln!("无法读取文件: {:?}", path);
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
    let mut node_map = HashMap::new(); // 缓存节点以避免重复添加

    for line in dot_content.lines() {
        let line = line.trim();
        if line.is_empty() || line.starts_with("//") || line.contains("rankdir") {
            continue;
        }

        // 解析边
        if let Some(caps) = EDGE_PATTERN.captures(line) {
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
        else if let Some(caps) = NODE_PATTERN.captures(line) {
            let node = caps[1].replace(r#"\""#, "\"");
            node_map
                .entry(node.clone())
                .or_insert_with(|| di_graph.add_node(node)); // 确保孤立节点亦被添加到图中
        }
    }

    Some(di_graph)
}

/// 生成验证图的输出字符串
fn validate_graph_output(graph: &DiGraph<String, String>) -> String {
    let mut output = String::new();

    let (has_self_loop, self_loop_nodes) = check_self_loops(graph);
    if has_self_loop {
        output.push_str("存在自身交换\n");
        for node in self_loop_nodes {
            output.push_str(&format!("  {}\n", graph[node]));
        }
    } else {
        output.push_str("不存在自身交换\n");
    }

    let (has_duplicate, duplicate_edges) = check_duplicate_edges(graph);
    if has_duplicate {
        output.push_str("存在重复交换\n");
        for (source, target) in &duplicate_edges {
            output.push_str(&format!(
                "  {} -> {}\n",
                graph[source.clone()],
                graph[target.clone()]
            ));
        }
    } else {
        output.push_str("不存在重复交换\n");
    }

    let (is_complete, missing_edges) = check_complete_graph(graph);
    if is_complete {
        output.push_str(&format!("每个商品直接交换所有其他商品\n"));
    } else {
        output.push_str("\n缺失的交换关系：\n");
        for (node, missing) in missing_edges {
            output.push_str(&format!(
                "  节点 `{}` 未连接到: {:?}\n",
                graph[node], missing
            ));
        }
    }

    let currencies = find_currencies(graph);
    if currencies.is_empty() {
        output.push_str(&format!("不存在货币\n"));
    } else {
        output.push_str(&format!("货币形式数量：{}\n", currencies.len()));
        output.push_str(&format!("  {}\n", currencies.join(", ")));
    }

    output
}

/// 检查图中是否存在自环
fn check_self_loops(graph: &DiGraph<String, String>) -> (bool, Vec<NodeIndex>) {
    let edges: Vec<_> = graph.edge_references().collect();
    let has_self_loop = std::sync::Mutex::new(false);
    let self_loop_nodes = std::sync::Mutex::new(Vec::new());

    // 并行遍历边
    edges.par_iter().for_each(|&edge| {
        if edge.source() == edge.target() {
            *has_self_loop.lock().unwrap() = true;
            self_loop_nodes.lock().unwrap().push(edge.source());
        }
    });

    (
        has_self_loop.into_inner().unwrap(),
        self_loop_nodes.into_inner().unwrap(),
    )
}

/// 检查图中是否存在重复边
fn check_duplicate_edges(graph: &DiGraph<String, String>) -> (bool, Vec<(NodeIndex, NodeIndex)>) {
    let edges: Vec<_> = graph.edge_references().collect();
    let has_duplicate = std::sync::Mutex::new(false);
    let duplicate_edges = std::sync::Mutex::new(Vec::new());
    let edge_set = std::sync::Mutex::new(HashSet::new());

    // 并行遍历边
    edges.par_iter().for_each(|&edge| {
        let key = (edge.source(), edge.target());
        let contains = {
            let mut edge_set = edge_set.lock().unwrap();
            if edge_set.contains(&key) {
                true
            } else {
                edge_set.insert(key);
                false
            }
        };
        if contains {
            *has_duplicate.lock().unwrap() = true;
            duplicate_edges.lock().unwrap().push(key);
        }
    });

    (
        has_duplicate.into_inner().unwrap(),
        duplicate_edges.into_inner().unwrap(),
    )
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
    let total_nodes_min = 4; // 总边数不能太少，意思是市场中有必要数量的商品。
    let node_outgoing_max = 3; // 货币作为相对价值形式的最大数量，意思是它不能过多地把别的商品作为货币。

    // 将 NodeIndices 转换为 Vec<NodeIndex>，然后使用 par_iter
    let nodes: Vec<NodeIndex> = graph.node_indices().collect();

    nodes
        .par_iter() // 并行迭代器
        .filter(|&&node| {
            let node_ingoing_count = graph
                .edges_directed(node, petgraph::Direction::Incoming)
                .count();
            total_nodes >= total_nodes_min
                && graph.edges(node).count() <= node_outgoing_max
                && node_ingoing_count == total_nodes - 1
        })
        .map(|&node| graph[node].clone())
        .collect()
}
