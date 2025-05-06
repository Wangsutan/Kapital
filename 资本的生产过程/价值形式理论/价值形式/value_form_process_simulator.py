# 价值形式全过程模拟器（多线程优化版）
import os
import glob
import random
import json
from PIL import Image
import networkx as nx
import matplotlib

matplotlib.use("Agg")  # 使用非交互式后端
import matplotlib.pyplot as plt
from typing import Dict, List, Set, Tuple
import math
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor
import threading

# 全局变量用于存储绘图任务
plot_tasks = []
plot_lock = threading.Lock()


def generate_time_step(t: int, products: List[str], layout: Dict, output_dir: str):
    """处理单个时间步的生成任务"""
    dot_filename = os.path.join(output_dir, f"exchange_{t:02d}.dot")
    bidirectional_filename = os.path.join(output_dir, f"bidirectional_{t:02d}.json")
    cycles_filename = os.path.join(output_dir, f"cycles_{t:02d}.json")

    with open(dot_filename, "w") as dot_file, open(
        cycles_filename, "w"
    ) as cycles_file, open(bidirectional_filename, "w") as bidirectional_file:
        # 写入DOT文件头
        dot_file.write("digraph {\n")
        dot_file.write("    layout=neato;\n")
        dot_file.write("    overlap=false;\n")
        dot_file.write("    splines=true;\n")

        # 写入节点定义
        for product in products:
            dot_file.write(
                f'    {product} [pos="{layout[product]["pos"]}", style=filled, fillcolor="{layout[product]["color"]}"];\n'
            )

        # 构建图并记录边
        G = nx.DiGraph()
        edge_records: List[Tuple[str, str]] = []
        bidirectional_edges: Set = set()

        exchange_prob = 0.25
        for src in products:
            for dst in products:
                if src != dst and random.random() < exchange_prob:
                    G.add_edge(src, dst)
                    edge_records.append((src, dst))
                    # 检测双向边
                    if G.has_edge(dst, src):
                        bidirectional_edges.add(frozenset({src, dst}))

        # 检测双向边并保存到文件
        bidirectionals: List[List] = [list(pair) for pair in bidirectional_edges]
        json.dump(bidirectionals, bidirectional_file, indent=2)

        # 检测环并保存到文件
        cycles: List[List] = [cycle for cycle in nx.simple_cycles(G) if len(cycle) >= 3]
        json.dump(cycles, cycles_file, indent=2)

        # 找出无法交换的节点
        bidirectional_nodes_set = set()
        for pair in bidirectionals:
            bidirectional_nodes_set.update(pair)

        cycle_nodes = set()
        for cycle in cycles:
            cycle_nodes.update(cycle)

        # 排除双向边和环中的节点
        candidate_nodes = [
            p
            for p in products
            if p not in bidirectional_nodes_set and p not in cycle_nodes
        ]

        non_exchangeable_node_set = set()
        for node in candidate_nodes:
            if G.out_degree(node):  # 有出度
                targets = set(G.successors(node))
                # 检查所有目标节点是否都没有指向该节点的边
                if all(not G.has_edge(target, node) for target in targets):
                    non_exchangeable_node_set.add(node)

        # 从环中的节点中，排除双向边中的节点
        cycle_nodes_set = set(cycle_nodes) - bidirectional_nodes_set

        # 收集绘图任务而不是直接绘图
        if non_exchangeable_node_set or bidirectional_nodes_set or cycle_nodes_set:
            with plot_lock:
                plot_tasks.append(
                    (
                        non_exchangeable_node_set,
                        bidirectional_nodes_set,
                        cycle_nodes_set,
                        output_dir,
                        t,
                    )
                )

        # 确定边颜色
        edge_colors: Dict[Tuple[str, str]] = {}
        cycle_edges: Set = set()
        for cycle in cycles:
            for i in range(len(cycle)):
                cycle_edges.add((cycle[i], cycle[(i + 1) % len(cycle)]))

        # 写入边定义
        for src, dst in edge_records:
            if frozenset({src, dst}) in bidirectional_edges:
                edge_colors[(src, dst)] = "#00ff00"  # 双向边绿色
            else:
                edge_colors[(src, dst)] = "#ff0000"  # 单向边红色
            dot_file.write(
                f'    {src} -> {dst} [color="{edge_colors[(src, dst)]}", arrowsize=0.8];\n'
            )
        dot_file.write("}\n")


def execute_plot_tasks():
    """在主线程执行所有积压的绘图任务"""
    global plot_tasks
    while plot_tasks:
        task = plot_tasks.pop(0)
        _plot_node_distribution(*task)


def _plot_node_distribution(
    non_exchangeable_node_set,
    bidirectional_nodes_set,
    cycle_nodes_set,
    output_dir,
    time_step,
):
    """实际的绘图函数（确保在主线程调用）"""
    # 计算各类节点数量
    special_count = len(non_exchangeable_node_set)
    bidirectional_count = len(bidirectional_nodes_set)
    cycle_count = len(cycle_nodes_set)

    # 合并所有节点类别
    categories = []
    counts = []
    colors = []

    # 定义颜色映射：红、绿、黄
    color_map = {
        "non_exchangeable_node": "red",
        "bidirectional_nodes": "green",
        "cycle_nodes": "yellow",
    }

    if special_count > 0:
        categories.append("non_exchangeable_node")
        counts.append(special_count)
        colors.append(color_map["non_exchangeable_node"])
    if bidirectional_count > 0:
        categories.append("bidirectional_nodes")
        counts.append(bidirectional_count)
        colors.append(color_map["bidirectional_nodes"])
    if cycle_count > 0:
        categories.append("cycle_nodes")
        counts.append(cycle_count)
        colors.append(color_map["cycle_nodes"])

    if not counts:
        print(f"时间步 {time_step}: 没有节点数据可显示")
        return

    os.makedirs(output_dir, exist_ok=True)

    plt.figure(figsize=(8, 6))
    plt.pie(counts, labels=categories, autopct="%1.1f%%", startangle=90, colors=colors)
    plt.title(f"Nodes Distribution (Time Step {time_step})")
    plt.axis("equal")

    plot_filename = os.path.join(output_dir, f"node_distribution_{time_step:02d}.png")
    plt.savefig(plot_filename, dpi=300, bbox_inches="tight")
    plt.close()


