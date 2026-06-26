"""マップノードモデル"""
from __future__ import annotations
from typing import Optional

NODE_BATTLE = "battle"
NODE_ELITE = "elite"
NODE_REST = "rest"
NODE_BOSS = "boss"

NODE_LABELS = {
    NODE_BATTLE: "通常敵",
    NODE_ELITE: "強敵",
    NODE_REST: "休憩",
    NODE_BOSS: "ボス",
}


class Node:
    def __init__(self, node_type: str, next_nodes: Optional[list["Node"]] = None):
        self.type = node_type
        self.next_nodes: list["Node"] = next_nodes or []

    @property
    def label(self) -> str:
        return NODE_LABELS.get(self.type, self.type)

    def __repr__(self) -> str:
        return f"Node({self.type})"


def build_map() -> Node:
    """
    固定マップを生成する。

    通常敵
    ↓
    分岐
    ├ 通常敵
    └ 強敵
    ↓
    休憩
    ↓
    ボス
    """
    boss = Node(NODE_BOSS)
    rest = Node(NODE_REST, next_nodes=[boss])
    battle2 = Node(NODE_BATTLE, next_nodes=[rest])
    elite = Node(NODE_ELITE, next_nodes=[rest])
    battle1 = Node(NODE_BATTLE, next_nodes=[battle2, elite])
    return battle1
