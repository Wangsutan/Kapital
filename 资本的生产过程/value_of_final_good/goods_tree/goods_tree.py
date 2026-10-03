import pandas as pd
import graphviz
from collections import defaultdict
from typing import Dict, List, Set, Tuple, DefaultDict


dependency_tree: DefaultDict[str, List[str]] = defaultdict(list)
value_cache: Dict[str, float] = {}
node_cache: Set[str] = set()
non_commodity_nodes: DefaultDict[str, List[Tuple[str, float, float]]] = defaultdict(
    list
)  # 存储无需递归节点信息：{父节点: [(子节点, 数量, 单价)]}


def search(good_before: str, goods_x: List[str]) -> None:
    for good_current in goods_x:
        print(f"当前处理节点: {good_current}")

        if good_current in node_cache:
            print(f"跳过已处理节点: {good_current}")
            continue
        node_cache.add(good_current)

        # 读取生产要素表
        df: pd.DataFrame = pd.read_excel(
            good_current + "生产要素表.xlsx", index_col="生产要素"
        )
        globals()["df_" + good_current] = df

        # 识别无需递归节点并存储
        non_commodity: List[Tuple[str, float, float]] = []
        for elem, row in df.iterrows():
            if row["单价"] != "x":  # 无需递归节点
                non_commodity.append((elem, row["数量"], row["单价"]))

        if non_commodity:
            non_commodity_nodes[good_current] = non_commodity
            print(f"发现无需递归节点: {[x[0] for x in non_commodity]}")

        # 获取需要递归处理的节点
        goods_next: List[str] = df.query("单价 == 'x'").index.tolist()

        if goods_next:
            print(f"发现上级节点需递归: {goods_next}")
            dependency_tree[good_current].extend(goods_next)
            search(good_current, goods_next)
        else:
            print("无上级节点需递归")

        # 计算节点价值（包括无需递归节点）
        total_value: float = 0.0
        for elem, row in df.iterrows():
            if elem in value_cache:  # 节点
                total_value += row["数量"] * value_cache[elem]
            elif row["单价"] != "x":  # 无需递归节点
                total_value += row["数量"] * row["单价"]

        value_cache[good_current] = total_value

        # 更新父节点表中的单价
        if good_before != good_current:
            globals()["df_" + good_before].loc[good_current, "单价"] = total_value

        print(f"{good_current}价值: {total_value:.6f}\n")


def draw_dependency_tree() -> None:
    dot: graphviz.Digraph = graphviz.Digraph(comment="商品价值依赖树", format="png")
    dot.attr(rankdir="TB", size="12,8", fontname="Microsoft YaHei")

    # 添加所有节点
    for node in node_cache:
        if node in value_cache:  # 需递归节点
            dot.node(
                node,
                f"{node}\\n价值: {value_cache[node]:.6f}",
                shape="box",
                style="filled",
                fillcolor="lightblue",
            )
        else:  # 无需递归节点
            # 查找首次出现该节点的父节点和单价
            for parent, elems in non_commodity_nodes.items():
                for name, qty, price in elems:
                    if name == node:
                        dot.node(
                            node,
                            f"{node}\\n单价: {price:.6f}",
                            shape="ellipse",
                            style="filled",
                            fillcolor="#FFD700",
                        )
                        break

    # 添加节点间的依赖关系
    for parent, children in dependency_tree.items():
        for child in children:
            df: pd.DataFrame = globals().get(f"df_{parent}")
            if df is not None and child in df.index:
                qty = df.loc[child, "数量"]
                contribution: float = qty * value_cache[child]
                dot.edge(
                    child,
                    parent,
                    label=f"{qty}×{value_cache[child]:.6f}\n= {contribution:.6f}",
                )

    # 添加需递归节点到其他节点的依赖关系
    for parent, elems in non_commodity_nodes.items():
        for name, qty, price in elems:
            contribution = qty * price
            dot.edge(
                name,
                parent,
                label=f"{qty}×{price:.6f}\n= {contribution:.6f}",
                style="dashed",
                color="gray",
            )

    # 添加图例
    with dot.subgraph(name="cluster_legend") as legend:
        legend.attr(
            label="图例", style="rounded,filled", fillcolor="#F0F0F0", fontsize="12"
        )
        legend.node(
            "commodity",
            "需递归生产要素节点",
            shape="box",
            style="filled",
            fillcolor="lightblue",
        )
        legend.node(
            "resource",
            "无需递归生产要素节点",
            shape="ellipse",
            style="filled",
            fillcolor="#FFD700",
        )
        legend.node("dep1", "需递归生产要素依赖关系", shape="plaintext")
        legend.node(
            "dep2",
            "无需递归生产要素依赖",
            style="dashed",
            color="gray",
            shape="plaintext",
        )

    # 渲染并保存图像
    output_file: str = dot.render("commodity_dependency_tree", view=True)
    print(f"依赖树已保存为: {output_file}")


if __name__ == "__main__":
    good_before: str = "茶叶蛋"
    goods_x: List[str] = ["茶叶蛋"]
    search(good_before, goods_x)
    draw_dependency_tree()
