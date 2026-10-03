# 价值形式全过程模拟器（多线程优化版）
import os
import ast
from openai import OpenAI
import glob
import random
import json
from PIL import Image
import networkx as nx
import math
import matplotlib

matplotlib.use("Agg")  # 使用非交互式后端
import matplotlib.pyplot as plt
from typing import Dict, List, Set, Tuple, FrozenSet, Literal, Callable, Union
from openai.types.chat import ChatCompletionMessage, ChatCompletion

import concurrent.futures
from concurrent.futures import ThreadPoolExecutor
import threading
import logging

# 全局变量用于存储绘图任务
plot_tasks: List[
    Tuple[
        Set[str],  # non_exchangeable_nodes
        Set[str],  # bidirectional_nodes
        Set[str],  # cycle_nodes_without_bidirectional_nodes
        str,  # output_dir
        int,  # time_step
    ]
] = []
plot_lock = threading.Lock()


def generate_dot_series_with_layout(
    output_dir: str, time_steps: int, products: List[str]
) -> None:
    global plot_tasks
    plot_tasks = []  # 重置绘图任务队列

    os.makedirs(output_dir, exist_ok=True)

    # 生成随机布局（所有时间步共享）
    layout: Dict[str, Dict[str, str]] = {}
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
            except Exception as e:
                logging.error(f"生成时间步 {i} 失败: {str(e)}")


def generate_time_step(
    t: int, products: List[str], layout: Dict[str, Dict[str, str]], output_dir: str
) -> None:
    """处理单个时间步的生成任务"""
    dot_filename: str = os.path.join(output_dir, f"exchange_{t:02d}.dot")
    bidirectional_filename: str = os.path.join(
        output_dir, f"bidirectional_{t:02d}.json"
    )
    cycles_filename: str = os.path.join(output_dir, f"cycles_{t:02d}.json")

    with (
        open(dot_filename, "w") as dot_file,
        open(cycles_filename, "w") as cycles_file,
        open(bidirectional_filename, "w") as bidirectional_file,
    ):
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
        G: nx.DiGraph = nx.DiGraph()
        edge_records: List[Tuple[str, str]] = []
        bidirectional_edges: Set[FrozenSet[str]] = set()

        exchange_prob: float = 0.25
        for src in products:
            for dst in products:
                if src != dst and random.random() < exchange_prob:
                    G.add_edge(src, dst)
                    edge_records.append((src, dst))
                    # 检测双向边
                    if G.has_edge(dst, src):
                        bidirectional_edges.add(frozenset({src, dst}))

        # 检测双向边并保存到文件
        bidirectionals: List[List[str]] = [list(pair) for pair in bidirectional_edges]
        json.dump(bidirectionals, bidirectional_file, indent=2)

        # 检测环并保存到文件
        cycles: List[List[str]] = [
            cycle for cycle in nx.simple_cycles(G) if len(cycle) >= 3
        ]
        json.dump(cycles, cycles_file, indent=2)

        # 找出无法交换的节点
        bidirectional_nodes: Set[str] = set()
        for pair in bidirectionals:
            bidirectional_nodes.update(pair)

        cycle_nodes: Set[str] = set()
        for cycle in cycles:
            cycle_nodes.update(cycle)

        # 排除双向边和环中的节点
        candidate_nodes: List[str] = [
            p for p in products if p not in bidirectional_nodes and p not in cycle_nodes
        ]

        non_exchangeable_nodes: Set[str] = set()
        for node in candidate_nodes:
            if G.out_degree(node):  # 有出度
                targets: Set[str] = set(G.successors(node))
                # 检查所有目标节点是否都没有指向该节点的边
                if all(not G.has_edge(target, node) for target in targets):
                    non_exchangeable_nodes.add(node)

        # 从环中的节点中，排除双向边中的节点
        cycle_nodes_without_bidirectional_nodes: Set[str] = (
            cycle_nodes - bidirectional_nodes
        )

        # 收集绘图任务而不是直接绘图
        if (
            non_exchangeable_nodes
            or bidirectional_nodes
            or cycle_nodes_without_bidirectional_nodes
        ):
            with plot_lock:
                plot_tasks.append(
                    (
                        non_exchangeable_nodes,
                        bidirectional_nodes,
                        cycle_nodes_without_bidirectional_nodes,
                        output_dir,
                        t,
                    )
                )

        # 确定边颜色
        edge_colors: Dict[Tuple[str, str], str] = {}
        for src, dst in edge_records:
            if frozenset({src, dst}) in bidirectional_edges:
                edge_colors[(src, dst)] = "#00ff00"  # 双向边绿色
            else:
                edge_colors[(src, dst)] = "#ff0000"  # 单向边红色
            dot_file.write(
                f'    {src} -> {dst} [color="{edge_colors[(src, dst)]}", arrowsize=0.8];\n'
            )
        dot_file.write("}\n")


