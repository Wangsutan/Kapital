import random
from collections import defaultdict
from typing import Dict, List, Set, Tuple


class Market:
    def __init__(self) -> None:
        self.liquidity: Dict[str, float] = (
            {}
        )  # 商品流通性，格式：{商品名称: 流通性评分}

    def set_liquidity(self, good: str, change: float) -> None:
        """设置商品流通性"""
        if good not in self.liquidity:
            self.liquidity[good] = 0.0
        self.liquidity[good] += change

    def change_liquidity(self, one: "MarketAgent", another: "MarketAgent") -> None:
        """执行交易，更新商品流通性"""
        # 获取所有库存和需求商品
        goods_inventory_all: Set[str] = set(one.inventory.keys()).union(
            set(another.inventory.keys())
        )
        goods_need_all: Set[str] = set(one.need.keys()).union(set(another.need.keys()))

        # 找出双方可以交易的商品
        tradable_goods_one: Set[str] = set(one.inventory.keys()).intersection(
            set(another.need.keys())
        )
        tradable_goods_another: Set[str] = set(one.need.keys()).intersection(
            set(another.inventory.keys())
        )
        tradable_goods_all: Set[str] = tradable_goods_one.union(tradable_goods_another)

        # 更新商品流通性
        for good in goods_inventory_all:
            if good in tradable_goods_all:
                self.set_liquidity(good, 1.0)  # 可交易的商品流通性增加
            else:
                self.set_liquidity(good, -1.0)  # 不可交易的商品流通性减少

        for good in goods_need_all:
            if good in tradable_goods_all:
                self.set_liquidity(good, 0.2)  # 可交易的需求商品流通性增加
            else:
                self.set_liquidity(good, 1.0)  # 不可交易的需求商品流通性增加


class MarketAgent:
    def __init__(
        self,
        name: str,
        goods_list: List[str],
        inventory_prob: Dict[str, float],
        need_prob: Dict[str, float],
    ) -> None:
        self.name: str = name
        self.goods_list: List[str] = goods_list  # 商品列表
        self.inventory_prob: Dict[str, float] = inventory_prob  # 商品出现在库存中的概率
        self.need_prob: Dict[str, float] = need_prob  # 商品出现在需求中的概率
        self.inventory: Dict[str, int] = defaultdict(
            int
        )  # 库存，格式：{商品名称: 数量}
        self.need: Dict[str, int] = defaultdict(int)  # 需求，格式：{商品名称: 数量}

    def generate_random_goods(self) -> None:
        """随机生成库存和需求商品"""
        self.inventory.clear()  # 清空当前库存
        self.need.clear()  # 清空当前需求

        for good in self.goods_list:
            # 随机决定商品是出现在库存还是需求中
            random_location: str = random.choice(["inventory", "need"])
            if random_location == "inventory":
                if random.random() < self.inventory_prob.get(good, 0.0):
                    self.inventory[good] += 1
            elif random_location == "need":
                if random.random() < self.need_prob.get(good, 0.0):
                    self.need[good] += 1


def simulate_trading(
    market: Market, agents: List[MarketAgent], trade_times: int
) -> None:
    """模拟交易"""
    # 随机选择两个不同的市场主体进行交易
    for _ in range(trade_times):
        one, another = random.sample(agents, 2)
        one.generate_random_goods()
        another.generate_random_goods()
        market.change_liquidity(one, another)


if __name__ == "__main__":
    # 示例商品列表和概率
    goods_list: List[str] = ["贝壳", "小麦", "铁", "木材", "上衣"]
    inventory_prob: Dict[str, float] = {
        "贝壳": 0.6,
        "小麦": 0.3,
        "铁": 0.2,
        "木材": 0.2,
        "上衣": 0.2,
    }  # 商品出现在库存中的概率
    need_prob: Dict[str, float] = {
        "贝壳": 0.6,
        "小麦": 0.3,
        "铁": 0.2,
        "木材": 0.2,
        "上衣": 0.2,
    }  # 商品出现在需求中的概率

    # 创建市场
    market: Market = Market()

    # 随机生成市场主体数量
    num_agents: int = random.randint(3, 10)
    agents: List[MarketAgent] = [
        MarketAgent(f"Agent{i + 1}", goods_list, inventory_prob, need_prob)
        for i in range(num_agents)
    ]

    # 模拟交易
    print("开始模拟交易。")
    trade_times: int = 100000
    print(f"交易次数： {trade_times}")
    simulate_trading(market, agents, trade_times)

    # 打印最终商品流通性（按值排序）
    sorted_liquidity: List[Tuple[str, float]] = sorted(
        market.liquidity.items(), key=lambda x: x[1], reverse=True
    )
    print(f"\n最终的商品流通性（按值排序）:\n{sorted_liquidity}")
