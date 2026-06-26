"""カードモデル"""
from __future__ import annotations
from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from src.models.game import Game


class Card:
    def __init__(self, name: str, cost: int, description: str, effect: Callable[["Game"], None]):
        self.name = name
        self.cost = cost
        self.description = description
        self.effect = effect

    def use(self, game: "Game") -> None:
        self.effect(game)

    def __repr__(self) -> str:
        return f"Card({self.name}, cost={self.cost})"


# ---- カード定義 ----

def _strike_effect(game: "Game") -> None:
    if game.enemy is None:
        return
    actual = game.enemy.take_damage(6)
    game.log(f"Strike: 敵に {actual} ダメージ！（敵HP: {game.enemy.hp}）")


def _defend_effect(game: "Game") -> None:
    game.player_block += 5
    game.log(f"Defend: ブロック +5（現在 {game.player_block}）")


def _draw_effect(game: "Game") -> None:
    game.draw_cards(2)
    game.log("Draw: カードを2枚引いた")


def make_strike() -> Card:
    return Card("Strike", 1, "敵に6ダメージ", _strike_effect)


def make_defend() -> Card:
    return Card("Defend", 1, "ブロック +5", _defend_effect)


def make_draw() -> Card:
    return Card("Draw", 1, "カードを2枚引く", _draw_effect)


def build_initial_deck() -> list[Card]:
    """初期デッキ（Strike×5, Defend×4, Draw×1）を生成する"""
    deck: list[Card] = []
    deck += [make_strike() for _ in range(5)]
    deck += [make_defend() for _ in range(4)]
    deck += [make_draw() for _ in range(1)]
    return deck