def execute_plot_tasks() -> None:
    """在主线程执行所有积压的绘图任务"""
    global plot_tasks
    while plot_tasks:
        task = plot_tasks.pop(0)
        _plot_node_distribution(*task)


def _plot_node_distribution(
    non_exchangeable_nodes: Set[str],
    bidirectional_nodes: Set[str],
    cycle_nodes_without_bidirectional_nodes: Set[str],
    output_dir: str,
    time_step: int,
) -> None:
    """实际的绘图函数（确保在主线程调用）"""
    # 计算各类节点数量
    special_count: int = len(non_exchangeable_nodes)
    bidirectional_count: int = len(bidirectional_nodes)
    cycle_count: int = len(cycle_nodes_without_bidirectional_nodes)

    # 合并所有节点类别
    categories: List[str] = []
    counts: List[int] = []
    colors: List[str] = []

    # 定义颜色映射：红、绿、黄
    color_map: Dict[str, str] = {
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

    plot_filename: str = os.path.join(
        output_dir, f"node_distribution_{time_step:02d}.png"
    )
    plt.savefig(plot_filename, dpi=300, bbox_inches="tight")
    plt.close()


class ExchangeDifficultyError(Exception):
    """自定义异常：交换难度计算错误"""

    pass


def render_dot_files(output_dir: str) -> None:
    """多线程渲染DOT文件"""
    dot_files: List[str] = sorted(glob.glob(os.path.join(output_dir, "exchange_*.dot")))

    with ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(render_single_dot, dot_file) for dot_file in dot_files
        ]

        for i, future in enumerate(concurrent.futures.as_completed(futures)):
            try:
                future.result()
            except Exception as e:
                logging.error(f"渲染 DOT 文件 {i} 失败: {str(e)}")


def render_single_dot(dot_file: str) -> None:
    """单个DOT文件的渲染任务"""
    output_png: str = dot_file.replace(".dot", ".png")
    os.system(f"dot -Tpng {dot_file} -o {output_png}")


def create_gif_animation(output_dir: str) -> None:
    png_files: List[str] = sorted(glob.glob(os.path.join(output_dir, "exchange_*.png")))
    images: List[Image.Image] = [
        Image.open(png).resize((800, 600), Image.LANCZOS) for png in png_files
    ]
    gif_path: str = os.path.join(output_dir, "dynamic_exchange.gif")
    images[0].save(
        gif_path,
        save_all=True,
        append_images=images[1:],
        duration=1000,
        loop=0,
        optimize=True,
    )


def exponential_exchange_difficulty(n: int, k: float = 1, base: float = 2) -> float:
    """
    计算环形交换难度的指数增长模型（含异常处理）
    """
    try:
        if n < 2:
            raise ExchangeDifficultyError(f"节点数至少为2，当前n={n}")
        if base <= 1:
            raise ExchangeDifficultyError(f"基数必须>1，当前base={base}")

        difficulty: float = k * base**n

        if math.isinf(difficulty):
            raise ExchangeDifficultyError(f"计算结果溢出（n={n}, base={base}）")

        return difficulty

    except OverflowError:
        raise ExchangeDifficultyError("数学计算溢出！请减小base或n") from None
    except TypeError as e:
        raise ExchangeDifficultyError(f"输入类型错误: {str(e)}") from None


# AI相关类型别名定义
AIModelType = Literal["deepseek", "kimi"]
OpenAIMessage = Dict[str, str]
AIResponse = Union[ChatCompletionMessage, None]
APIResponse = Union[ChatCompletion, None]


def get_product_list_from_deepseek(
    base_url: str, api_key: str, model: str, messages: List[OpenAIMessage]
) -> ChatCompletionMessage:
    """
    通过DeepSeek API获取产品列表

    Args:
        base_url: API基础地址
        api_key: 认证密钥
        model: 使用的模型名称
        messages: 消息上下文

    Returns:
        ChatCompletionMessage: OpenAI格式的响应消息对象

    Raises:
        ValueError: API调用失败时抛出
    """
    try:
        from openai import OpenAI

        client: OpenAI = OpenAI(api_key=api_key, base_url=base_url)
        response: APIResponse = client.chat.completions.create(
            model=model,
            messages=messages,
            stream=False,
        )

        if response and response.choices:
            return response.choices[0].message
        raise ValueError("Empty response from DeepSeek API")

    except Exception as e:
        logging.error(f"获取产品列表失败 (DeepSeek): {str(e)}", exc_info=True)
        raise ValueError(f"DeepSeek API调用失败: {str(e)}") from e


