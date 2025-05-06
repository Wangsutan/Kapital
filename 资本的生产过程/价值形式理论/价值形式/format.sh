#!/bin/bash

export PATH="$HOME/.cargo/bin:$PATH"
export RUST_LOG=warn

# 格式化并检查 .toml 文件（排除 Cargo.toml）
rg -g "*.toml" -e "" --files --glob "!.toml" | while read -r file; do
    taplo format "$file" || exit 1
    taplo lint "$file" || exit 1
done

# 定义 Rust 子项目目录
RUST_PROJECTS=("check_data" "check_graph" "gen_graphviz" "gen_complete")

# 并行格式化并检查每个 Rust 子项目
for project in "${RUST_PROJECTS[@]}"; do
  (
    cd "$project" || { echo "Failed to enter $project"; exit 1; }
    cargo fmt --quiet || exit 1
    cargo check --quiet || exit 1
  ) &
done

# 等待所有子进程完成
wait

# 检查是否有子任务失败
if [[ $? -ne 0 ]]; then
  echo "Some Rust tasks failed. Stopping."
  exit 1
fi

# 格式化 Python 代码
black *.py > /dev/null || exit 1

# 检查 Python 类型
mypy *.py --config-file mypy.ini > /dev/null || exit 1

# 检查 Python 代码风格
flake8 *.py || exit 1
