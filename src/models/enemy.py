"""敵モデル"""
from __future__ import annotations
import random
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.models.game import Game


class Enemy:
    def __init__(self, name: str, hp: int, attack_power: int, block_power: int):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.block = 0
        self.attack_power = attack_power
        self.block_power = block_power

    @property
    def is_alive(self) -> bool:
        return self.hp > 0

    def take_damage(self, damage: int) -> int:
        """ダメージを受ける。実際に受けたダメージ量を返す"""
        actual = max(0, damage - self.block)
        self.block = max(0, self.block - damage)
        self.hp = max(0, self.hp - actual)
        return actual

    def act(self, game: "Game") -> None:
        """敵の行動（ランダム：攻撃 or 防御）"""
        action = random.choice(["attack", "defend"])
        if action == "attack":
            self._do_attack(game)
        else:
            self._do_defend(game)

    def _do_attack(self, game: "Game") -> None:
        damage = max(0, self.attack_power - game.player_block)
        game.player_block = max(0, game.player_block - self.attack_power)
        game.player_hp -= damage
        game.log(f"{self.name}: 攻撃！ プレイヤーに {damage} ダメージ")

    def _do_defend(self, game: "Game") -> None:
        self.block += self.block_power
        game.log(f"{self.name}: 防御！ ブロック +{self.block_power}（現在 {self.block}）")

    def reset_block(self) -> None:
        self.block = 0


# ---- 敵ファクトリ ----

def make_normal_enemy() -> Enemy:
    return Enemy("スライム", hp=40, attack_power=8, block_power=4)


def make_elite_enemy() -> Enemy:
    return Enemy("ゴブリンエリート", hp=60, attack_power=12, block_power=6)


def make_boss_enemy() -> Enemy:
    return Enemy("ダークロード（ボス）", hp=80, attack_power=15, block_power=8)
