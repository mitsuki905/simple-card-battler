"""戦闘画面ウィジェット"""
from __future__ import annotations
from typing import TYPE_CHECKING

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QTextEdit, QFrame, QScrollArea,
)
from PySide6.QtCore import Qt, Signal

if TYPE_CHECKING:
    from src.models.game import Game
from src.models.card import Card


class BattleScreen(QWidget):
    """戦闘画面"""

    # 戦闘終了シグナル（勝利 or 敗北）
    battle_ended = Signal(bool)  # True=勝利, False=敗北

    def __init__(self, game: "Game", parent: QWidget | None = None):
        super().__init__(parent)
        self.game = game
        self._setup_ui()
        self._connect_log()
        self.refresh()

    # ------------------------------------------------------------------ #
    # UI構築
    # ------------------------------------------------------------------ #

    def _setup_ui(self) -> None:
        root = QVBoxLayout(self)
        root.setSpacing(12)
        root.setContentsMargins(20, 16, 20, 16)

        # ---- 上部：敵情報 ----
        self._enemy_panel = self._make_panel()
        ep_layout = QVBoxLayout(self._enemy_panel)
        self._enemy_name_lbl = QLabel()
        self._enemy_name_lbl.setObjectName("subtitle")
        self._enemy_hp_lbl = QLabel()
        self._enemy_block_lbl = QLabel()
        self._enemy_block_lbl.setObjectName("muted")
        ep_layout.addWidget(self._enemy_name_lbl)
        ep_layout.addWidget(self._enemy_hp_lbl)
        ep_layout.addWidget(self._enemy_block_lbl)
        root.addWidget(self._enemy_panel)

        # ---- 中部：プレイヤー情報 ----
        self._player_panel = self._make_panel()
        pp_layout = QHBoxLayout(self._player_panel)
        self._player_hp_lbl = QLabel()
        self._player_block_lbl = QLabel()
        self._player_energy_lbl = QLabel()
        for lbl in (self._player_hp_lbl, self._player_block_lbl, self._player_energy_lbl):
            pp_layout.addWidget(lbl)
        root.addWidget(self._player_panel)

        # ---- 手札エリア ----
        hand_label = QLabel("手札")
        hand_label.setObjectName("subtitle")
        root.addWidget(hand_label)

        self._hand_area = QHBoxLayout()
        self._hand_area.setSpacing(8)
        hand_container = QWidget()
        hand_container.setLayout(self._hand_area)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(hand_container)
        scroll.setFixedHeight(130)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        root.addWidget(scroll)

        # ---- ターン終了ボタン ----
        self._end_turn_btn = QPushButton("ターン終了")
        self._end_turn_btn.setObjectName("end_turn_btn")
        self._end_turn_btn.clicked.connect(self._on_end_turn)
        root.addWidget(self._end_turn_btn, alignment=Qt.AlignmentFlag.AlignRight)

        # ---- ログ ----
        log_label = QLabel("行動ログ")
        log_label.setObjectName("muted")
        root.addWidget(log_label)

        self._log_view = QTextEdit()
        self._log_view.setReadOnly(True)
        self._log_view.setFixedHeight(140)
        root.addWidget(self._log_view)

    @staticmethod
    def _make_panel() -> QFrame:
        frame = QFrame()
        frame.setObjectName("panel")
        return frame

    # ------------------------------------------------------------------ #
    # ログ接続
    # ------------------------------------------------------------------ #

    def _connect_log(self) -> None:
        self.game.set_log_callback(self._append_log)

    def _append_log(self, message: str) -> None:
        self._log_view.append(message)
        self._log_view.verticalScrollBar().setValue(
            self._log_view.verticalScrollBar().maximum()
        )

    # ------------------------------------------------------------------ #
    # 表示更新
    # ------------------------------------------------------------------ #

    def refresh(self) -> None:
        """ゲーム状態に合わせてUIを更新する"""
        g = self.game
        enemy = g.enemy

        # 敵情報
        if enemy:
            self._enemy_name_lbl.setText(f"⚔ {enemy.name}")
            self._enemy_hp_lbl.setText(f"HP: {enemy.hp} / {enemy.max_hp}")
            self._enemy_block_lbl.setText(f"ブロック: {enemy.block}")
        else:
            self._enemy_name_lbl.setText("（敵なし）")
            self._enemy_hp_lbl.setText("")
            self._enemy_block_lbl.setText("")

        # プレイヤー情報
        self._player_hp_lbl.setText(f"❤ HP: {g.player_hp} / {g.player_max_hp}")
        self._player_block_lbl.setText(f"🛡 Block: {g.player_block}")
        self._player_energy_lbl.setText(f"⚡ Energy: {g.energy} / 3")

        # 手札
        self._rebuild_hand()

        # ターン終了ボタン
        self._end_turn_btn.setEnabled(g.in_battle and not g.game_over and not g.game_clear)

    def _rebuild_hand(self) -> None:
        """手札ボタンを再構築する"""
        # 既存ボタンを削除
        while self._hand_area.count():
            item = self._hand_area.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        g = self.game
        can_play = g.in_battle and not g.game_over and not g.game_clear

        for card in g.hand:
            btn = self._make_card_button(card, can_play and g.energy >= card.cost)
            self._hand_area.addWidget(btn)

        # 空きスペース
        self._hand_area.addStretch()

    def _make_card_button(self, card: Card, enabled: bool) -> QPushButton:
        text = f"{card.name}\nCost:{card.cost}\n{card.description}"
        btn = QPushButton(text)
        btn.setObjectName("card_btn")
        btn.setEnabled(enabled)
        btn.clicked.connect(lambda checked=False, c=card: self._on_play_card(c))
        return btn

    # ------------------------------------------------------------------ #
    # イベントハンドラ
    # ------------------------------------------------------------------ #

    def _on_play_card(self, card: Card) -> None:
        success = self.game.play_card(card)
        if success:
            self.refresh()
            self._check_battle_end()

    def _on_end_turn(self) -> None:
        self.game.end_player_turn()
        self.refresh()
        self._check_battle_end()

    def _check_battle_end(self) -> None:
        g = self.game
        if g.game_clear:
            self.battle_ended.emit(True)
        elif g.game_over:
            self.battle_ended.emit(False)
        elif not g.in_battle:
            # 敵を倒したがゲームクリアではない → マップへ
            self.battle_ended.emit(True)
