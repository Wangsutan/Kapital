import pygraphviz as pgv
import plotly.graph_objects as go
import random
import numpy as np
import os
from typing import Dict, Tuple, List, Any

# 配置参数（新增节点半径参数）
coord_range: Dict[str, Tuple[int, int]] = {
    "x": (-8, 8),
    "y": (-8, 8),
    "z": (-8, 8),
}  # 扩大坐标范围
node_radius: float = 0.6  # 对应marker.size=10的实际半径


# 提取颜色逻辑（新增函数）
def get_node_color(product_names: List[str]) -> List[str]:
    """根据商品名称返回节点颜色"""
    colors: List[str] = []
    for name in product_names:
        if name == "金":
            colors.append("gold")  # 金色节点
        else:
            # 随机生成其他颜色
            colors.append(
                f"rgb({random.randint(0, 255)}, {random.randint(0, 255)}, {random.randint(0, 255)})"
            )
    return colors


def visualize_graph(dot_file_path: str) -> None:
    # 读取 DOT 文件
    graph: pgv.AGraph = pgv.AGraph(dot_file_path)

    # 提取文件名作为图形标题
    graph_name: str = os.path.splitext(os.path.basename(dot_file_path))[0]

    # 提取节点和边
    nodes: List[Any] = graph.nodes()
    edges: List[Any] = graph.edges()

    # 自动生成节点位置
    node_positions: Dict[str, Tuple[float, float, float]] = {}
    for node in nodes:
        node_name: str = str(node)
        node_positions[node_name] = (
            random.uniform(*coord_range["x"]),
            random.uniform(*coord_range["y"]),
            random.uniform(*coord_range["z"]),
        )

    # 生成商品名称列表（优化点）
    product_names: List[str] = list(node_positions.keys())

    # 创建节点轨迹（使用提取的颜色逻辑）
    node_trace: go.Scatter3d = go.Scatter3d(
        x=[pos[0] for pos in node_positions.values()],
        y=[pos[1] for pos in node_positions.values()],
        z=[pos[2] for pos in node_positions.values()],
        mode="markers+text",
        marker=dict(
            size=10,  # 保持原尺寸
            color=get_node_color(product_names),  # 使用提取的颜色逻辑
            line=dict(width=2, color="DarkSlateGrey"),
        ),
        text=product_names,  # 使用商品名称列表
        textposition="top center",
    )

    # 创建边和箭头（关键修改部分）
    edge_trace: List[go.Scatter3d | go.Cone] = []
    for edge in edges:
        source: str = str(edge[0])
        target: str = str(edge[1])
        src_pos: Tuple[float, float, float] = node_positions[source]
        tgt_pos: Tuple[float, float, float] = node_positions[target]

        # ========== 表面坐标计算 ==========
        dx, dy, dz = (
            tgt_pos[0] - src_pos[0],
            tgt_pos[1] - src_pos[1],
            tgt_pos[2] - src_pos[2],
        )
        distance: float = np.sqrt(dx**2 + dy**2 + dz**2)
        if distance > 0:
            ux, uy, uz = dx / distance, dy / distance, dz / distance
            start_point: List[float] = [
                src_pos[0] + ux * node_radius,
                src_pos[1] + uy * node_radius,
                src_pos[2] + uz * node_radius,
            ]
            end_point: List[float] = [
                tgt_pos[0] - ux * node_radius,
                tgt_pos[1] - uy * node_radius,
                tgt_pos[2] - uz * node_radius,
            ]
        else:
            start_point, end_point = src_pos, tgt_pos
        # ========== 修改结束 ==========

        # 边的主体（使用新坐标）
        edge_trace.append(
            go.Scatter3d(
                x=[start_point[0], end_point[0]],
                y=[start_point[1], end_point[1]],
                z=[start_point[2], end_point[2]],
                mode="lines",
                line=dict(color="black", width=2),
            )
        )

        # 箭头部分（关键修改）
        edge_trace.append(
            go.Cone(
                x=[end_point[0]],  # 使用表面坐标
                y=[end_point[1]],
                z=[end_point[2]],
                u=[ux * 0.7] if distance > 0 else [0],  # 缩短箭头向量
                v=[uy * 0.7] if distance > 0 else [0],
                w=[uz * 0.7] if distance > 0 else [0],
                sizemode="absolute",
                sizeref=0.3,  # 调整箭头大小（值越小箭头越大）
                showscale=False,
                colorscale=[[0, "black"], [1, "black"]],
                anchor="tip",  # 关键参数：箭头尖对准坐标点
            )
        )

    # 保持原有布局配置
    fig: go.Figure = go.Figure(data=edge_trace + [node_trace])
    fig.update_layout(
        title={
            "text": f"3D 可视化: {graph_name}",  # 标题文本
            "y": 0.95,  # 标题垂直位置（0-1，1为顶部）
            "x": 0.5,  # 标题水平位置（0-1，0.5为居中）
            "xanchor": "center",  # 标题水平对齐方式
            "yanchor": "top",  # 标题垂直对齐方式
            "font": dict(size=20),  # 标题字体大小
        },
        scene=dict(
            xaxis=dict(nticks=4, range=coord_range["x"]),
            yaxis=dict(nticks=4, range=coord_range["y"]),
            zaxis=dict(nticks=4, range=coord_range["z"]),
            aspectratio=dict(x=1, y=1, z=1),
            camera=dict(up=dict(x=0, y=0, z=1), eye=dict(x=1.5, y=1.5, z=0.5)),
        ),
        margin=dict(l=0, r=0, b=0, t=40),  # 增加顶部边距
        dragmode="orbit",
    )

    # 保存为 HTML 文件
    output_html_path: str = os.path.join(
        os.path.dirname(dot_file_path), f"{graph_name}.html"
    )
    fig.write_html(output_html_path)
    print(f"已生成 HTML 文件: {output_html_path}")

    graph.close()


# 遍历当前目录下的所有.dot文件
def process_dot_files(directory: str = "./graphs_generated") -> None:
    for filename in os.listdir(directory):
        if filename.endswith(".dot"):
            file_path: str = os.path.join(directory, filename)
            print(f"正在处理文件: {file_path}")
            try:
                visualize_graph(file_path)
            except Exception as e:
                print(f"处理文件 {file_path} 时出错: {e}")


# 主程序入口
if __name__ == "__main__":
    process_dot_files()  # 默认处理当前目录
