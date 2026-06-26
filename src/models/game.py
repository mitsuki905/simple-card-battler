"""ゲームモデル（状態管理・戦闘ロジック）"""
from __future__ import annotations
import random
from typing import Optional, Callable

from src.models.card import Card, build_initial_deck
from src.models.enemy import Enemy
from src.models.map_node import Node, build_map, NODE_BATTLE, NODE_ELITE, NODE_REST, NODE_BOSS
from src.models.enemy import make_normal_enemy, make_elite_enemy, make_boss_enemy

HAND_SIZE = 5
MAX_ENERGY = 3
REST_HEAL = 15


class Game:
    def __init__(self):
        # プレイヤー
        self.player_hp: int = 50
        self.player_max_hp: int = 50
        self.player_block: int = 0
        self.energy: int = MAX_ENERGY

        # 敵
        self.enemy: Optional[Enemy] = None

        # デッキ管理
        self.deck: list[Card] = []
        self.hand: list[Card] = []
        self.discard: list[Card] = []

        # マップ
        self.current_node: Optional[Node] = None

        # ログ
        self._log_lines: list[str] = []
        self._log_callback: Optional[Callable[[str], None]] = None

        # 状態
        self.in_battle: bool = False
        self.game_over: bool = False
        self.game_clear: bool = False

        self._init_game()

    # ------------------------------------------------------------------ #
    # 初期化
    # ------------------------------------------------------------------ #

    def _init_game(self) -> None:
        deck = build_initial_deck()
        random.shuffle(deck)
        self.deck = deck
        self.current_node = build_map()

    # ------------------------------------------------------------------ #
    # ログ
    # ------------------------------------------------------------------ #

    def set_log_callback(self, callback: Callable[[str], None]) -> None:
        self._log_callback = callback

    def log(self, message: str) -> None:
        self._log_lines.append(message)
        if self._log_callback:
            self._log_callback(message)

    def get_logs(self) -> list[str]:
        return list(self._log_lines)

    def clear_logs(self) -> None:
        self._log_lines.clear()

    # ------------------------------------------------------------------ #
    # デッキ操作
    # ------------------------------------------------------------------ #

    def draw_cards(self, count: int = 1) -> None:
        for _ in range(count):
            if not self.deck:
                if not self.discard:
                    self.log("山札も捨て札も空です")
                    return
                random.shuffle(self.discard)
                self.deck = self.discard[:]
                self.discard.clear()
                self.log("捨て札をシャッフルして山札に戻した")
            if self.deck:
                card = self.deck.pop(0)
                self.hand.append(card)

    def _fill_hand(self) -> None:
        needed = HAND_SIZE - len(self.hand)
        if needed > 0:
            self.draw_cards(needed)

    # ------------------------------------------------------------------ #
    # ノード処理
    # ------------------------------------------------------------------ #

    def enter_node(self, node: Node) -> None:
        self.current_node = node
        self.log(f"--- {node.label} に進んだ ---")

        if node.type == NODE_REST:
            self._do_rest()
        elif node.type in (NODE_BATTLE, NODE_ELITE, NODE_BOSS):
            self._start_battle(node.type)

    def _do_rest(self) -> None:
        healed = min(REST_HEAL, self.player_max_hp - self.player_hp)
        self.player_hp += healed
        self.log(f"休憩：HP +{healed}（現在 {self.player_hp}）")

    # ------------------------------------------------------------------ #
    # 戦闘
    # ------------------------------------------------------------------ #

    def _start_battle(self, node_type: str) -> None:
        if node_type == NODE_ELITE:
            self.enemy = make_elite_enemy()
        elif node_type == NODE_BOSS:
            self.enemy = make_boss_enemy()
        else:
            self.enemy = make_normal_enemy()

        self.in_battle = True
        self.log(f"{self.enemy.name} が現れた！（HP {self.enemy.hp}）")
        self.start_player_turn()

    def start_player_turn(self) -> None:
        """プレイヤーターン開始処理"""
        self.energy = MAX_ENERGY
        self.player_block = 0          # ブロックはターン開始時にリセット
        self._fill_hand()
        self.log(f"--- プレイヤーのターン（エネルギー {self.energy}）---")

    def play_card(self, card: Card) -> bool:
        """手札からカードを使用する。成功したら True を返す"""
        if card not in self.hand:
            return False
        if self.energy < card.cost:
            self.log(f"エネルギー不足（必要 {card.cost}、現在 {self.energy}）")
            return False

        self.energy -= card.cost
        self.hand.remove(card)
        card.use(self)
        self.discard.append(card)

        # 敵の死亡チェック
        if self.enemy and self.enemy.hp <= 0:
            self._on_enemy_defeated()

        return True

    def end_player_turn(self) -> None:
        """ターン終了 → 敵行動"""
        if not self.in_battle:
            return

        # 手札を全て捨て札へ
        self.discard.extend(self.hand)
        self.hand.clear()

        self.log("--- 敵のターン ---")
        if self.enemy and self.enemy.is_alive:
            self.enemy.act(self)
            self.enemy.reset_block()

        # プレイヤー死亡チェック
        if self.player_hp <= 0:
            self._on_player_defeated()
            return

        # 次のプレイヤーターン
        self.start_player_turn()

    def _on_enemy_defeated(self) -> None:
        self.in_battle = False
        self.log(f"{self.enemy.name} を倒した！")

        if self.current_node and self.current_node.type == NODE_BOSS:
            self.game_clear = True
            self.log("🎉 ゲームクリア！おめでとう！")
        else:
            self.log("マップに戻る...")

    def _on_player_defeated(self) -> None:
        self.in_battle = False
        self.game_over = True
        self.log("💀 ゲームオーバー...")

    # ------------------------------------------------------------------ #
    # 状態参照
    # ------------------------------------------------------------------ #

    @property
    def player_alive(self) -> bool:
        return self.player_hp > 0

    @property
    def next_nodes(self) -> list[Node]:
        if self.current_node:
            return self.current_node.next_nodes
        return []
