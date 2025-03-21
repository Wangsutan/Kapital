#!/bin/bash

echo "生成 TOML 文件……"
cd gen_complete
cargo run
if [ $? -ne 0 ]; then
    echo "生成 TOML 文件失败，请检查错误。"
    exit 1
fi
cd ..
echo "TOML 文件生成完成。"

echo "检查 TOML 文件……"
cd check_data
cargo run
if [ $? -ne 0 ]; then
    echo "检查 TOML 文件失败，请检查错误。"
    exit 1
fi
cd ..
echo "TOML 文件检查完成。"

echo "生成 Graphviz 文件……"
cd gen_graphviz
cargo run
if [ $? -ne 0 ]; then
    echo "生成 Graphviz 文件失败，请检查错误。"
    exit 1
fi
cd ..
echo "Graphviz 文件生成完成。"

echo "检查 Graphviz 文件……"
cd check_graph
cargo run
if [ $? -ne 0 ]; then
    echo "检查 Graphviz 文件失败，请检查错误。"
    exit 1
fi
cd ..
echo "Graphviz 文件检查完成。"

echo "生成 3D 可视化文件 (HTML)……"
python gen_3d_plotly.py
if [ $? -ne 0 ]; then
    echo "生成 3D 可视化文件 (HTML) 失败，请检查错误。"
    exit 1
fi
echo "3D 可视化文件 (HTML) 生成完成。"

echo "生成 3D 图形文件 (OBJ/STL/PLY)……"
python gen_3d_pyvista.py
if [ $? -ne 0 ]; then
    echo "生成 3D 图形文件 (OBJ/STL/PLY) 失败，请检查错误。"
    exit 1
fi
echo "3D 图形文件 (OBJ/STL/PLY) 生成完成。"

echo "所有步骤已完成！"