class ExchangeDifficultyError(Exception):
    """自定义异常：交换难度计算错误"""

    pass


def exponential_exchange_difficulty(n: int, base: float = 2, k: float = 1) -> float:
    """
    计算环形交换难度的指数增长模型（含异常处理）
    """
    try:
        if n < 3:
            raise ExchangeDifficultyError(f"节点数至少为3，当前n={n}")
        if base <= 1:
            raise ExchangeDifficultyError(f"基数必须>1，当前base={base}")

        difficulty = k * (base ** (n - 2))

        if math.isinf(difficulty):
            raise ExchangeDifficultyError(f"计算结果溢出（n={n}, base={base}）")

        return difficulty

    except OverflowError:
        raise ExchangeDifficultyError("数学计算溢出！请减小base或n") from None
    except TypeError as e:
        raise ExchangeDifficultyError(f"输入类型错误: {str(e)}") from None


def render_single_dot(dot_file: str):
    """单个DOT文件的渲染任务"""
    output_png = dot_file.replace(".dot", ".png")
    os.system(f"dot -Tpng {dot_file} -o {output_png}")


def render_dot_files(output_dir: str) -> None:
    """多线程渲染DOT文件"""
    dot_files = sorted(glob.glob(os.path.join(output_dir, "exchange_*.dot")))

    with ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(render_single_dot, dot_file) for dot_file in dot_files
        ]

        for i, future in enumerate(concurrent.futures.as_completed(futures)):
            try:
                future.result()
                print(f"\r渲染进度: {i+1}/{len(dot_files)}", end="")
            except Exception as e:
                print(f"\n渲染失败: {str(e)}")


def create_gif_animation(output_dir: str):
    png_files = sorted(glob.glob(os.path.join(output_dir, "exchange_*.png")))
    images = [Image.open(png).resize((800, 600), Image.LANCZOS) for png in png_files]
    gif_path = os.path.join(output_dir, "dynamic_exchange.gif")
    images[0].save(
        gif_path,
        save_all=True,
        append_images=images[1:],
        duration=1000,
        loop=0,
        optimize=True,
    )


def generate_dot_series_with_layout(
    output_dir: str, time_steps: int, products: List[str]
) -> None:
    global plot_tasks
    plot_tasks = []  # 重置绘图任务队列

    os.makedirs(output_dir, exist_ok=True)

    # 生成随机布局（所有时间步共享）
    layout: Dict = {}
    for product in products:
        layout[product] = {
            "pos": f"{random.uniform(0, 10)}, {random.uniform(0, 10)}!",
            "color": (
                "gold"
                if product == "Gold"
                else (
                    "silver"
                    if product == "Silver"
                    else "#%06x" % random.randint(0, 0xFFFFFF)
                )
            ),
        }

    # 多线程生成时间步
    with ThreadPoolExecutor() as executor:
        futures = []
        for t in range(time_steps):
            futures.append(
                executor.submit(generate_time_step, t, products, layout, output_dir)
            )

        for i, future in enumerate(concurrent.futures.as_completed(futures)):
            try:
                future.result()
                print(f"\r生成进度: {i+1}/{time_steps}", end="")
            except Exception as e:
                print(f"\n生成失败: {str(e)}")


if __name__ == "__main__":
    # 文件路径
    output_dir: str = "./datas_dynamic_graphs"
    # 帧数
    time_steps: int = 60
    # 产品列表
    products: List[str] = [
        "Gold",
        "Silver",
        "Fish",
        "Meat",
        "Grain",
        "Cloth",
        "Wood",
        "Salt",
    ]

    print("生成动态DOT文件")
    generate_dot_series_with_layout(output_dir, time_steps, products)

    # 在主线程执行所有绘图任务
    print("\n绘制节点统计图")
    execute_plot_tasks()

    print("\n渲染PNG图像")
    render_dot_files(output_dir)

    print("\n生成GIF动画")
    create_gif_animation(output_dir)

    # 绘制指数型增长的交换难度曲线
    n_values = range(3, 10)
    difficulties = [exponential_exchange_difficulty(n, math.e, 1) for n in n_values]

    plt.figure(figsize=(10, 6), dpi=100)
    plt.plot(n_values, difficulties, marker="o", label="Exchange Difficulty")
    plt.title("Exponential Growth of Exchange Difficulty\n($D(n) = e^{n-2}$)")
    plt.xlabel("Number of Nodes (n)")
    plt.ylabel("Exchange Difficulty (D)")
    plt.xticks(n_values)
    plt.legend()
    plt.grid(True)
    plt.savefig(f"{output_dir}/exchange_difficulty.png", bbox_inches="tight")
    plt.close()
