import pygraphviz as pgv
import pyvista as pv
import random
import numpy as np
import os
from typing import Dict, Tuple, List, Any

# 配置参数
coord_range: Dict[str, Tuple[int, int]] = {
    "x": (-8, 8),
    "y": (-8, 8),
    "z": (-8, 8),
}
node_radius: float = 0.6  # 节点半径
edge_radius: float = 0.1  # 减小边的半径
arrow_radius: float = 0.2  # 箭头半径
arrow_length: float = 0.5  # 箭头长度


def get_node_color(product_names: List[str]) -> List[Tuple[float, float, float]]:
    """根据商品名称返回节点颜色"""
    colors: List[Tuple[float, float, float]] = []
    for name in product_names:
        if name == "金":
            colors.append((1.0, 0.843, 0.0))  # 金色节点 (RGB: 255, 215, 0)
        else:
            # 随机生成其他颜色 (归一化到 [0, 1] 范围)
            colors.append((
                random.random(),
                random.random(),
                random.random()
            ))
    return colors


def generate_3d_graph(dot_file_path: str) -> None:
    # 读取 DOT 文件
    graph: pgv.AGraph = pgv.AGraph(dot_file_path)
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

    # 获取节点颜色
    product_names = [str(node) for node in nodes]
    node_colors = get_node_color(product_names)

    # 创建 PyVista 场景
    plotter = pv.Plotter()

    # 添加节点（球体）
    spheres = []
    for (node_name, pos), color in zip(node_positions.items(), node_colors):
        sphere = pv.Sphere(radius=node_radius, center=pos)
        plotter.add_mesh(sphere, color=color, label=node_name)
        spheres.append(sphere)

        # 添加节点标签
        label_pos = (pos[0], pos[1], pos[2] + node_radius * 1.5)  # 将标签位置稍微抬高
        plotter.add_point_labels(
            [label_pos],  # 标签位置
            [node_name],  # 标签文本
            font_size=20,  # 字体大小
            font_family="arial",  # 字体
            text_color="gray",  # 文本颜色
            shape_opacity=0.0,  # 背景透明度
            name=f"label_{node_name}",  # 标签名称
        )

    # 添加边（圆柱体）和箭头（锥体）
    cylinders = []
    arrows = []
    for edge in edges:
        source: str = str(edge[0])
        target: str = str(edge[1])
        src_pos: np.ndarray = np.array(node_positions[source])
        tgt_pos: np.ndarray = np.array(node_positions[target])

        direction: np.ndarray = tgt_pos - src_pos
        length: float = np.linalg.norm(direction)
        if length > 0:
            direction_normalized = direction / length

            # 计算圆柱体的长度和中心
            cylinder_length = length - node_radius * 2 - arrow_length
            if cylinder_length > 0:
                # 缩短圆柱体的起始位置，使其从源节点中心开始，减去箭头长度的一半
                cylinder_start = src_pos + direction_normalized * (node_radius + arrow_length / 2)
                cylinder_end = tgt_pos - direction_normalized * (node_radius + arrow_length / 2)
                cylinder_center = (cylinder_start + cylinder_end) / 2
                cylinder = pv.Cylinder(
                    center=cylinder_center,
                    direction=direction_normalized,
                    radius=edge_radius,  # 减小边的半径
                    height=cylinder_length,
                    resolution=50  # 提高分辨率
                )
                plotter.add_mesh(cylinder, color="gray", opacity=0.3, line_width=1)  # 半透明效果
                cylinders.append(cylinder)

            # 添加箭头（锥体）
            arrow_center = tgt_pos - direction_normalized * (node_radius + arrow_length / 2)
            arrow = pv.Cone(
                center=arrow_center,
                direction=direction_normalized,
                radius=arrow_radius,
                height=arrow_length,
                resolution=50  # 提高分辨率
            )
            plotter.add_mesh(arrow, color="gray", opacity=0.3)  # 半透明效果
            arrows.append(arrow)

    # 合并所有网格
    combined_mesh = spheres[0]
    for sphere in spheres[1:]:
        combined_mesh = combined_mesh.merge(sphere)
    for cylinder in cylinders:
        combined_mesh = combined_mesh.merge(cylinder)
    for arrow in arrows:
        combined_mesh = combined_mesh.merge(arrow)

    # 保存为文件
    output_dir: str = os.path.dirname(dot_file_path)
    for file_format in ['obj', 'stl', 'ply']:
        output_path: str = os.path.join(output_dir, f"{graph_name}.{file_format}")
        combined_mesh.save(output_path)
        print(f"已生成 {file_format.upper()} 文件: {output_path}")

    # 显示 3D 场景
    # plotter.show()

    graph.close()


# 遍历当前目录下的所有.dot文件
def process_dot_files(directory: str = "./graphs_generated") -> None:
    for filename in os.listdir(directory):
        if filename.endswith(".dot"):
            file_path: str = os.path.join(directory, filename)
            print(f"正在处理文件: {file_path}")
            try:
                generate_3d_graph(file_path)
            except Exception as e:
                print(f"处理文件 {file_path} 时出错: {e}")


# 主程序入口
if __name__ == "__main__":
    process_dot_files()