def get_product_list_from_kimi(
    base_url: str, api_key: str, model: str, messages: List[OpenAIMessage]
) -> ChatCompletionMessage:
    """
    通过Kimi API获取产品列表

    Args:
        base_url: API基础地址
        api_key: 认证密钥
        model: 使用的模型名称
        messages: 消息上下文

    Returns:
        ChatCompletionMessage: OpenAI格式的响应消息对象

    Raises:
        ValueError: API调用失败时抛出
    """
    try:
        client: OpenAI = OpenAI(api_key=api_key, base_url=base_url)
        response: APIResponse = client.chat.completions.create(
            model=model,
            messages=messages,
            stream=False,
        )

        if response and response.choices:
            return response.choices[0].message
        raise ValueError("Empty response from Kimi API")

    except Exception as e:
        logging.error(f"获取产品列表失败 (Kimi): {str(e)}", exc_info=True)
        raise ValueError(f"Kimi API调用失败: {str(e)}") from e


def get_product_message(
    method: AIModelType, messages: List[OpenAIMessage]
) -> ChatCompletionMessage:
    """
    获取AI生成的产品信息

    Args:
        method: AI平台选择
        messages: 消息上下文

    Returns:
        ChatCompletionMessage: 标准化响应消息

    Raises:
        ValueError: 参数错误或API调用失败
        FileNotFoundError: API密钥文件不存在
        RuntimeError: 其他运行时错误
    """
    try:
        api_key: str
        match method:
            case "deepseek":
                with open("./ai_api_key/api_key_deepseek.txt", "r") as f:
                    api_key = f.read().strip()
                return get_product_list_from_deepseek(
                    base_url="https://api.deepseek.com",
                    api_key=api_key,
                    model="deepseek-chat",
                    messages=messages,
                )

            case "kimi":
                with open("./ai_api_key/api_key_kimi.txt", "r") as f:
                    api_key = f.read().strip()
                return get_product_list_from_kimi(
                    base_url="https://api.moonshot.cn/v1",
                    api_key=api_key,
                    model="moonshot-v1-8k",
                    messages=messages,
                )

            case _:
                raise ValueError(f"不支持的AI模型: {method}")

    except FileNotFoundError as fnf_error:
        logging.critical(f"API密钥文件未找到: {str(fnf_error)}")
        raise
    except ValueError as ve:
        logging.warning(f"参数错误: {str(ve)}")
        raise
    except Exception as e:
        logging.error(f"AI生成列表数据失败: {str(e)}", exc_info=True)
        raise RuntimeError(f"AI服务不可用: {str(e)}") from e


def ai_response_to_list(list_str: str) -> List[str]:
    """
    将AI响应转换为产品列表

    Args:
        list_str: AI返回的字符串内容

    Returns:
        List[str]: 标准化产品列表

    Raises:
        ValueError: 内容格式无效时抛出
        SyntaxError: 解析语法错误时抛出
    """
    try:
        parsed_data: object = ast.literal_eval(list_str.strip())
        if isinstance(parsed_data, list):
            return [item for item in parsed_data if isinstance(item, str)]
        raise ValueError("响应内容不是有效列表格式")

    except (ValueError, SyntaxError) as e:
        logging.error(f"列表转换失败: {str(e)}\n原始内容: {list_str}")
        raise ValueError("无法解析AI响应内容") from e
    except Exception as e:
        logging.error(f"意外解析错误: {str(e)}")
        raise RuntimeError("数据处理失败") from e


if __name__ == "__main__":
    # 绘制指数型增长的交换难度曲线
    n_values: List[int] = list(range(2, 10))
    difficulties: List[float] = [
        exponential_exchange_difficulty(n, 1, math.e) for n in n_values
    ]

    plt.figure(figsize=(10, 6), dpi=100)
    plt.plot(n_values, difficulties, marker="o", label="Exchange Difficulty")

    plt.title("Exponential Growth of Exchange Difficulty")
    plt.xlabel("Number of Nodes (n)")
    plt.ylabel("Exchange Difficulty (D)")
    plt.xticks(n_values)
    plt.gca().get_yaxis().set_visible(False)  # 隐藏纵坐标
    plt.legend()
    plt.grid(True, axis="x")  # 只显示横向网格线
    plt.savefig(f"exchange_difficulty.png", bbox_inches="tight")
    plt.close()
