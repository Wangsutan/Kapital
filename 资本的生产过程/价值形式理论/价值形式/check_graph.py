import networkx as nx
import os
from typing import List, Tuple, Dict, Set


def validate_graph(file_path: str) -> None:
    """
    验证价值形式理论的图文件。
    """
    # 读取DOT文件
    G = nx.drawing.nx_agraph.read_dot(file_path)

    print(f"有无自身交换: {check_self_loops(G)}")
    print(f"有无重复交换: {check_duplicate_edges(G)}")

    is_complete, missing_edges = check_complete_graph(G)
    print(f"每个商品是否直接交换所有其他节点: {is_complete}")
    if not is_complete:
        print("\n=== 缺失的边 ===")
        for node, missing in missing_edges:
            print(f"节点 `{node}` 未连接到: {missing}")

    currencies: List[str] = find_currencies(G)
    print(f"货币形式数量: {len(currencies)}")
    if currencies:
        print("货币形式为: " + ", ".join(currencies))


def check_self_loops(G: nx.DiGraph) -> bool:
    """
    检查图中是否存在自环（商品是否与自己交换）。
    """
    self_loops: List[Tuple[str, str]] = list(nx.selfloop_edges(G))
    has_self_loop: bool = len(self_loops) > 0
    return has_self_loop


def check_duplicate_edges(G: nx.DiGraph) -> bool:
    """
    检查图中是否存在重复边（一种商品是否重复交换别的商品）。
    """
    edge_count: Dict[Tuple[str, str], int] = {}
    duplicates: List[Tuple[str, str]] = []
    for u, v in G.edges():
        key: Tuple[str, str] = (u, v)
        if key in edge_count:
            duplicates.append(key)
        else:
            edge_count[key] = 1
    has_duplicates: bool = len(duplicates) > 0
    return has_duplicates


def check_complete_graph(G: nx.DiGraph) -> Tuple[bool, List[Tuple[str, List[str]]]]:
    """
    检查图是否是完全图（每个节点是否直接连接所有其他节点）。
    """
    nodes: List[str] = list(G.nodes())
    G_clean: nx.DiGraph = nx.DiGraph()
    G_clean.add_edges_from(set(G.edges()))
    is_complete: bool = True
    missing_edges: List[Tuple[str, List[str]]] = []
    for node in nodes:
        out_edges: Set[str] = set(G_clean.successors(node))
        expected: Set[str] = set(nodes) - {node}  # 期望连接的节点
        missing: Set[str] = expected - out_edges
        if missing:
            is_complete = False
            missing_edges.append((node, list(missing)))

    return is_complete, missing_edges


def find_currencies(G: nx.DiGraph) -> List[str]:
    """
    查找图中的货币形式（一般等价物）。
    货币形式的定义是：出度为 0，入度为 n-1（n 为节点总数）。
    """
    currencies: List[str] = []
    total_nodes: int = len(G.nodes())
    total_nodes_min: int = 3
    for node in G.nodes():
        if (
            G.out_degree(node) <= 3
            and G.in_degree(node) == total_nodes - 1
            and total_nodes > total_nodes_min
        ):
            currencies.append(node)
    return currencies


# 遍历当前目录下的所有.dot文件
def process_dot_files(directory: str = "./graphs_generated") -> None:
    """
    遍历指定目录下的所有 .dot 文件，并对其进行验证。
    """
    for filename in os.listdir(directory):
        if filename.endswith(".dot"):
            file_path: str = os.path.join(directory, filename)
            print(f"\n正在处理文件: {file_path}")
            try:
                validate_graph(file_path)
            except Exception as e:
                print(f"处理文件 {file_path} 时出错: {e}")


if __name__ == "__main__":
    process_dot_files()  # 默认处理当前目录
