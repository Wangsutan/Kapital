import value_form_process_simulator as vfps
from typing import List, Dict


historical_periods: Dict[str, Dict[str, str]] = {
    "primitive_society": {
        "prompt": "生成一个关于产品的Python列表，这些产品数量为5，属于人类社会早期的产品，用于交换。输出结果只要列表，其他任何东西都不要。",
        "output_dir": "primitive_society",
    },
    "feudal_society": {
        "prompt": "生成一个关于产品的Python列表，这些产品数量为10，属于封建社会的产品，用于交换。要根据之前历史时期的情况，对商品做一定的增删改动。输出结果只要列表，其他任何东西都不要。",
        "output_dir": "feudal_society",
    },
    "capitalist_society": {
        "prompt": "生成一个关于产品的Python列表，这些产品数量为15，属于资本主义社会的产品，用于交换。要根据之前历史时期的情况，对商品做一定的增删改动。输出结果只要列表，其他任何东西都不要。",
        "output_dir": "capitalist_society",
    },
}

# AI所用提示词和回复等信息
messages: List[vfps.OpenAIMessage] = []

# 文件路径
dir_father: str = "./datas_dynamic_graphs"
# 帧数
time_steps: int = 12

for period, info in historical_periods.items():
    output_dir: str = f"{dir_father}/{info['output_dir']}"
    prompt: str = info["prompt"]
    msg_ask: vfps.OpenAIMessage = {"role": "user", "content": prompt}
    messages.append(msg_ask)

    try:
        msg_product: vfps.ChatCompletionMessage = vfps.get_product_message(
            "deepseek", messages
        )
        messages.append(msg_product)
        products: List[str] = vfps.ai_response_to_list(msg_product.content)
    except Exception as e:
        print(f"Failed to get products for {period}: {str(e)}")
        continue
    vfps.generate_dot_series_with_layout(output_dir, time_steps, products)
    vfps.execute_plot_tasks()
    vfps.render_dot_files(output_dir)
    vfps.create_gif_animation(output_dir)
